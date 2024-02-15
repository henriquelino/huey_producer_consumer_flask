from enum import Enum

from huey import Huey
from huey.consumer import Consumer as HueyConsumer
from loguru import logger
from transitions import Machine


class Consumer(object):

    class States(str, Enum):
        stopped = 'stopped'
        running = 'running'

        def __str__(self):
            return self.value

        __repr__ = __str__

    huey_consumer: HueyConsumer = None

    def __init__(self, initial_state: States = States.running):

        self.initial = self.States.stopped
        self.machine = Machine(model=self, states=[s.value for s in self.States], initial=initial_state)

        self.machine.add_transition(trigger='start', source='stopped', dest='running')

        self.machine.add_transition(trigger='stop', source='running', dest='stopped')

    @classmethod
    def start_consumer(self, huey: Huey, config: dict):

        def inner():
            try:
                self.huey_consumer = huey.create_consumer(**config)
                self.huey_consumer.start()
            except ValueError as e:
                logger.debug(f"Error while starting consumer: '{e}'")
                # signal only works in main thread of the main interpreter
                # but even with this error the consumer starts, so I guess dont need to worry?
                pass

        return inner

    @classmethod
    def stop_consumer(self):
        if self.huey_consumer:
            self.huey_consumer.stop(graceful=True)


STATE_MACHINE = Consumer(initial_state=Consumer.States.running)
