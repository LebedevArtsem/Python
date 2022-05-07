import math


class TestFullClass():
    def __init__(self):
        self.creation = True
        self.age = 15
        self.weigth = 65
        self.name = "BB23A"
        self.list = [[11, 12], [12, [13, 14, [17, 16]]], [13, 14, 15]]


class TestFullClassWithMethods(TestFullClass):
    def bark(iz):
        if iz is None:
            print("ill")
        else:
            iz = 2
        return iz


test_int = 11
test_float = 12
test_str = "hello1"
test_bool = False
test_none = None
test_list = [12, [13, [14, 15]]]
test_dict = {"first": 1, "second": {"third": "3", "fourth": True}}
test_bytes = bytes(12)


def test_func(s=11):
    return math.pow(s, test_int)
