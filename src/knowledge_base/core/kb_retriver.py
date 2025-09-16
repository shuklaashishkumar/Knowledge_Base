from knowledge_base.logger import logger
import yaml
from langchain.vectorstores.base import VectorStoreRetriever 
from langchain_chroma import Chroma
from langchain_google_vertexai import VertexAIEmbeddings
from knowledge_base.common.kbretriverconfig import KBRetrieverConfig
from knowledge_base.utils import constants 

class KnowledgeBaseRetriever:
 
    def __init__(self, config: KBRetrieverConfig):
        logger.debug("Inside KnowledgeBaseRetriever.__init__")
        try:
            self._config = config

            # Initialize embedding model

            if self._config.embedding_engine_name == constants.VERTEX:
                    self._embedding = VertexAIEmbeddings(
                    model_name=self._config.embedding_engine_model
                ) 
            elif self._config.embedding_engine_name == constants.OPENAI:
                #self._embedding = OpenAIEmbeddings(model=self._config.embedding_engine_model)
                raise ValueError(f"Unsupported embedding engine: {self._config.embedding_engine_name}")   
            elif self._config.embedding_engine_name == constants.HUGGINGFACE:
                #self._embedding = HuggingFaceEmbeddings(model_name=self._config.embedding_engine_model)
                raise ValueError(f"Unsupported embedding engine: {self._config.embedding_engine_name}") 
            else:
                raise ValueError(f"Unsupported embedding engine: {self._config.embedding_engine_name}") 
        
            """Set up the retriever based on the provided configuration."""

            if self._config.vector_store == constants.CHROMADB:
                self._vector_store = Chroma(
                    embedding_function=self._embedding,
                    persist_directory=self._config.vector_store_persist_path,
                    collection_name=self._config.vector_store_collection_name
                )
            elif self._config.vector_store == constants.FIASS:
                #self._vector_store = FAISS.load_local(self._config.vector_store_persist_path, self.embedding_model)
                raise ValueError(f"Unsupported vector store: {self._config.vector_store}")
            elif self._config.vector_store == constants.WEAVIATE:
                #self._vector_store = Weaviate(url="http://localhost:8080",  index_name=self._config.vector_store_collection_name,embedding_function=self.embedding_model.embed_query )
                raise ValueError(f"Unsupported vector store: {self._config.vector_store}")
            else:
                raise ValueError(f"Unsupported vector store: {self._config.vector_store}")
        except Exception as e:
            logger.debug(f"Exception occured in _setup method in KnowledgeBaseRetriever\nException: {e}")
    @property  
    def retriever(self ):
        logger.debug("Inside KnowledgeBaseRetriever.retriever")
        try:
            """Retrieve documents based on the query."""
            # Initialize retriever
            return  self._vector_store.as_retriever()
        except Exception as e:
            logger.debug(f"Exception occured in retriever property in KnowledgeBaseRetriever\nException: {e}")

      