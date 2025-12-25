from typing import List, Optional, Any, Dict
from pydantic import BaseModel

# 定义字段描述
class FieldSchemaModel(BaseModel):
    field_name: str
    data_type: str  # 例如 "VarChar", "FloatVector", "Int64"
    max_length: Optional[int] = None
    dimension: Optional[int] = None
    is_primary: bool = False
    auto_id: bool = False
    description: Optional[str] = ""

# 定义索引描述
class IndexParamModel(BaseModel):
    field_name: str
    index_type: str  # "AUTOINDEX", "IVF_FLAT" etc.
    metric_type: str # "COSINE", "L2", "IP"

# 创建集合的通用请求
class CreateCollectionRequest(BaseModel):
    collection_name: str
    fields: List[FieldSchemaModel]
    indexes: List[IndexParamModel]

class DropCollectionRequest(BaseModel):
    collection_name: str

class UpsertRequest(BaseModel):
    collection_name: str
    data: List[Dict[str, Any]]

class SearchRequest(BaseModel):
    collection_name: str
    vector: List[float]
    top_k: int
    output_fields: List[str]
    search_params: Dict[str, Any] = {} # 比如 metric_type

class DeleteRequest(BaseModel):
    collection_name: str
    ids: List[str]