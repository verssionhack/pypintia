# py_json2dataclass
Free your hands from typing char to parse json to python dataclass

# Usage

python3 parse_json2dataclass.py <json_file_path>:<dataclass_name> ...

parse_json2dataclass.py will process <json_file_path> and named the top of the json tree to dataclass_name


# Example

The contents of <json_file_path>:
{
    "stutent": {
        "name": "bob",
        "age": 1,
    }
}

The output will be write to stutent.py

```python3

@dataclass
class Student:
    name: str
    age: int

    def __init__(self, data: dict):
        name = data.get('name')
        age = data.get('age')

```
