import inspect

class Should:
    def __init__(self, actual_value):
        self.__actual_value = actual_value

    def should_equal(self, expected_value):
        if self.__actual_value != expected_value:
            raise AssertionError('%s does not equal %s' % (self.__actual_value, expected_value))

def should(description, function):
    return Phrase(description, lambda value: function(Should(value)), ())

class Result:
    def __init__(self, description, error, children=None):
        self.__description = description
        self.__message = error
        self.__children = children

    def description(self):
        return self.__description

    def passed(self):
        return self.__message == ''

    def message(self):
        return self.__message

    def children(self):
        return self.__children

class Phrase:
    @classmethod
    def make(self, obj):
        if type(obj) == type(()):
            return Phrase(*obj)
        else:
            return obj

    def __init__(self, description, function, children):
        self.__description = description
        self.__function = function
        self.__children = (Phrase.make(child) for child in children)

    def run(self, parent_output=None):
        passed = True
        numargs = len(inspect.getargspec(self.__function)[0])
        message = ''
        try:
            if numargs == 0:
                output = self.__function()
            else:
                output = self.__function(parent_output)
        except AssertionError as error:
            passed = False
            message = str(error)

        return Result(self.__description, message, [child.run(output) for child in self.__children])

class SpecsFor:
    def __init__(self, description):
        self.__description = description
        self.__children = []

    def add(self, description, function, *children):
        self.__children.append((description, function, children))

    def run(self):
        return Phrase(self.__description, lambda: None, self.__children).run()
