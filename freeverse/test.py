import inspect
import functools

class Result:
    def __init__(self, message):
        self.__message = message

    def passed(self):
        return self.__message == ''

    def message(self):
        return self.__message

class Step:
    @classmethod
    def runStep(cls, previous_step_result, step):
        return step.run(previous_step_result)

    def __init__(self, description, func):
        self.__description = description
        self.__execute_step = func

    def _numberOfArgs(self):
        return len(inspect.getargspec(self.__execute_step)[0])

    def description(self):
        return self.__description

    def run(self, previous_step_result=None):
        numberOfArgs = self._numberOfArgs()
        if numberOfArgs == 0:
            return self.__execute_step()
        if numberOfArgs == 1:
            return self.__execute_step(previous_step_result)
        else:
            return functools.partial(self.__execute_step, previous_step_result)

class Case:
    def __init__(self, steps):
        self.__steps = steps

    def _format_exception(self, exception):
        return '%s raised: %s' % (exception.__class__.__name__, exception)

    def run(self):
        try:
            message = functools.reduce(Step.runStep, self.__steps, None)
        except Exception as error:
            message = self._format_exception(error)
        return Result(message)

class Suite:
    def __init__(self, cases):
        self.__cases = cases

    def run(self):
        return [case.run() for case in self.__cases]

