import os
import tempfile
from git import Repo
from typing import Dict, List, Tuple
import tiktoken
import markdown
from bs4 import BeautifulSoup
import requests
from pathlib import Path

class GitHubLoader:
    def __init__(self):
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.ignored_dirs = ['.git', '__pycache__', 'node_modules', 'venv', 'env']
        self.text_extensions = ['.md', '.txt', '.py', '.js', '.java', '.c', '.cpp', '.h', '.hpp', 
                              '.html', '.css', '.scss', '.go', '.rs', '.rb', '.sh', '.yaml', '.yml']
    
    def clone_repo(self, repo_url: str) -> str:
        """Clone a GitHub repository to a temporary directory"""
        temp_dir = tempfile.mkdtemp()
        Repo.clone_from(repo_url, temp_dir)
        return temp_dir
    
    def process_repo(self, repo_path: str) -> Tuple[Dict, List[Dict]]:
        """Process all files in a repository"""
        stats = {
            "total_files": 0,
            "file_types": {},
            "total_chunks": 0
        }
        documents = []
        
        for root, _, files in os.walk(repo_path):
            # Skip ignored directories
            if any(ignored in root for ignored in self.ignored_dirs):
                continue
                
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file).suffix.lower()
                
                # Skip non-text files
                if file_ext not in self.text_extensions:
                    continue
                
                # Update stats
                stats["total_files"] += 1
                stats["file_types"][file_ext] = stats["file_types"].get(file_ext, 0) + 1
                
                # Process file content
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Process markdown files
                    if file_ext == '.md':
                        content = self._process_markdown(content)
                    
                    # Split into chunks
                    chunks = self._chunk_text(content)
                    stats["total_chunks"] += len(chunks)
                    
                    # Prepare documents for ChromaDB
                    for i, chunk in enumerate(chunks):
                        documents.append({
                            "text": chunk,
                            "metadata": {
                                "source": file_path.replace(repo_path, '').lstrip('/'),
                                "file_type": file_ext,
                                "chunk_index": i
                            }
                        })
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        
        return stats, documents
    
    def _process_markdown(self, content: str) -> str:
        """Convert markdown to plain text"""
        html = markdown.markdown(content)
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()
    
    def _chunk_text(self, text: str, max_tokens: int = 512) -> List[str]:
        """Split text into chunks based on token count"""
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        for i in range(0, len(tokens), max_tokens):
            chunk_tokens = tokens[i:i + max_tokens]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
        
        return chunks