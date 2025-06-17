from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from app.core.config import settings
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict
import pickle

class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.OPENAI_MODEL,
            temperature=0.1
        )
        # Ensure storage directories exist
        os.makedirs(settings.POLICIES_DIR, exist_ok=True)
        
        # Initialize vector search components
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.documents = []
        self._load_or_create_index()
    
    def _load_or_create_index(self):
        index_path = os.path.join(settings.STORAGE_DIR, 'vector_index.faiss')
        documents_path = os.path.join(settings.STORAGE_DIR, 'documents.pkl')
        
        if os.path.exists(index_path) and os.path.exists(documents_path):
            # Load existing index and documents
            self.index = faiss.read_index(index_path)
            with open(documents_path, 'rb') as f:
                self.documents = pickle.load(f)
        else:
            # Create new index
            self.index = faiss.IndexFlatL2(384)  # 384 is the dimension of all-MiniLM-L6-v2
            self.documents = []
    
    def _save_index(self):
        index_path = os.path.join(settings.STORAGE_DIR, 'vector_index.faiss')
        documents_path = os.path.join(settings.STORAGE_DIR, 'documents.pkl')
        
        faiss.write_index(self.index, index_path)
        with open(documents_path, 'wb') as f:
            pickle.dump(self.documents, f)
    
    def _chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """Split text into overlapping chunks."""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - 100):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks
    
    def _get_relevant_context(self, question: str, k: int = 3) -> str:
        """Get relevant context using vector similarity search."""
        if not self.documents:
            return "No policy documents have been ingested yet."
        
        # Encode the question
        question_vector = self.model.encode([question])[0]
        
        # Search for similar documents
        distances, indices = self.index.search(
            np.array([question_vector]).astype('float32'), k
        )
        
        # Get the most relevant chunks
        relevant_chunks = [self.documents[i] for i in indices[0]]
        
        # Combine the chunks into context
        context = "\n\n".join(relevant_chunks)
        return context
    
    def _create_prompt(self, question: str, context: str) -> str:
        template = """You are a helpful assistant that answers questions about company policies and standards.
        Use the following context to answer the question. If you cannot find the answer in the context,
        say that you don't have enough information to answer the question.

        Context: {context}

        Question: {question}

        Answer:"""
        
        prompt = ChatPromptTemplate.from_template(template)
        return prompt.format(context=context, question=question)
    
    async def answer_question(self, question: str) -> str:
        try:
            # Get relevant context from stored policies
            context = self._get_relevant_context(question)
            
            # Create the prompt
            prompt = self._create_prompt(question, context)
            
            # Generate response
            chain = LLMChain(llm=self.llm, prompt=ChatPromptTemplate.from_template(prompt))
            response = await chain.arun(question=question, context=context)
            
            return response.strip()
            
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
    
    async def ingest_document(self, document_text: str, document_name: str):
        try:
            # Store document in local filesystem
            file_path = os.path.join(settings.POLICIES_DIR, document_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(document_text)
            
            # Process document for vector search
            chunks = self._chunk_text(document_text)
            
            # Encode chunks
            chunk_vectors = self.model.encode(chunks)
            
            # Add to FAISS index
            self.index.add(np.array(chunk_vectors).astype('float32'))
            
            # Store chunks
            self.documents.extend(chunks)
            
            # Save updated index and documents
            self._save_index()
            
            return {"status": "success", "message": f"Document {document_name} ingested successfully"}
        except Exception as e:
            raise Exception(f"Error ingesting document: {str(e)}") 