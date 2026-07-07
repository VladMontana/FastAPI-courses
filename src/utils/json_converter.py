import orjson
from typing import Any

def to_json(value: Any) -> str:
    """
    Преобразует Python-объект в JSON-строку.

    Используется перед сохранением данных в Redis, потому что Redis хранит
    строки/байты, а не Python-объекты вроде list, dict, tuple и так далее.

    :param value: Любой JSON-сериализуемый Python-объект:
        dict, list, str, int, float, bool, None.
    :return: JSON-строка.
    """
    return orjson.dumps(value).decode("utf-8")
    

def from_json(value: str | None) -> Any | None:
    """
    Преобразует JSON-строку обратно в Python-объект.

    Используется после получения данных из Redis, чтобы вернуть строку JSON
    обратно в обычный Python-объект: dict, list, str, int и так далее.

    :param value: JSON-строка, bytes или None.
    :return: Python-объект после десериализации или None, если значение отсутствует.
    """
    if value is None:
        return None
    
    return orjson.loads(value)