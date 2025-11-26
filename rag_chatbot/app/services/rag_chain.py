from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings
from app.services.vector_store import VectorStoreService

class RAGService:
    def __init__(self, vector_store_service: VectorStoreService):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=settings.OPENAI_API_KEY)
        self.vector_store_service = vector_store_service
        
        # Define system prompt
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "\n\n"
            "{context}"
        )
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

    def get_answer(self, query: str):
        retriever = self.vector_store_service.as_retriever()
        question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        response = rag_chain.invoke({"input": query})
        return response
