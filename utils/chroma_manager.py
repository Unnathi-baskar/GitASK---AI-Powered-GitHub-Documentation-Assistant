import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Optional
import os

class ChromaManager:
    def __init__(self, collection_name: str = "docs_collection", persist_dir: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )
    
    def add_documents(self, documents: List[str], metadatas: List[Dict], ids: List[str]):
        """Add documents to the collection"""
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(self, query_text: str, n_results: int = 5) -> Dict:
        """Query the collection for similar documents"""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        return {
            "count": self.collection.count(),
            "name": self.collection.name
        }
    
    def reset_collection(self):
        """Reset the entire collection"""
        self.client.delete_collection(name=self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            embedding_function=self.embedding_function
        )