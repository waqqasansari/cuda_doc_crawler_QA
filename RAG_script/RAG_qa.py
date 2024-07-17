import os
import tempfile
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_milvus.vectorstores import Milvus
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers import ContextualCompressionRetriever
from langchain.prompts import ChatPromptTemplate
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
import glob


class ChatbotLogic:
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.index_name = "chatbot_index"

        os.environ["OPENAI_API_KEY"] = self.openai_api_key

        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")

        print("Loading and processing text files...")
        self.docs = self.load_text_files('./data/*.txt')

        print("Initializing embeddings and semantic chunking...")
        self.embeddings = OpenAIEmbeddings()
        self.semantic_chunker = SemanticChunker(OpenAIEmbeddings(), breakpoint_threshold_type="standard_deviation")
        self.splits = self.semantic_chunker.create_documents(self.docs)

        print("Setting up Milvus Lite...")
        self.temp_dir = tempfile.mkdtemp()
        # self.milvus_lite_uri = f"sqlite:///{os.path.join(self.temp_dir, 'milvus_lite.db')}"
        self.milvus_lite_uri = "./milvus_demo.db"

        # self.flat_vectorstore = MilvusLite.from_documents(
        #     documents=self.splits,
        #     embedding=self.embeddings,
        #     collection_name="flat_collection",
        #     connection_args={"uri": self.milvus_lite_uri},
        #     index_params={"metric_type": "L2", "index_type": "FLAT", "params": {}}
        # )

        self.ivf_vectorstore = Milvus.from_documents(
            documents=self.splits,
            embedding=self.embeddings,
            collection_name="ivf_collection",
            connection_args={"uri": self.milvus_lite_uri},
            index_params={"metric_type": "L2", "index_type": "IVF_FLAT", "params": {"nlist": 1024}}
        )

        print("Setting up retrievers...")
        # self.flat_retriever = self.flat_vectorstore.as_retriever(search_kwargs={"k": 5})
        self.ivf_retriever = self.ivf_vectorstore.as_retriever(search_kwargs={"k": 5})
        self.bm25_retriever = BM25Retriever.from_documents(self.splits)
        self.bm25_retriever.k = 5

        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.bm25_retriever, self.ivf_retriever],
            weights=[0.3, 0.35]
        )

        print("Setting up reranker...")
        compressor = LLMChainExtractor.from_llm(self.llm)
        self.reranker = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=self.ensemble_retriever)

        print("Setting up question-answering chains...")
        self.contextualize_q_system_prompt = """Given a chat history and the latest user question\ 
                                                which might reference context in the chat history, formulate a standalone question \
                                                which can be understood without the chat history. Do NOT answer the question, \
                                                just reformulate it if needed and otherwise return it as is."""
        self.contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        self.history_aware_retriever = create_history_aware_retriever(
            self.llm, self.reranker, self.contextualize_q_prompt
        )

        self.qa_system_prompt = """You are an assistant for question-answering tasks. \
                                Use the following pieces of retrieved context to answer the question. \
                                If you don't know the answer, just say that you don't know. \
                                Use three sentences maximum and keep the answer concise.\

                                {context}"""
        self.qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        self.question_answer_chain = create_stuff_documents_chain(self.llm, self.qa_prompt)

        self.rag_chain = create_retrieval_chain(
            self.history_aware_retriever, self.question_answer_chain
        )

        self.store = {}

    def load_text_files(self, file_pattern):
        documents = []
        for file_path in glob.glob(file_pattern):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                documents.append(content)
        # print('documents', documents)
        return documents

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def process_message(self, session_id: str, user_input: str) -> str:
        conversational_rag_chain = RunnableWithMessageHistory(
            self.rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
        response = conversational_rag_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}},
        )
        return response
    

if __name__ == "__main__":
    # Create an instance of ChatbotLogic
    assistant = ChatbotLogic()

    # Define a session ID for the conversation (can be any unique identifier)
    session_id = "123"

    # Start the conversation
    print("Bot: Hello! How can I assist you today?")

    while True:
        # User input
        user_input = input("You: ")

        # Check for termination command (e.g., "exit" or "quit")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Bot: Goodbye!")
            break
        
        # Process the user input and get the response
        response = assistant.process_message(session_id, user_input)

        # Print the response
        print("Bot:", response["answer"])