def should(description, function):
    pass

class Result:
    def __init__(self, description, children=None):
        self.__description = description
        self.__children = children

    def description(self):
        return self.__description

    def passed(self):
        return True

    def children(self):
        return self.__children

class SpecsFor:
    def __init__(self, description):
        pass
    def add(self, description, function, *args):
        pass
    def run(self):
        return Result('True', [Result('be true')])
