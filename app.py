import streamlit as st
import os
import tempfile
from utils.github_loader import GitHubLoader
from utils.chroma_manager import ChromaManager
from utils.ollama_helper import OllamaHelper
import time

# Initialize session state
if 'repo_processed' not in st.session_state:
    st.session_state.repo_processed = False
if 'collection_stats' not in st.session_state:
    st.session_state.collection_stats = None
if 'chroma_manager' not in st.session_state:
    st.session_state.chroma_manager = None

# UI Setup
st.set_page_config(page_title="GitASK", layout="wide")
st.title(" GitASK ")

# Sidebar for repo input
with st.sidebar:
    st.header("GitASK")
    repo_url = st.text_input("Enter GitHub Repository URL:", placeholder="https://github.com/username/repo")
    process_btn = st.button("Process Repository")
    
    if process_btn and repo_url:
        with st.spinner("Processing repository..."):
            try:
                # Clone and process repo
                loader = GitHubLoader()
                temp_repo_path = loader.clone_repo(repo_url)
                stats, documents = loader.process_repo(temp_repo_path)
                
                # Initialize ChromaDB
                chroma_manager = ChromaManager()
                chroma_manager.reset_collection()
                
                # Add documents to ChromaDB
                for i, doc in enumerate(documents):
                    chroma_manager.add_documents(
                        documents=[doc['text']],
                        metadatas=[doc['metadata']],
                        ids=[f"doc_{i}"]
                    )
                
                # Update session state
                st.session_state.repo_processed = True
                st.session_state.collection_stats = stats
                st.session_state.chroma_manager = chroma_manager
                
                # Cleanup
                import shutil
                shutil.rmtree(temp_repo_path)
                
                st.success("Repository processed successfully!")
            except Exception as e:
                st.error(f"Error processing repository: {e}")

# Main content area
if st.session_state.repo_processed and st.session_state.collection_stats:
    # Show processing stats
    st.subheader("Repository Processing Stats")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📄 Total files processed", st.session_state.collection_stats['total_files'])
    
    with col2:
        file_types = ", ".join([f"{k} ({v})" for k, v in st.session_state.collection_stats['file_types'].items()])
        st.metric("📚 File types found", file_types)
    
    with col3:
        st.metric("📦 Total chunks indexed", st.session_state.collection_stats['total_chunks'])
    
    st.success("✅ Ready for queries")
    
    # Query section
    st.divider()
    st.subheader("Ask About the Repository")
    
    query = st.text_area("Enter your question:", height=100, placeholder="How do I use the XYZ function?")
    generate_code = st.checkbox("Generate code snippet if applicable", value=True)
    
    if st.button("Submit Query"):
        if query:
            with st.spinner("Searching documentation and generating response..."):
                try:
                    # Query ChromaDB
                    results = st.session_state.chroma_manager.query(query)
                    
                    # Prepare context
                    context = "\n\n".join([doc for doc in results['documents'][0]])
                    sources = "\n".join([f"- {meta['source']}" for meta in results['metadatas'][0]])
                    
                    # Generate response
                    ollama = OllamaHelper()
                    
                    if generate_code:
                        response = ollama.generate_code_snippet(context, query)
                    else:
                        messages = [
                            {"role": "system", "content": "You are a helpful documentation assistant."},
                            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
                        ]
                        response = ollama.chat_completion(messages)
                    
                    # Display results
                    st.subheader("Answer")
                    st.markdown(response)
                    
                    st.subheader("Sources")
                    st.markdown(sources)
                    
                    # Show relevant chunks
                    with st.expander("See relevant document chunks"):
                        for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                            st.markdown(f"**Chunk {i+1} from {meta['source']}**")
                            st.text(doc)
                            st.divider()
                except Exception as e:
                    st.error(f"Error processing query: {e}")
        else:
            st.warning("Please enter a question")
else:
    st.info("Please enter a GitHub repository URL in the sidebar and click 'Process Repository' to get started")

# Footer
st.divider()
st.caption("GitASK - Powered by ChromaDB and Ollama")