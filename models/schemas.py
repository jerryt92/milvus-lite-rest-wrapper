from typing import List, Optional, Any, Dict, Union

from pydantic import BaseModel, Field


# 定义字段描述
class FieldSchemaModel(BaseModel):
    field_name: str
    data_type: str  # 例如 "VarChar", "FloatVector", "Int64"
    max_length: Optional[int] = None
    dimension: Optional[int] = None
    is_primary: bool = False
    auto_id: bool = False
    description: Optional[str] = ""
    enable_analyzer: Optional[bool] = None
    analyzer_params: Optional[Dict[str, Any]] = None


# 定义索引描述
class IndexParamModel(BaseModel):
    field_name: str
    index_type: str  # "AUTOINDEX", "IVF_FLAT" etc.
    metric_type: str  # "COSINE", "L2", "IP"


class FunctionSchemaModel(BaseModel):
    name: str
    function_type: str  # "BM25", "TEXTEMBEDDING", "RANKER"
    input_field_names: Union[str, List[str]]
    output_field_names: Optional[Union[str, List[str]]] = None
    description: Optional[str] = ""
    params: Optional[Dict[str, Any]] = None


# 创建集合的通用请求
class CreateCollectionRequest(BaseModel):
    collection_name: str
    fields: List[FieldSchemaModel]
    indexes: List[IndexParamModel]
    functions: Optional[List[FunctionSchemaModel]] = None


class DropCollectionRequest(BaseModel):
    collection_name: str


class UpsertRequest(BaseModel):
    collection_name: str
    data: List[Dict[str, Any]]


class SearchRequest(BaseModel):
    collection_name: str
    vector: Any
    top_k: int
    output_fields: List[str]
    search_params: Dict[str, Any] = Field(default_factory=dict)  # 比如 metric_type
    anns_field: Optional[str] = None


class DeleteRequest(BaseModel):
    collection_name: str
    ids: List[str]
