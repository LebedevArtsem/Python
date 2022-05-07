from unittest import TestCase, main

from serializers.serializer_yaml import SerializerYaml
from serializers.converter import Converter

from test_value import TestFullClass, TestFullClassWithMethods, test_int, test_bytes, \
    test_float, test_bool, test_str, test_none, test_dict, test_list

test_fullclass = TestFullClass()
test_fullclass_methods = TestFullClassWithMethods()


class SerializerYamlTest(TestCase):
    def setUp(self):
        self.ser_yaml = SerializerYaml()

    def test_get_value(self):
        self.assertEqual(test_int, self.ser_yaml.loads(self.ser_yaml.dumps(test_int)))

        self.assertEqual(test_float, self.ser_yaml.loads(self.ser_yaml.dumps(test_float)))

        self.assertEqual(test_bool, self.ser_yaml.loads(self.ser_yaml.dumps(test_bool)))

        self.assertEqual(test_str, self.ser_yaml.loads(self.ser_yaml.dumps(test_str)))

        self.assertEqual(test_none, self.ser_yaml.loads(self.ser_yaml.dumps(test_none)))

        self.assertEqual(test_dict, self.ser_yaml.loads(self.ser_yaml.dumps(test_dict)))

        self.assertEqual(test_list, self.ser_yaml.loads(self.ser_yaml.dumps(test_list)))

        self.assertEqual(test_bytes, self.ser_yaml.loads(self.ser_yaml.dumps(test_bytes)))

        self.assertEqual(Converter.object_to_dict(test_fullclass),
                         self.ser_yaml.loads(self.ser_yaml.dumps(test_fullclass)))

        # self.assertEqual(test_func(), self.ser_json.loads(self.ser_json.dumps(test_func))())

        # self.assertEqual(test_func(51), self.ser_json.loads(self.ser_json.dumps(test_func))(51))

        # self.assertEqual(Converter.object_to_dict(test_fullclass), Converter.object_to_dict(
        # self.ser_json.loads(self.ser_json.dumps(TestFullClass))()))


if __name__ == "__main__":
    main()
