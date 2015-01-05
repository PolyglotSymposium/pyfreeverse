from .expectations import ActualValue
from .test import Step

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

def _format_exception(exception):
    return '%s raised: %s' % (exception.__class__.__name__, exception)

class Verify:
    def __init__(self, description, function):
        self.__description = description
        self.__function = function

    def as_test_step(self):
        return Step(self.__description, self.__function)

    def run(self, parent_output):
        testStep = self.as_test_step()
        try:
            message = testStep.run(parent_output)
        except Exception as error:
            message = _format_exception(error)
        return Result(testStep.description(), message)

class Should:
    def __init__(self, description, function):
        self.__description = description
        self.__function = function

    def as_test_step(self):
        exec_step = lambda prev_result: self.__function(ActualValue(prev_result))
        return Step('should ' + self.__description, exec_step)

    def run(self, parent_output):
        testStep = self.as_test_step()
        try:
            message = testStep.run(parent_output)
        except Exception as error:
            message = _format_exception(error)
        return Result(testStep.description(), message)

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

    def as_test_step(self):
        return Step(self.__description,
                         self.__function if callable(self.__function) else lambda: self.__function)

    def __run_children(self, message, output):
        if message == '':
            return [child.run(output) for child in self.__children]
        else:
            return []

    def as_test_cases(self):
        return self

    def run(self, parent_output=None):
        message = ''
        output = None
        testStep = self.as_test_step()
        try:
            output = testStep.run(parent_output)
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
        tests = Phrase(self.__description, None, self.__children).as_test_cases()
        return tests.run()

    def run_and_write_to(self, outputter):
        outputter.write(self.run())

class FlatOutput:
    def __init__(self, stream):
        self.__stream = stream;

    def __write_output(self, result, parent_description=None):
        if parent_description == None:
            description = result.description()
        else:
            description = u'%s %s' % (parent_description, result.description())
        if result.children() == None:
            self.__stream.write(u'\t%s\n' % description)
        else:
            for child_result in result.children():
                self.__write_output(child_result, description)

    def write(self, results):
        self.__stream.write(results.description() + u'\n')
        for result in results.children():
            self.__write_output(result)
