import os
import yaml
import argparse
from typing import Dict, Any, List


def parse_openapi_spec(file_path: str) -> Dict[str, Any]:
    """
    解析 OpenAPI 规范文件
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        spec = yaml.safe_load(f)
    return spec


def generate_flask_routes_from_spec(spec: Dict[str, Any], output_dir: str = 'controller'):
    """
    从 OpenAPI 规范生成 Flask 路由代码，按 tag 分组到不同文件
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取 API 版本信息
    info = spec.get('info', {})
    title = info.get('title', 'Generated API')
    version = info.get('version', '1.0.0')

    # 处理路径和操作，按 tag 分组
    paths = spec.get('paths', {})
    tag_groups = group_operations_by_tag(spec)

    # 为每个 tag 生成一个 API 文件
    for tag_name, operations in tag_groups.items():
        # 转换 tag 名称格式，使其成为有效的 Python 文件名
        safe_tag_name = tag_name.replace(' ', '_').replace('-', '_').lower()
        file_name = f"{safe_tag_name}_api.py"
        file_path = os.path.join(output_dir, file_name)

        # 生成基础导入和应用实例
        base_imports = """from fastapi import APIRouter
import json

router = APIRouter()
"""

        # 生成路由代码
        routes_code = []
        for path, method, operation in operations:
            route_code = generate_single_route(path, method, operation)
            routes_code.append(route_code)

        # 组合完整代码
        full_code = base_imports + "\n" + "\n".join(routes_code)

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_code)

        print(f"Flask 路由代码已生成到: {file_path}")


def group_operations_by_tag(spec: Dict[str, Any]) -> Dict[str, List[tuple]]:
    """
    按 tag 对操作进行分组
    """
    paths = spec.get('paths', {})
    tag_groups = {}

    for path, path_item in paths.items():
        for method, operation in path_item.items():
            # 获取操作的 tags
            tags = operation.get('tags', [])
            if not tags:
                # 如果没有标签，使用默认标签
                tags = ['default']

            # 将操作添加到每个相关的标签组中
            for tag in tags:
                if tag not in tag_groups:
                    tag_groups[tag] = []
                tag_groups[tag].append((path, method, operation))

    return tag_groups


def generate_single_route(path: str, method: str, operation: Dict[str, Any]) -> str:
    """
    生成单个路由的代码
    """
    # 转换路径参数格式
    flask_path = path.replace('{', '<').replace('}', '>')

    # 获取函数名 - 使用 operationId 或基于路径和方法生成
    operation_id = operation.get('operationId',
                                 f"{method.lower()}_{path.replace('/', '_').replace('<', '_').replace('>', '_').strip('_')}")
    operation_id = operation_id.replace('-', '_').replace('__', '_')

    # 生成路由装饰器
    method_upper = method.upper()
    if method_upper == 'GET':
        decorator = f'@router.get("{path}")'
    elif method_upper == 'POST':
        decorator = f'@router.post("{path}")'
    elif method_upper == 'PUT':
        decorator = f'@router.put("{path}")'
    elif method_upper == 'DELETE':
        decorator = f'@router.delete("{path}")'
    elif method_upper == 'PATCH':
        decorator = f'@router.patch("{path}")'
    else:
        decorator = f'@router.route("{path}", methods=["{method_upper}"])'

    # 生成函数体
    summary = operation.get('summary', f'Handle {method_upper} request for {path}')
    responses = operation.get('responses', {})

    # 确定返回值
    response_example = get_response_example(responses)

    # 生成完整的函数代码
    function_code = f"""{decorator}
async def {operation_id}():
    \"\"\"{summary}\"\"\"
    # TODO: 实现业务逻辑
    return {response_example}
"""
    return function_code


def get_response_example(responses: Dict[str, Any]) -> str:
    """
    从响应定义中获取示例返回值
    """
    for status_code, response in responses.items():
        if status_code == '200' or status_code.startswith('2'):
            content = response.get('content', {})
            for content_type, schema_info in content.items():
                example = schema_info.get('example')
                if example is not None:
                    return str(example)

                # 尝试从 schema 获取示例
                schema = schema_info.get('schema', {})
                if schema.get('type') == 'object':
                    properties = schema.get('properties', {})
                    if properties:
                        example_obj = {}
                        for prop_name, prop_schema in properties.items():
                            prop_type = prop_schema.get('type', 'string')
                            example_obj[prop_name] = get_example_value(prop_type)
                        return str(example_obj)

    # 默认返回
    return '{"status": "ok"}'


def get_example_value(prop_type: str) -> Any:
    """
    根据类型返回示例值
    """
    type_examples = {
        'string': 'example',
        'integer': 0,
        'number': 0.0,
        'boolean': True,
        'array': [],
        'object': {}
    }
    return type_examples.get(prop_type, 'value')


def main():
    parser = argparse.ArgumentParser(description='OpenAPI 规范到 Flask 路由生成器')
    parser.add_argument('--input', '-i', default='openapi-interface.yaml',
                        help='指定输入文件 (默认: openapi-interface.yaml)')
    parser.add_argument('--output', '-o', default='generated',
                        help='指定输出目录 (默认: controller)')

    args = parser.parse_args()

    # 检查输入文件是否存在
    if not os.path.exists(args.input):
        print(f'{args.input} 文件不存在')
        return

    # 解析 OpenAPI 规范
    try:
        spec = parse_openapi_spec(args.input)
        print(f'成功解析 OpenAPI 规范: {args.input}')

        # 生成 Flask 路由
        generate_flask_routes_from_spec(spec, args.output)
        print(f'Flask 路由代码已生成到 {args.output} 目录')
    except Exception as e:
        print(f'解析或生成失败: {e}')


if __name__ == '__main__':
    main()