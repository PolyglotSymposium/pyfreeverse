class ActualValue:
    def __init__(self, actual_value):
        self.__actual_value = actual_value

    def should(self, predicate):
        if predicate(self.__actual_value):
            return ''
        else:
            return 'Predicate not true of %s' % self.__actual_value

    def should_equal(self, expected_value):
        if self.__actual_value == expected_value:
            return ''
        else:
            return '%s does not equal %s' % (self.__actual_value, expected_value)

class Expect:
    def __init__(self, actual_value):
        self.__actual_value = ActualValue(actual_value)

    def __getattr__(self, name):
        if name.startswith('to'):
            return getattr(self.__actual_value, 'should' + name[2:])
        else:
            raise AttributeError

It = lambda: It
for method_name in dir(ActualValue):
    if method_name.startswith('should'):
        (lambda method_name:
            setattr(It, method_name,
                lambda expected:
                    lambda actual_value: getattr(actual_value, method_name)(expected))
        )(method_name)

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

_takesNoArgs = (lambda:
    lambda func: len(__import__("inspect").getargspec(func)[0]) == 0
)()


def _format_exception(exception):
    return '%s raised: %s' % (exception.__class__.__name__, exception)

class Verify:
    def __init__(self, description, function):
        self.__description = description
        self.__function = function

    def run(self, parent_output):
        try:
            if _takesNoArgs(self.__function):
                message = self.__function()
            else:
                message = self.__function(parent_output)
        except Exception as error:
            message = _format_exception(error)
        return Result(self.__description, message)

class Should:
    def __init__(self, description, function):
        self.__description = description
        self.__function = function

    def run(self, parent_output):
        try:
            message = self.__function(ActualValue(parent_output))
        except Exception as error:
            message = _format_exception(error)
        return Result('should ' + self.__description, message)

def make_phrase_from(obj):
    if type(obj) == type(()):
        if len(obj) == 2:
            return Verify(*obj)
        else:
            return Phrase(*obj)
    else:
        return obj

class Phrase:
    def __init__(self, description, function, children):
        self.__description = description
        self.__function = function
        self.__children = (make_phrase_from(child) for child in children)

    def __run_children(self, message, output):
        if message == '':
            return [child.run(output) for child in self.__children]
        else:
            return []

    def run(self, parent_output=None):
        message = ''
        output = None
        try:
            if callable(self.__function):
                if _takesNoArgs(self.__function):
                    output = self.__function()
                else:
                    output = self.__function(parent_output)
            else:
                output = self.__function
        except Exception as error:
            message = _format_exception(error)

        return Result(self.__description, message, self.__run_children(message, output))

class SpecsFor:
    def __init__(self, description):
        self.__description = description
        self.__children = []

    def add(self, description, function, *children):
        self.__children.append((description, function, children))

    def run(self):
        return Phrase(self.__description, lambda: None, self.__children).run()
