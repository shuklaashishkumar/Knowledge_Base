from knowledge_base.logger import logger
import yaml
from knowledge_base.utils import constants 
from knowledge_base.common.kbretriverconfig import KBRetrieverConfig
from knowledge_base.core.kb_retriver  import  KnowledgeBaseRetriever
from langchain.chat_models import init_chat_model
from langchain.prompts import load_prompt
from langchain_core.messages import BaseMessage

class KnowledgeBaseGenerator:
    def __init__(self, config:KBRetrieverConfig):
        logger.debug("Inside KnowledgeBaseGenerator.__init__")
        try:
            self._config = config
            self._retriver = KnowledgeBaseRetriever(self._config)
            self._vector_store = self._retriver.retriever
            self._model = init_chat_model(
                model=self._config.llm_model,
                model_provider=self._config.llm_model_provider
                )
        except Exception as e:
            logger.debug(f"Exception occured in __init__ method in KnowledgeBaseGenerator\nException: {e}")

    def format_docs(self, docs):
        logger.debug("Inside KnowledgeBaseGenerator.format_docs")
        try:
            out = []
            for d in docs:
                src = d.metadata.get(constants.SOURCE, constants.UNKWON)
                page = d.metadata.get(constants.PAGE)
                tag = f"{src}" + (f" p.{page}" if page is not None else "")
                txt = d.page_content.strip().replace("\n" , " ")
                out.append(f"source :{tag} ] {txt}")
            return "\n\n".join(out[:12])
        except Exception as e:
            logger.debug(f"Exception occured in format_docs method in KnowledgeBaseGenerator\nException: {e}")
    
    def respond_to_employee(self, question:str)->BaseMessage:
        logger.debug("Inside KnowledgeBaseGenerator.respond_to_employee")
        """_summary_
            Args:
                question (str): _description_
            Returns:
                BaseMessage: _description_
        """
        try:

            if self._vector_store is not None:
                docs = self._vector_store.invoke(question)
                context = self.format_docs(docs)
                prompt = load_prompt(constants.PROMPT_YAML_PATH)
                formatted_prompt = prompt.format(context=context, question=question)
                result = self._model.invoke(formatted_prompt)
                if result is not None:
                    return result
                else:
                    logger.error("Result from self._model.invoke is None.")
            else:
                logger.error("self._vector_store is None. Cannot invoke question.")
        except Exception as e:
            logger.debug(f"Exception occured in respond_to_employee method in KnowledgeBaseGenerator\nException: {e}")
    