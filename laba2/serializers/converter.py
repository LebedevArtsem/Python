import base64
import inspect
import sys
from types import NoneType, CodeType, FunctionType


class Converter:
    @staticmethod
    def get_simple_object(value):
        if isinstance(value, bool):
            row = str(value).lower()
        elif isinstance(value, str):
            row = f"\"{value}\""
        elif isinstance(value, (int, float)):
            row = str(value)
        elif value is None:
            row = "null"
        elif isinstance(value, bytes):
            row = str(base64.b64encode(value))

        return row + ','

    @staticmethod
    def set_simple_object(string):
        char = string[0]
        if string.startswith('b'):
            string = string.replace('b', '')
            value = base64.b64decode(string)
        elif string[0] == '\"':
            value = string.replace('"', '')
        elif string == 'null':
            value = None
        elif string == 'true':
            value = True
        elif string == 'false':
            value = False
        elif string.find('.'):
            value = float(string)
        else:
            value = int(string)
        return value

    @staticmethod
    def list_to_str(arr):
        string = ''
        for row in arr:
            string = string + row + '\n'
        string = string[:-1]
        return string

    @staticmethod
    def get_list(data, indent):
        rows = []
        indent += 4
        for value in data:
            if isinstance(value, (float, int, str, bool, NoneType, bytes)):
                row = ' ' * indent + Converter.get_simple_object(value)
                rows.append(row)
            elif isinstance(value, dict):
                if not value:
                    rows.append(' ' * indent + "{" + "},")
                else:
                    rows.append(' ' * indent + "{")
                    row = Converter.get_dict_json(value, indent)
                    rows = rows + row
            elif isinstance(value, (list, tuple, set)):
                if not value:
                    rows.append(' ' * indent + "[" + "],")
                else:
                    rows.append(' ' * indent + "[")
                    row = Converter.get_list(value, indent)
                    rows = rows + row
            elif inspect.isclass(value):
                rows.append(' ' * indent + '{')
                temp = Converter.class_to_dict(value)
                row = Converter.get_dict_json(temp, indent)
                rows += row
            else:
                rows.append(' ' * indent + "{")
                temp = Converter.object_to_dict(value)
                row = Converter.get_dict_json(temp, indent)
                rows = rows + row
        indent -= 4
        rows[-1] = rows[-1][:-1]
        rows.append(' ' * indent + '],')
        return rows

    @staticmethod
    def get_dict_json(data, indent):
        rows = []
        indent += 4
        for key, value in data.items():
            row = ' ' * indent + f"\"{key}\": "
            if isinstance(value, (float, int, str, bool, NoneType, bytes)):
                row += Converter.get_simple_object(value)
                rows.append(row)
            elif isinstance(value, dict):
                if not value:
                    rows.append(row + "{" + "},")
                else:
                    rows.append(row + "{")
                    row = Converter.get_dict_json(value, indent)
                    rows = rows + row
            elif isinstance(value, (list, tuple, set)):
                if not value:
                    rows.append(row + "[" + "],")
                else:
                    rows.append(row + "[")
                    row = Converter.get_list(value, indent)
                    rows = rows + row
            elif inspect.isfunction(value):
                rows.append(row + '{')
                temp = Converter.function_to_dict(value)
                row = Converter.get_dict_json(temp, indent)
                rows = rows + row
            elif inspect.ismethod(value):
                rows.append(row + '{')
                temp = Converter.function_to_dict(value.__func__)
                row = Converter.get_dict_json(temp, indent)
                rows = rows + row
            elif inspect.isclass(value):
                rows.append(row + '{')
                temp = Converter.class_to_dict(value)
                row = Converter.get_dict_json(temp, indent)
                rows += row
            else:
                rows.append(row + "{")
                temp = Converter.object_to_dict(value)
                row = Converter.get_dict_json(temp, indent)
                rows = rows + row
        indent -= 4
        rows[-1] = rows[-1][:-1]
        rows.append(' ' * indent + '},')
        return rows

    @staticmethod
    def set_dict_json(rows, index):
        dict_values = {}
        for _ in rows:
            if rows[index] == '}':
                return dict_values, index + 1
            items = rows[index].split(":")
            if len(items) > 1:
                for i in range(2, len(items)):
                    items[1] += items[i]
            key = items[0].replace("\"", "")
            if items[1] == '{' + '}':
                dict_values[key] = {}
                index += 1
            elif items[1] == '[]':
                dict_values[key] = []
                index += 1
            elif items[1].startswith("["):
                value, index = Converter.set_list(rows, index + 1)
                dict_values[key] = value
            elif items[1].startswith("{"):
                value, index = Converter.set_dict_json(rows, index + 1)
                dict_values[key] = value
            else:
                dict_values[key] = Converter.set_simple_object(items[1])
                index += 1

    @staticmethod
    def get_dict_yaml(data):
        dict_values = {}
        temp_list = []
        if inspect.isfunction(data):
            dict_values = Converter.function_to_dict(data)
        elif inspect.ismethod(data):
            dict_values = Converter.function_to_dict(data.__func__)
        elif inspect.isclass(data):
            dict_values = Converter.class_to_dict(data)
            for name, value in dict_values["__dict__"].items():
                dict_values["__dict__"][name] = Converter.get_dict_yaml(value)
            for value in dict_values["__bases__"]:
                temp_list.append(Converter.get_dict_yaml(value))
            dict_values["__bases__"] = temp_list
        elif isinstance(data, (int, float, str, NoneType, bool, dict, tuple, list, set, bytes)):
            return data
        else:
            dict_values = Converter.object_to_dict(data)
            for key, value in dict_values.items():
                dict_values[key] = Converter.get_dict_yaml(value)
        return dict_values

    @staticmethod
    def set_dict_yaml(data):
        if "__code__" in data:
            data = Converter.dict_to_function(data)
        elif "__bases__" in data:
            data = Converter.dict_to_class(data)
        else:
            for key, value in data.items():
                if isinstance(value, dict):
                    data[key] = Converter.set_dict_yaml(value)
        return data

    @staticmethod
    def get_dict_toml(data):
        dict_values = {}
        temp_list = []
        if inspect.isfunction(data):
            dict_values = Converter.function_to_dict(data)
        elif inspect.ismethod(data):
            dict_values = Converter.function_to_dict(data.__func__)
        elif inspect.isclass(data):
            dict_values = Converter.class_to_dict(data)
            for name, value in dict_values["__dict__"].items():
                dict_values["__dict__"][name] = Converter.get_dict_toml(value)
            for value in dict_values["__bases__"]:
                temp_list.append(Converter.get_dict_toml(value))
            dict_values["__bases__"] = temp_list
        elif isinstance(data, (int, float, str, NoneType, bool, tuple, list, set, bytes)):
            return data
        else:
            dict_values = Converter.object_to_dict(data)
            for key, value in dict_values.items():
                dict_values[key] = Converter.get_dict_toml(value)
        return dict_values

    @staticmethod
    def set_dict_toml(data):
        if len(data) == 1 and "value" in data:
            return data["value"]
        if "__code__" in data:
            data = Converter.dict_to_function(data)
        elif "__bases__" in data:
            data = Converter.dict_to_class(data)

        else:
            for key, value in data.items():
                if isinstance(value, dict):
                    data[key] = Converter.set_dict_toml(value)
        return data

    @staticmethod
    def set_list(rows, index):
        list_values = []
        for _ in rows:
            if rows[index] == '{' + '}':
                list_values.append({})
                index += 1
            if rows[index] == '[]':
                list_values.append([])
                index += 1
            elif rows[index].startswith('['):
                result, index = Converter.set_list(rows, index + 1)
                list_values.append(result)
            elif rows[index].startswith('{'):
                result, index = Converter.set_dict_json(rows, index + 1)
                list_values.append(result)
            elif rows[index] == ']':
                return list_values, index + 1
            else:
                list_values.append(Converter.set_simple_object(rows[index]))
                index += 1

    @staticmethod
    def class_to_dict(obj):
        class_values = {}
        bases = []
        dict_values = {}
        for name, value in inspect.getmembers(obj):
            if not name.startswith("__"):
                dict_values[name] = value
            elif name == "__init__":
                dict_values["__init__"] = value
        class_values["__dict__"] = dict_values
        class_values["__name__"] = obj.__name__
        mro = inspect.getmro(obj)
        for i in range(1, len(mro) - 1):
            bases.append(mro[i])
        class_values["__bases__"] = bases
        return class_values

    @staticmethod
    def object_to_dict(obj):
        dict_values = {}
        for name, value in inspect.getmembers(obj):
            if not name.startswith("__"):
                dict_values[name] = value
        return dict_values

    @staticmethod
    def function_to_dict(func):  # no globals
        function_members = {}
        function_code = {}
        function_globals = {}

        for key, value in inspect.getmembers(func):
            if key == "__code__" or key == "__name__" or key == "__defaults__" or key == "__globals__":
                function_members[key] = value
        for key, value in inspect.getmembers(function_members["__code__"]):
            if (not key.startswith("_") and key != 'co_linetable'
                    and isinstance(value, (int, float, str, bool, NoneType, tuple, dict, list, bytes, set))):
                function_code[key] = value

        if function_members["__defaults__"] == None:
            function_members["__defaults__"] = []

        for elem in function_code["co_names"]:
            if elem in function_members["__globals__"]:
                value = function_members["__globals__"][elem]
            else:
                continue

            if elem == function_members["__name__"]:
                function_globals[elem] = elem

            elif isinstance(value, (int, float, bool, bytes, str, NoneType, dict, list, tuple, set)):
                function_globals[elem] = value

            elif inspect.ismodule(value):
                function_globals[value.__name__] = "__module__"

            elif inspect.isclass(value):
                function_globals[elem] = Converter.class_to_dict(value)

            elif inspect.isfunction(value):
                function_globals[elem] = Converter.function_to_dict(value)

            elif inspect.ismethod(value):
                function_globals[elem] = Converter.function_to_dict(value.__func__)

            else:
                function_globals[elem] = Converter.object_to_dict(value)

        function_members["__code__"] = function_code
        function_members["__globals__"] = function_globals
        return function_members

    @staticmethod
    def dict_to_function(func_values):
        if sys.version_info.minor == 10:
            func_code = {"co_argcount": None, "co_posonlyargcount": None, "co_kwonlyargcount": None, "co_nlocals": None,
                         "co_stacksize": None, "co_flags": None, "co_code": None, "co_consts": None, "co_names": None,
                         "co_varnames": None, "co_filename": None, "co_name": None, "co_firstlineno": None,
                         "co_lnotab": None, "co_freevars": (), "co_cellvars": ()}
        else:
            func_code = {"co_argcount": None, "co_posonlyargcount": None, "co_kwonlyargcount": None, "co_nlocals": None,
                         "co_stacksize": None, "co_flags": None, "co_code": None, "co_consts": None, "co_names": None,
                         "co_varnames": None, "co_filename": None, "co_name": None, "co_qualname": None,
                         "co_firstlineno": None, "co_endlinetable": None, "co_columntable": None,
                         "co_exceptiontable": None,
                         "co_lnotab": None, "co_freevars": (), "co_cellvars": ()}
        for key, value in func_values['__code__'].items():
            if isinstance(value, list):
                if (key == "co_code" or key == "co_endlinetable" or key == "co_columntable" or
                        key == "co_exceptiontable" or key == "co_lnotab"):
                    value = bytes(value)
                else:
                    value = tuple(value)
            func_code[key] = value

        for key, value in func_values['__globals__'].items():
            if value == func_values['__name__']:
                continue

            elif value == "__module__":
                func_values["__globals__"][key] = __import__(key)

            if isinstance(value, dict):
                for name in value.keys():

                    if name == "__bases__":
                        func_values['__globals__'][key] = Converter.dict_to_class(value)

                    if name == "__code__":
                        func_values["__globals__"][key] = Converter.dict_to_function(value)

        code_list = [value for key, value in func_code.items()]
        func_values['__globals__']['__builtins__'] = __builtins__
        code = CodeType(*code_list)
        func = FunctionType(code, func_values['__globals__'], func_values['__name__'],
                            tuple(func_values['__defaults__']))
        return func

    @staticmethod
    def dict_to_class(class_values):
        bases = []
        for key, value in class_values["__dict__"].items():
            if "__code__" in value:
                class_values["__dict__"][key] = Converter.dict_to_function(value)
        for value in class_values["__bases__"]:
            bases.append(Converter.dict_to_class(value))

        return type(class_values["__name__"], tuple(bases), class_values["__dict__"])
