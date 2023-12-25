import json


def flattenjson(json_obj, normalresult=None):
    if normalresult is None:
        normalresult = {}
    # 用于存储处理过程中的临时结果
    temp_results = [{}]
    for k, v in json_obj.items():
        if isinstance(v, dict):
            # 递归处理嵌套字典，并合并结果
            nested_results = flattenjson(v)
            temp_results = [
                dict(item, **nested)
                for nested in nested_results
                for item in temp_results
            ]
        elif isinstance(v, list):
            # 处理列表，为每个元素创建新的字典
            temp_results = [dict(item, **{k: j}) for j in v for item in temp_results]
        else:
            # 处理普通键值对，加入到临时结果中
            for item in temp_results:
                item[k] = v
    # 将普通结果合并到每个字典中
    final_results = [dict(item, **normalresult) for item in temp_results]
    return final_results
