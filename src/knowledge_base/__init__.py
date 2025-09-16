#import logging
from knowledge_base.logger import logger
from knowledge_base.utils import constants 
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from knowledge_base.utils.config_reader import ConfigReader 

from knowledge_base.common.kbindexerconfig import  KBIndexerConfig
from knowledge_base.common.kbretriverconfig import KBRetrieverConfig
from knowledge_base.core.kb_indexer import KnowledgeBaseIndexer
from knowledge_base.core.kb_retriver import KnowledgeBaseRetriever
from knowledge_base.core.kb_generator import KnowledgeBaseGenerator

def index_rag(): 
    logger.debug("Inside index_rag()")
    configreader = ConfigReader(constants.CONFIG_YMAL_PATH)
    kb_indexer_config = KBIndexerConfig(configreader)
    kb_indexer = KnowledgeBaseIndexer(kb_indexer_config)
    result = kb_indexer.index()
    logger.info(result)
    #print(result)

def retriever_rag():
    logger.debug("Inside retriever_rag()")
    configreader = ConfigReader(constants.CONFIG_YMAL_PATH)
    kb_retriever_config = KBRetrieverConfig(configreader)
    kb_retriver = KnowledgeBaseRetriever(kb_retriever_config)

    #question = input("Enter your question: ")   
    question = "Leave policy" 
    
    if kb_retriver.retriever is not None:
        docs = kb_retriver.retriever.invoke(question)
        for doc in docs:
            print(doc.page_content)
            print(doc.metadata)
    else:
        logger.error("kb_retriver.retriever is None. Check your retriever setup.")

def generation_rag():
    logger.debug("Inside generation_rag()")
    #question = input("Enter your question: ")   
    question = "Leave policy" 
    logger.info(f"Question asked : {question}")
    configreader = ConfigReader(constants.CONFIG_YMAL_PATH)
    kb_retriever_config = KBRetrieverConfig(configreader)
   # kb_retriver = KnowledgeBaseRetriever(kb_retriever_config)
    kb_generator = KnowledgeBaseGenerator(kb_retriever_config)
    if kb_generator is not None:
        response = kb_generator.respond_to_employee(question)
        if response is not None:
            response.pretty_print()
            logger.info(f"Response from system : {response.content}")
        else:
            logger.error("Response from kb_generator.respond_to_employee is None.")
            raise ValueError(f"Response from kb_generator.respond_to_employee is None.: ")

    else:
        logger.error("Could not get Generator Object created.")

def main() -> None:
#    config = ConfigReader(constants.CONFIG_YMAL_PATH)
    #embedding_engine_name = config[constants.EMBEDDING_ENGINE][constants.NAME]  
    #embedding_engine_model = config[constants.EMBEDDING_ENGINE][constants.MODEL] 
    #embedding_engine_base_url =  config[constants.EMBEDDING_ENGINE][constants.BASE_URL]     
#    embedding_engine_name = config[constants.EMBEDDING_ENGINE][constants.NAME]  
#    embedding_engine_model = config[config[constants.EMBEDDING_ENGINE][constants.NAME]][constants.MODEL]
#    embedding_engine_base_url =   config[config[constants.EMBEDDING_ENGINE][constants.NAME]].get(constants.BASE_URL)
#    print(f"embedding_engine_name :{embedding_engine_name}")
#    print(f"embedding_engine_model : {embedding_engine_model}")
#    print(f"embedding_engine_base_url: {embedding_engine_base_url}")
#    llm_model = config[config[constants.LLM][constants.NAME]][constants.MODEL]
#    llm_model_provider = config[config[constants.LLM][constants.NAME]][constants.MODEL_PROVIDER]
#    baseurl = config[config[constants.LLM][constants.NAME]].get(constants.BASE_URL)
#    rewtriver_k = config[config[constants.LLM][constants.NAME]][constants.RETRIEVER_K]
#    rewtriver_score_thr = config[config[constants.LLM][constants.NAME]][constants.RETRIVER_SCORE_THRESHOLD]
#    print(llm_model)
#    print(llm_model_provider )
#    print(f"llm_baseurl :{baseurl}")
#    print(rewtriver_k)
#    print(rewtriver_score_thr)

    logger.info("Starting the app...")
    logger.debug("Inside main()") 
    #index_rag()
    #clear
    retriever_rag()
    generation_rag()
