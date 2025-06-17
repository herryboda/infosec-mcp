from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from app.core.config import settings
import os
import json

class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.OPENAI_MODEL,
            temperature=0.1
        )
        # Ensure storage directories exist
        os.makedirs(settings.POLICIES_DIR, exist_ok=True)
        
    def _get_relevant_context(self, question: str) -> str:
        # TODO: Implement vector search to find relevant policy documents
        # For now, we'll return a placeholder
        return "Company policy context will be retrieved here."
    
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
            return {"status": "success", "message": f"Document {document_name} ingested successfully"}
        except Exception as e:
            raise Exception(f"Error ingesting document: {str(e)}") 