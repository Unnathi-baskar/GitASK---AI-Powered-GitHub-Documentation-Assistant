import requests
import json
from typing import Dict, List

class OllamaHelper:
    def __init__(self, base_url: str = "http://localhost:11434/api"):
        self.base_url = base_url
    
    def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings using Ollama"""
        response = requests.post(
            f"{self.base_url}/embeddings",
            json={"model": "llama3", "prompt": text}
        )
        response.raise_for_status()
        return response.json().get("embedding", [])
    
    def generate_code_snippet(self, context: str, question: str) -> str:
        """Generate a code snippet based on context and question"""
        prompt = f"""You are a helpful coding assistant. Based on the following documentation context:
        
        {context}
        
        Answer the question: {question}
        
        Provide a clear code example if applicable. Include explanations if needed."""
        
        response = requests.post(
            f"{self.base_url}/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.9
                }
            }
        )
        response.raise_for_status()
        return response.json().get("response", "")
    
    def chat_completion(self, messages: List[Dict]) -> str:
        """Chat completion with Ollama"""
        response = requests.post(
            f"{self.base_url}/chat",
            json={
                "model": "llama3",
                "messages": messages,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "")