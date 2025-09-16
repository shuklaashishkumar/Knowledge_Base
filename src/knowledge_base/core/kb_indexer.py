from knowledge_base.logger import logger
"""Indexer base classes and reusable implementations for RAG indexing pipeline.

This module provides the foundational components for building indexing pipelines
in Retrieval-Augmented Generation (RAG) systems, including base classes and
common implementations for document processing and vector indexing.
"""
from abc import ABC, abstractmethod
from knowledge_base.utils import constants 
from langchain.indexes import SQLRecordManager, IndexingResult
from langchain.indexes import  index
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from knowledge_base.common.kbindexerconfig import KBIndexerConfig 


class KnowledgeBaseIndexer():
    """Abstract base class for RAG indexers.

    This class defines the interface for indexers in a Retrieval-Augmented Generation (RAG)
    system. Subclasses must implement the `index` method to handle the indexing process.

    Methods:
        index: Abstract method to perform indexing of documents.
    """

  
    def __init__(self, config: KBIndexerConfig):
        logger.debug("Inside KnowledgeBaseIndexer.__init__")
        try:
            self._config: KBIndexerConfig = config
            self._setup()
        except Exception as e:
            logger.debug(f"Exception occured in __init__ method in KnowledgeBaseIndexer\nException: {e}")

    def _setup(self):
        logger.debug("Inside KnowledgeBaseIndexer._setup")
        try:
            """Perform any necessary setup operations.

            This method can be overridden by subclasses to perform custom setup
            operations specific to the indexer.
            """
            # Initialize record manager
            self._record_manager = SQLRecordManager(
                namespace=self._config.record_manager_name_space,
                db_url=self._config.record_manager_db_url)
            self._record_manager.create_schema()

            # Initialize embedding model
            if self._config.embedding_engine_name == constants.VERTEX:
                 self._embedding = VertexAIEmbeddings(
                    model_name=self._config.embedding_engine_model
                )
            elif self._config.embedding_engine_name == constants.OPENAI:
                self._embedding = OpenAIEmbeddings(
                    model=self._config.embedding_engine_model
                    )
            elif self._config.embedding_engine_name == constants.HUGGINGFACE:
                self._embedding = HuggingFaceEmbeddings(
                    model_name=self._config.embedding_engine_model
                    )
            else:
                raise ValueError(f"Unsupported embedding engine: {self._config.embedding_engine_name}")

            # Initialize vector store based on configuration
            if self._config.vector_store == constants.CHROMADB:
                self._vector_store = Chroma(
                    embedding_function=self._embedding,
                    persist_directory=self._config.vector_store_persist_path,
                    collection_name=self._config.vector_store_collection_name
                )
            elif self._config.vector_store == constants.FIASS:
                raise ValueError(f"Unsupported vector store: {self._config.vector_store}")
            elif self._config.vector_store == constants.WEAVIATE:
                raise ValueError(f"Unsupported vector store: {self._config.vector_store}")
            else:
                raise ValueError(f"Unsupported vector store: {self._config.vector_store}")

            # Initialize text splitter
            self._text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self._config.chunk_size,
                chunk_overlap=self._config.chunk_overlap,
                separators=list(self._config.separators)
            )
            self._load_docs()
            self._chunked_docs = self._text_splitter.split_documents(self._docs)
        except Exception as e:
            logger.debug(f"Exception occured in _setup method in KnowledgeBaseIndexer\nException: {e}")
   
    def _load_docs(self):
        logger.debug("Inside KnowledgeBaseIndexer._load_docs")
        try:
            """Load documents from a local source.

            This method should be implemented by subclasses to define the specific
            logic for loading documents from a local source.
            """
            # if config glob is about pdf glob pattern load PyPDF loader
            # also implement markdown and text loaders 
            if self._config.glob == constants.GLOB_REGEX_TXT:
                loader = DirectoryLoader(
                    path=self._config.source,
                    glob=self._config.glob,
                    use_multithreading=True
                )
                self._docs = loader.load()
            elif self._config.glob == constants.GLOB_REGEX_MD:
                raise NotImplementedError("Markdown loader is not implemented yet")
            elif self._config.glob == constants.GLOB_REGEX_PDF:
                raise NotImplementedError("Text loader is not implemented yet")
        except Exception as e:
            logger.debug(f"Exception occured in _load_docs method in KnowledgeBaseIndexer\nException: {e}")

    def get_retriever(self, *args, **kwargs)-> VectorStoreRetriever:
        logger.debug("Inside KnowledgeBaseIndexer.get_retriever")
        try:
            """Get a retriever for querying the indexed documents.

            This method returns a retriever object that can be used to query
            the indexed documents.

            Returns:
                BaseRetriever: A retriever for querying the indexed documents.
            """
            return self._vector_store.as_retriever(*args, **kwargs)
        except Exception as e:
            logger.debug(f"Exception occured in get_retriever method in KnowledgeBaseIndexer\nException: {e}")
    


    """Concrete implementation of BaseIndexer for the Employee Handbook.

    This class implements the indexing process for the Employee Handbook,
    utilizing the configurations defined in HandbookIndexConfig.

    Methods:
        index: Perform indexing of documents into the vector store.
    """

    def index(self, *args, **kwargs) -> IndexingResult:
        logger.debug("Inside KnowledgeBaseIndexer.index")
        try:
            """Index documents from a source into the vector store.

            Args:
                source: The source of documents to index.
            """
            # index documents
            result = index(
                docs_source=self._docs,
                record_manager=self._record_manager,
                vector_store=self._vector_store,
                cleanup=self._config.clean_up,
                source_id_key=self._config.source_id_key,
            )
            return result
        except Exception as e:
            logger.debug(f"Exception occured in index method in KnowledgeBaseIndexer\nException: {e}")