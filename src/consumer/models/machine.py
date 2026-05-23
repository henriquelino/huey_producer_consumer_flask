from enum import Enum
from typing import Optional

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

    def __init__(self, initial_state: States = States.stopped):
        self.huey: Optional[Huey] = None
        self.consumer_config: dict = {}
        self.huey_consumer: Optional[HueyConsumer] = None

        self.machine = Machine(
            model=self,
            states=[s.value for s in self.States],
            initial=initial_state,
            auto_transitions=True,
        )
        self.machine.add_transition(trigger='start', source='stopped', dest='running', after='_on_start')
        self.machine.add_transition(trigger='stop', source='running', dest='stopped', after='_on_stop')

    def configure(self, huey: Huey, consumer_config: dict):
        # Wire huey and consumer options in after import time, since the singleton is
        # constructed before commons.config has been loaded by the consumer entry point.
        self.huey = huey
        self.consumer_config = consumer_config

    def _on_start(self):
        # Tests drive the endpoints without wiring huey, so the state transitions still
        # work but no real worker pool is spun up.
        if self.huey is None:
            return

        try:
            self.huey_consumer = self.huey.create_consumer(**self.consumer_config)
            self.huey_consumer.start()
        except ValueError as e:
            # huey installs signal handlers on start(), which only works on the main thread.
            # When start() is driven from a Flask request handler (worker thread), the consumer
            # still starts but signal-based shutdown won't work — surface as a warning instead
            # of silently swallowing.
            logger.warning(f"huey consumer started without signal handlers (not on main thread): {e}")

    def _on_stop(self):
        if self.huey_consumer is not None:
            self.huey_consumer.stop(graceful=True)
            self.huey_consumer = None


STATE_MACHINE = Consumer(initial_state=Consumer.States.stopped)
