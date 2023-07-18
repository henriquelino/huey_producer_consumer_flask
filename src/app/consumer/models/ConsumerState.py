import enum


class States(enum.Enum):
    stopped = 'stopped'
    running = 'running'


class CurrentState:

    def __init__(self, state: States = States.stopped) -> None:
        self.state = state


CONSUMER_STATE = CurrentState()
