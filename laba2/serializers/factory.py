from serializers.serializer_json import SerializerJson
from serializers.serializer_yaml import SerializerYaml
from serializers.serializer_toml import SerializerToml


class Fabric:

    @staticmethod
    def get_serializer(serializer_name):
        if serializer_name == "json":
            return SerializerJson()
        if serializer_name == "yaml":
            return SerializerYaml()
        if serializer_name == "toml":
            return SerializerToml()
