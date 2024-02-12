import enum


class CurrentState:

    class States(enum.Enum):
        stopped = 'stopped'
        running = 'running'


    def __init__(self, state: States = States.stopped) -> None:
        self.state = state


CONSUMER_STATE = CurrentState()
