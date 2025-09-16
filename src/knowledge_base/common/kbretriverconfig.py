from knowledge_base.utils import constants 
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Literal
from knowledge_base.utils.config_reader import ConfigReader
from knowledge_base.logger import logger

class KBRetrieverConfig:
 
    vector_store: str 
    #Literal[constants.CHROMADB, constants.FIASS, constants.WEAVIATE] 
   
    vector_store_persist_path: Optional[str] 
   
    vector_store_collection_name: Optional[str] 
        
    source_id_key: Optional[str] 
   
    embedding_engine_name: str 

    embedding_engine_model: str
    
    embedding_engine_base_url: str 
   
    llm_model: str 

    llm_model_provider: str 

    llm_base_url: str
    
    llm_retriever_k: int 
   
    llm_retriever_score_threshold: float

    def __init__(self , config: ConfigReader):
        try:

            self.vector_store = config[constants.VECTORDB][constants.TYPE ] 
            self.vector_store_persist_path = config[constants.VECTORDB][constants.PERSIST_PATH] 
            self.vector_store_collection_name = config[constants.VECTORDB][constants.COLLECTION_NAME]
            self.source_id_key = config[constants.SQLRECORDMANAGER][constants.SOURCE_ID_KEY]  

            self.embedding_engine_name = config[constants.EMBEDDING_ENGINE][constants.NAME]   
            self.embedding_engine_model = config[config[constants.EMBEDDING_ENGINE][constants.NAME]][constants.MODEL]
            self.embedding_engine_base_url =   config[config[constants.EMBEDDING_ENGINE][constants.NAME]].get(constants.BASE_URL)

            self.llm_model = config[config[constants.LLM][constants.NAME]][constants.MODEL]
            self.llm_model_provider = config[config[constants.LLM][constants.NAME]][constants.MODEL_PROVIDER]
            self.llm_base_url = config[config[constants.LLM][constants.NAME]].get(constants.BASE_URL)
            self.llm_retriever_k  = config[config[constants.LLM][constants.NAME]][constants.RETRIEVER_K]
            self.llm_retriever_score_threshold = config[config[constants.LLM][constants.NAME]][constants.RETRIVER_SCORE_THRESHOLD]

        except Exception as e:
            logger.debug(f"Exception occured in __init__ method in KBRetrieverConfig\nException: {e}")
            


        
        
