class StateDispatcher(object):

    def __init__(self, state_attr='state'):
        self.registry = {}
        self._state_attr = state_attr

    def __get__(self, instance, owner):
        if instance is None:
            return self

        method = self.registry[getattr(instance, self._state_attr)]
        return method.__get__(instance, owner)

    def register(self, state):
        def decorator(method):
            self.registry[state] = method
            return method

        return decorator


class StateMachine(object):

    dispatcher = StateDispatcher()
    state = None

    @dispatcher.register('test')
    def test(self):
        print('Hello, World!', self.state)

    @dispatcher.register('working')
    def do_work(self):
        print('Working hard, or hardly working?', self.state)


"""
>>> sm = StateMachine()
>>> sm.state = 'test'
>>> sm.dispatcher()
Hello, World! test
>>> sm.state = 'working'
>>> sm.dispatcher()
Working hard, or hardly working? working
"""
