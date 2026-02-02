from fastapi import APIRouter, HTTPException
from pymilvus import DataType

from models.schemas import CreateCollectionRequest, UpsertRequest, SearchRequest, DropCollectionRequest
from modules.milvus_lite_client import client

router = APIRouter()

# 类型映射表：将 Java 传来的字符串转为 Milvus 类型
TYPE_MAPPING = {
    "VarChar": DataType.VARCHAR,
    "FloatVector": DataType.FLOAT_VECTOR,
    "Int64": DataType.INT64,
    "Float": DataType.FLOAT,
    # 根据需要补充其他类型
}


@router.get("/collections")
async def show_collections():
    """
    获取所有集合
    """
    print(f"GET /collections")
    return client.list_collections()


@router.post("/collections/create")
async def create_collection(req: CreateCollectionRequest):
    try:
        if client.has_collection(req.collection_name):
            client.drop_collection(req.collection_name)
        schema = client.create_schema(
            enable_dynamic_field=True,
            auto_id=False
        )
        for field in req.fields:
            if field.data_type not in TYPE_MAPPING:
                raise HTTPException(status_code=400, detail=f"Unsupported Data Type: {field.data_type}")
            # 构建基础参数
            field_kwargs = {
                "field_name": field.field_name,
                "datatype": TYPE_MAPPING[field.data_type],
                "is_primary": field.is_primary,
                "auto_id": field.auto_id,
                "description": field.description
            }
            # 只有当 max_length 不为 None 时才加入参数
            if field.max_length is not None:
                field_kwargs["max_length"] = field.max_length
            # 只有当 dimension 不为 None 时才加入参数
            if field.dimension is not None:
                field_kwargs["dim"] = field.dimension
            # 动态调用
            schema.add_field(**field_kwargs)
        index_params = client.prepare_index_params()
        for idx in req.indexes:
            index_params.add_index(
                field_name=idx.field_name,
                index_type=idx.index_type,
                metric_type=idx.metric_type
            )

        client.create_collection(
            collection_name=req.collection_name,
            schema=schema,
            index_params=index_params
        )

        return {"status": "success", "collection": req.collection_name}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/collections/drop")
async def drop_collection(req: DropCollectionRequest):
    client.drop_collection(req.collection_name)
    return {"status": "dropped"}


@router.post("/vectors/upsert")
async def upsert(req: UpsertRequest):
    res = client.upsert(req.collection_name, req.data)
    return {"upsert_count": res["upsert_count"]}


@router.post("/vectors/search")
async def search(req: SearchRequest):
    res = client.search(
        collection_name=req.collection_name,
        data=[req.vector],
        limit=req.top_k,
        output_fields=req.output_fields,
        search_params=req.search_params
    )
    # 简化结果
    results = []
    if res and len(res) > 0:
        for hit in res[0]:
            item = hit['entity']
            item['score'] = hit['distance']
            results.append(item)
    return results


from models.schemas import DeleteRequest


@router.post("/vectors/delete")
async def delete_vectors(req: DeleteRequest):
    """
    删除向量接口
    """
    try:
        if not req.ids:
            raise HTTPException(status_code=400, detail="至少需要提供一个ID进行删除")
        # MilvusClient 会自动识别主键名(hash)并处理引号
        res = client.delete(
            collection_name=req.collection_name,
            ids=req.ids
        )
        if isinstance(res, list) and len(res) > 0:
            return {"delete_count": len(res)}
        elif hasattr(res, 'delete_count'):
            return {"delete_count": res.delete_count}
        elif isinstance(res, dict) and 'delete_count' in res:
            return {"delete_count": res['delete_count']}
        else:
            return {"delete_count": len(req.ids)}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
