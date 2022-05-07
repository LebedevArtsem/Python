import inspect
from types import NoneType

from serializers.converter import Converter
from serializers.serializer import Serializer


class SerializerJson(Serializer):
    def dumps(self, obj, indent=0):
        rows = []
        if isinstance(obj, (float, int, str, bool, NoneType, bytes)):
            result = Converter.get_simple_object(obj)
            result = result[:-1]

        elif isinstance(obj, dict):
            rows.append('{')
            if not obj:
                rows[-1] = '{' + '}'
            else:
                row = Converter.get_dict_json(obj, indent)
                rows = rows + row
                rows[-1] = rows[-1][:-1]
            result = Converter.list_to_str(rows)
        elif isinstance(obj, (tuple, list, set)):
            rows.append('[')
            if not obj:
                rows[-1] = '[' + ']'
            else:
                row = Converter.get_list(obj, indent)
                rows = rows + row
                rows[-1] = rows[-1][:-1]
            result = Converter.list_to_str(rows)
        elif inspect.isfunction(obj):
            rows.append('{')
            temp = Converter.function_to_dict(obj)
            row = Converter.get_dict_json(temp, indent)
            rows += row
            rows[-1] = rows[-1][:-1]
            result = Converter.list_to_str(rows)
        elif inspect.ismethod(obj):
            rows.append('{')
            temp = Converter.function_to_dict(obj.__func__)
            row = Converter.get_dict_json(temp, indent)
            rows += row
            rows[-1] = rows[-1][:-1]
            result = Converter.list_to_str(rows)
        elif inspect.isclass(obj):
            rows.append('{')
            temp = Converter.class_to_dict(obj)
            row = Converter.get_dict_json(temp, indent)
            rows += row
            rows[-1] = rows[-1][:-1]
            result = Converter.list_to_str(rows)
        else:
            data = Converter.object_to_dict(obj)
            rows.append('{')
            row = Converter.get_dict_json(data, indent)
            rows = rows + row
            rows[-1] = rows[-1][:-1]
            result = Converter.list_to_str(rows)

        return result

    def loads(self, string):
        rows = string.split('\n')
        for i in range(len(rows)):
            rows[i] = rows[i].replace(" ", "").replace(",", "")
        if rows[0] == '[':
            data, temp = Converter.set_list(rows, 1)
        elif rows[0] == '{':
            data, temp = Converter.set_dict_json(rows, 1)
            if "__code__" in data:
                return Converter.dict_to_function(data)
            elif "__bases__" in data:
                return Converter.dict_to_class(data)
        else:
            data = Converter.set_simple_object(rows[0])
        return data
