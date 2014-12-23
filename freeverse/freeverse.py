from .expectations import ActualValue

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
        if len(obj) == 1:
            if obj[0].__class__ == Should:
                return obj[0]
            else:
                obj = obj[0]
        if len(obj) == 2:
            return Verify(*obj)
        else:
            return Phrase(obj[0], obj[1], obj[2:])
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

class SpecFor:
    def __init__(self, description):
        self.__description = description
        self.__children = []

    def add(self, description, function, *children):
        self.__children.append((description, function, children))

    def run(self):
        return Phrase(self.__description, lambda: None, self.__children).run()

    def run_and_write_to(self, outputter):
        outputter.write(self.run())

class FlatOutput:
    def __init__(self, stream):
        self.__stream = stream;

    def __write_output(self, result, parent_description=None):
        if parent_description == None:
            description = result.description()
        else:
            description = '%s %s' % (parent_description, result.description())
        if result.children() == None:
            self.__stream.write('\t%s\n' % description)
        else:
            for child_result in result.children():
                self.__write_output(child_result, description)

    def write(self, results):
        self.__stream.write(results.description() + '\n')
        for result in results.children():
            self.__write_output(result)
