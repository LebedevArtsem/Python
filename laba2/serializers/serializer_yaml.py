import yaml
from yaml.loader import FullLoader
from serializers.serializer import Serializer
from serializers.converter import Converter
from types import NoneType


class SerializerYaml(Serializer):
    def dumps(self, data, indent=0):
        dict_yaml = {}
        if not isinstance(data, (float, int, str, bool, NoneType, dict, list, tuple, set)):
            dict_yaml = Converter.get_dict_yaml(data)
            string = yaml.dump(dict_yaml)
        else:
            string = yaml.dump(data)
        return string

    def loads(self, string):
        data = yaml.load(string, Loader=FullLoader)
        if isinstance(data, dict):
            data = Converter.set_dict_yaml(data)
        return data
