from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Literal


@dataclass
class KBGeneratorConfig:
 
    vector_store: Literal["chromadb", "faiss", "weaviate"] 
   
    vector_store_persist_path: Optional[str] 
   
    vector_store_collection_name: Optional[str] 
   
    embedding_engine: Literal["vertex","openai", "huggingface"] 
   
    embedding_model_name: str 
    
    source_id_key: Optional[str] 
   
    retriever_k: int 
   
    retriever_score_threshold: float
       
    model_provier: str 

    model: str 