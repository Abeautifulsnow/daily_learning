from typing import Annotated, Any, Callable, Dict, List, Literal, Optional, Tuple, TypedDict


def classify_by(data: List[Dict[Any, Any]], by_key: Any) -> Dict[Any, List[Dict[Any, Any]]]:
    """相同by的数据进行分类

    比如:
    .. code-block:: python3

    [
        {
            "ts": "2024-04-04T00:03:00",
            "itemvalue": 0.7,
            "devproperty": "PGY02003_SPD01001_STPDZ01001_UDYPDX001_EQPD01DYPDX057_MPPFb2001"
        },
        {
            "ts": "2024-04-04T00:15:00",
            "itemvalue": 0.71,
            "devproperty": "PGY02003_SPD01001_STPDZ01001_UDYPDX001_EQPD01DYPDX057_MPPFb2001"
        },
        {
            "ts": "2024-04-04T00:03:00",
            "itemvalue": 0.04,
            "devproperty": "PGY02003_SPD01001_STPDZ01004_UDYPDX001_EQPD01DYPDX085_MPTUb2001"
        },
        {
            "ts": "2024-04-04T00:15:00",
            "itemvalue": 0.04,
            "devproperty": "PGY02003_SPD01001_STPDZ01004_UDYPDX001_EQPD01DYPDX085_MPTUb2001"
        }
    ]

    转化后:
    .. code-block:: python3

    {
        "2024-04-04 00:03:00": [
            {
                "ts": "2024-04-04T00:03:00",
                "itemvalue": 0.7,
                "devproperty": "PGY02003_SPD01001_STPDZ01001_UDYPDX001_EQPD01DYPDX057_MPPFb2001"
            },
            {
                "ts": "2024-04-04T00:03:00",
                "itemvalue": 0.04,
                "devproperty": "PGY02003_SPD01001_STPDZ01004_UDYPDX001_EQPD01DYPDX085_MPTUb2001"
            }
        ],
        "2024-04-04 00:15:00": [
            {
                "ts": "2024-04-04T00:15:00",
                "itemvalue": 0.71,
                "devproperty": "PGY02003_SPD01001_STPDZ01001_UDYPDX001_EQPD01DYPDX057_MPPFb2001"
            },
            {
                "ts": "2024-04-04T00:15:00",
                "itemvalue": 0.04,
                "devproperty": "PGY02003_SPD01001_STPDZ01004_UDYPDX001_EQPD01DYPDX085_MPTUb2001"
            }
        ]
    }
    """

    result: Dict[Any, List[Dict[Any, Any]]] = defaultdict(lambda: [])

    for _d in data:
        by_item = str(_d.get(by_key))
        _d[by_key] = by_item
        if result.get(by_item) is not None:
            result[by_item].append(_d)
        else:
            result[by_item] = [_d]

    return result


def classify_by1(data: List[Dict[Any, Any]], by_key: Any, append_key: Any) -> Dict[Any, List[Any]]:
    """相同by的数据进行分类

    data = [
        {
            "ts": "2024-04-04T00:03:00",
            "itemvalue": 0.7,
            "devproperty": "PGY02003_SPD01001_STPDZ01001_UDYPDX001_EQPD01DYPDX057_MPPFb2001",
        },
        {
            "ts": "2024-04-04T00:15:00",
            "itemvalue": 0.71,
            "devproperty": "PGY02003_SPD01001_STPDZ01001_UDYPDX001_EQPD01DYPDX057_MPPFb2001",
        },
        {
            "ts": "2024-04-04T00:03:00",
            "itemvalue": 0.04,
            "devproperty": "PGY02003_SPD01001_STPDZ01004_UDYPDX001_EQPD01DYPDX085_MPTUb2001",
        },
        {
            "ts": "2024-04-04T00:15:00",
            "itemvalue": 0.04,
            "devproperty": "PGY02003_SPD01001_STPDZ01004_UDYPDX001_EQPD01DYPDX085_MPTUb2001",
        },
    ]

    ==========
    {'2024-04-04T00:03:00': [0.7, 0.04], '2024-04-04T00:15:00': [0.71, 0.04]}
    """

    result: Dict[Any, List[Any]] = defaultdict(lambda: [])

    for _d in data:
        by_item = str(_d.get(by_key))
        _d[by_key] = by_item

        append_key_value = _d.get(append_key)
        if result.get(by_item) is not None:
            result[by_item].append(append_key_value)
        else:
            result[by_item] = [append_key_value]

    return result


def classify_by2(
    data: List[Dict[Any, Any]], by_key: Any, key_key: Any, value_key: Any, return_columns: bool = False
) -> Dict[Any, Dict[Any, Any]] | Tuple[Dict[Any, Dict[Any, Any]], List]:
    """相同by的数据进行归并

    Args:
        data (List[Dict[Any, Any]]): 原数据集, List[Dict] 类型
        by_key (Any): 存在相同值的字典key
        key_key (Any): 需要作为分类后字典key的key
        value_key (Any): 需要作为分类后字典value的key

    原数据:
    .. code-block:: python3
    data =
    [
        {
            "ts": "2024-04-04T00:03:00",
            "itemvalue": 0.7,
            "devproperty": "PGY02003_SPD01001_STPDZ01001_UDYPDX001_EQPD01DYPDX057_MPPFb2001"
        },
        {
            "ts": "2024-04-04T00:15:00",
            "itemvalue": 0.71,
            "devproperty": "PGY02003_SPD01001_STPDZ01001_UDYPDX001_EQPD01DYPDX057_MPPFb2001"
        },
        {
            "ts": "2024-04-04T00:03:00",
            "itemvalue": 0.04,
            "devproperty": "PGY02003_SPD01001_STPDZ01004_UDYPDX001_EQPD01DYPDX085_MPTUb2001"
        },
        {
            "ts": "2024-04-04T00:15:00",
            "itemvalue": 0.04,
            "devproperty": "PGY02003_SPD01001_STPDZ01004_UDYPDX001_EQPD01DYPDX085_MPTUb2001"
        }
    ]

    Returns:
        Dict[Any, Dict[Any, Any]]: 如下

    [
        {
            "ts": "2024-04-04T00:03:00",
            "PGY02003_SPD01001_STPDZ01001_UDYPDX001_EQPD01DYPDX057_MPPFb2001": 0.7,
            "PGY02003_SPD01001_STPDZ01004_UDYPDX001_EQPD01DYPDX085_MPTUb2001": 0.04
        }, {
            "ts": "2024-04-04T00:15:00",
            "PGY02003_SPD01001_STPDZ01001_UDYPDX001_EQPD01DYPDX057_MPPFb2001": 0.71,
            "PGY02003_SPD01001_STPDZ01004_UDYPDX001_EQPD01DYPDX085_MPTUb2001": 0.04
        }
    ]
    """

    merged_data: Dict = defaultdict(dict)
    columns = []

    for entry in data:
        by_item = entry.get(by_key)

        if isinstance(by_item, datetime):
            by_item = by_item.strftime("%Y-%m-%d %H:%M:%S")

        key_key_item = entry[key_key]
        if isinstance(key_key_item, datetime):
            key_key_item = key_key_item.strftime("%Y-%m-%d %H:%M:%S")

        value_key_item = entry[value_key]
        if isinstance(value_key_item, datetime):
            value_key_item = value_key_item.strftime("%Y-%m-%d %H:%M:%S")

        merged_data[by_item][by_key] = by_item
        merged_data[by_item][key_key_item] = value_key_item

        columns.append(key_key_item)

    if return_columns:
        return merged_data, list(sorted(set(columns)))

    return merged_data


def classify_by3(data: List[Dict[Any, Any]], by_key: Any) -> List[Dict[Any, Any]]:
    """相同by的数据进行归并

        Args:
            data (List[Dict[Any, Any]]): 原数据集, List[Dict] 类型
            by_key (Any): 存在相同值的字典key

        原数据:
        .. code-block:: python3
        data =
        [
        {"gateway": "747331", "2024-02-21 10:30:00": 1},
        {"gateway": "747337", "2024-02-21 10:30:00": 1},
        {"gateway": "747329", "2024-02-21 10:30:00": 1},
        {"gateway": "747341", "2024-02-21 10:30:00": 1},
        {"gateway": "747321", "2024-02-21 10:30:00": 1},
        {"gateway": "747323", "2024-02-21 10:30:00": 1},
        {"gateway": "747325", "2024-02-21 10:30:00": 1},
        {"gateway": "747327", "2024-02-21 10:30:00": 1},
        {"gateway": "747319", "2024-02-21 10:30:00": 1},
        {"gateway": "746667", "2024-02-21 10:30:00": 1},
        {"gateway": "746675", "2024-02-21 10:30:00": 1},
        {"gateway": "746679", "2024-02-21 10:30:00": 1},
        {"gateway": "747277", "2024-02-21 10:30:00": 1},
        {"gateway": "747333", "2024-02-21 10:30:00": 1},
        {"gateway": "747335", "2024-02-21 10:30:00": 1},
        {"gateway": "747339", "2024-02-21 10:30:00": 1},
        {"gateway": "747343", "2024-02-21 10:30:00": 1},
        {"gateway": "747317", "2024-02-21 10:30:00": 1},
        {"gateway": "747275", "2024-02-21 10:30:00": 1},
        {"gateway": "747315", "2024-02-21 10:30:00": 1},
        {"gateway": "747331", "2024-02-21 10:45:00": 1},
        {"gateway": "747337", "2024-02-21 10:45:00": 1},
        {"gateway": "747329", "2024-02-21 10:45:00": 1},
        {"gateway": "747341", "2024-02-21 10:45:00": 1},
        {"gateway": "747321", "2024-02-21 10:45:00": 1},
        {"gateway": "747323", "2024-02-21 10:45:00": 1},
        {"gateway": "747325", "2024-02-21 10:45:00": 1},
        {"gateway": "747327", "2024-02-21 10:45:00": 1},
        {"gateway": "747319", "2024-02-21 10:45:00": 1},
        {"gateway": "746667", "2024-02-21 10:45:00": 1},
        {"gateway": "746675", "2024-02-21 10:45:00": 1},
        {"gateway": "746679", "2024-02-21 10:45:00": 1},
        {"gateway": "747277", "2024-02-21 10:45:00": 1},
        {"gateway": "747333", "2024-02-21 10:45:00": 1},
        {"gateway": "747335", "2024-02-21 10:45:00": 1},
        {"gateway": "747339", "2024-02-21 10:45:00": 1},
        {"gateway": "747343", "2024-02-21 10:45:00": 1},
        {"gateway": "747317", "2024-02-21 10:45:00": 1},
        {"gateway": "747275", "2024-02-21 10:45:00": 1},
        {"gateway": "747315", "2024-02-21 10:45:00": 1},
        {"gateway": "747331", "2024-02-21 11:00:00": 1},
        {"gateway": "747337", "2024-02-21 11:00:00": 1},
        {"gateway": "747329", "2024-02-21 11:00:00": 1},
        {"gateway": "747341", "2024-02-21 11:00:00": 1},
        {"gateway": "747321", "2024-02-21 11:00:00": 1},
        {"gateway": "747323", "2024-02-21 11:00:00": 1},
        {"gateway": "747325", "2024-02-21 11:00:00": 1},
        {"gateway": "747327", "2024-02-21 11:00:00": 1},
        {"gateway": "747319", "2024-02-21 11:00:00": 1},
        {"gateway": "746667", "2024-02-21 11:00:00": 1},
        {"gateway": "746675", "2024-02-21 11:00:00": 1},
        {"gateway": "746679", "2024-02-21 11:00:00": 1},
        {"gateway": "747277", "2024-02-21 11:00:00": 1},
        {"gateway": "747333", "2024-02-21 11:00:00": 1},
        {"gateway": "747335", "2024-02-21 11:00:00": 1},
        {"gateway": "747339", "2024-02-21 11:00:00": 1},
        {"gateway": "747343", "2024-02-21 11:00:00": 1},
        {"gateway": "747317", "2024-02-21 11:00:00": 1},
        {"gateway": "747275", "2024-02-21 11:00:00": 1},
        {"gateway": "747315", "2024-02-21 11:00:00": 1},
    ]

    输出:
    [
        {"gateway": "747331", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "747337", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "747329", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "747341", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "747321", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "747323", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "747325", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "747327", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "747319", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "746667", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "746675", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "746679", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "747277", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "747333", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "747335", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "747339", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "747343", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "747317", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "747275", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
        {"gateway": "747315", "2024-02-21 10:30:00": 1, "2024-02-21 10:45:00": 1, "2024-02-21 11:00:00": 1},
    ]
    """

    result: defaultdict = defaultdict(lambda: defaultdict(int))

    for item in data:
        gateway = item["gateway"]
        for timestamp, value in item.items():
            if timestamp != "gateway":
                result[gateway][timestamp] += value

    result_list = [{"gateway": gateway, **timestamps} for gateway, timestamps in result.items()]
    return result_list
