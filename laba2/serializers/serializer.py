from abc import abstractmethod, ABC


class Serializer(ABC):

    def dump(self, obj, fp):
        with open(fp, "w") as file:
            file.write(self.dumps(obj))

    @abstractmethod
    def dumps(self, obj, indent=0):
        pass

    def load(self, fp):
        with open(fp, "w") as file:
            return self.loads(file.read())

    @abstractmethod
    def loads(self, s):
        pass
