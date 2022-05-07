import re

import toml
import tomli
import base64
from types import NoneType

from serializers.converter import Converter
from serializers.serializer import Serializer


class SerializerToml(Serializer):
    def dumps(self, data, indent=0):
        dict_toml = {}
        if isinstance(data, (float, int, str, bool, list, tuple, set)):
            dict_toml["value"] = data
            string = toml.dumps(dict_toml)
        elif isinstance(data, NoneType):
            string = "value = null"
        elif isinstance(data, bytes):
            string = "value = "
            string += str(base64.b64encode(data))
        elif isinstance(data, dict):
            string = toml.dumps(data)
        else:
            dict_toml = Converter.get_dict_toml(data)
            string = toml.dumps(dict_toml)
        return string

    def loads(self, string):
        if string == "value = null":
            data = None
        elif re.search("value = b", string):
            items = string.split("=")
            items[1] = re.sub(r'[ b]', '', items[1])
            data = base64.b64decode(items[1])
        else:
            data = tomli.loads(string)
            data = Converter.set_dict_toml(data)
        return data
