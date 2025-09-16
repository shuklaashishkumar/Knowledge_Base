from knowledge_base.logger import logger
from knowledge_base.utils import constants 
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Literal
from knowledge_base.utils.config_reader import ConfigReader 

from knowledge_base.logger import logger

class KBIndexerConfig:
    """
    Configuration for the Handbook application.

    Attributes:
        source_type (str): Type of the source, either 'local' or 'url'.
        source (str): Path or URL of the source data.
        glob (Optional[str]): Glob pattern to match files in local source.
        vector_store (str): Type of vector store to use ('chromadb', 'faiss', 'weaviate').
        vector_store_persist_path (Optional[str]): Path to persist the vector store.
        vector_store_collection_name (Optional[str]): Name of the collection in the vector store.
        record_manager_db_url (str): Database URL for the record manager.
        record_manager_name_space (Optional[str]): Namespace for the record manager.
        embedding_engine (str): Embedding engine to use ('vertex', 'openai', 'huggingface').
        embedding_model_name (str): Name of the embedding model.
        doc_store_type (str): Type of document store ('local', 'pinecone', 'weaviate', 'chroma').
        doc_store_persist_path (Optional[str]): Path to persist the document store.
        source_id_key (Optional[str]): Key to identify the source in documents.
        clean_up (str): Cleanup strategy ('full', 'incremental', 'none').
        chunk_size (int): Size of text chunks for processing.
        chunk_overlap (int): Overlap size between text chunks.
        separator (Tuple[str]): Tuple of separators used for chunking text.
    """

    source:str = field(default="data/")

    glob: Optional[str] 
    
    vector_store: Literal[constants.CHROMADB, constants.FIASS, constants.WEAVIATE]
    
    vector_store_persist_path: Optional[str] 
    
    vector_store_collection_name: Optional[str] 

    record_manager_db_url: str 
    
    record_manager_name_space:Optional[str]  
    
    embedding_engine_name: str
    #Literal[constants.VERTEX,constants.OPENAI, constants.HUGGINGFACE] 
    
    embedding_engine_model: str 

    embedding_engine_base_url: str 
    
    source_id_key: Optional[str] 
    
    clean_up:str 
    
    chunk_size: int 
    
    chunk_overlap: int 
    
    separators: Tuple[str] 

    def __init__(self , config: ConfigReader):
        self._setup(config)
    
    def _setup(self, config: ConfigReader):
        try:
            logger.info("inside KBIndexerConfig._setup()")
            self.source = config[constants.SPLITTER][constants.SOURCE]

            self.glob = config[constants.SPLITTER][constants.GLOB]
            
            self.vector_store = config[constants.VECTORDB][constants.TYPE]
            
            self.vector_store_persist_path = config[constants.VECTORDB][constants.PERSIST_PATH] 
            
            self.vector_store_collection_name = config[constants.VECTORDB][constants.COLLECTION_NAME]  

            self.record_manager_db_url = config[constants.SQLRECORDMANAGER][constants.URL]  
            
            self.record_manager_name_space  = config[constants.SQLRECORDMANAGER][constants.NAMESPACE]  
            
            self.source_id_key = config[constants.SQLRECORDMANAGER][constants.SOURCE_ID_KEY]  
            
            self.clean_up = config[constants.SQLRECORDMANAGER][constants.CLEAN_UP]  
     
            self.embedding_engine_name = config[constants.EMBEDDING_ENGINE][constants.NAME]  
            
            #self.embedding_engine_model = config[constants.EMBEDDING_ENGINE][constants.MODEL]   
            
            #self.embedding_engine_base_url =  config[constants.EMBEDDING_ENGINE][constants.BASE_URL]  

            self.embedding_engine_model = config[config[constants.EMBEDDING_ENGINE][constants.NAME]][constants.MODEL]
            
            self.embedding_engine_base_url =   config[config[constants.EMBEDDING_ENGINE][constants.NAME]].get(constants.BASE_URL)

            self.chunk_size = config[constants.SPLITTER][constants.CHUNK_SIZE]    
            
            self.chunk_overlap = config[constants.SPLITTER][constants.CHUNK_OVERLAP]   
            
            self.separators = config[constants.SPLITTER][constants.SEPARATORS]   
            
            
        except Exception as e:
            logger.debug(f"Exception occured in _setup() method in KBIndexerConfig \nException: {e}")
            print(f"Exception occured in _setup() method in kbindexerconfig.py\nException: {e}")

        


