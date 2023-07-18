## How to develop
This project is a template and uses [huey](https://huey.readthedocs.io) for handling tasks. I've created this template to use in some projects and decided to publish it here as I haven't found much about huey when I started using it.

New tasks can be created under [commons/tasks](/src/app/commons/tasks) directory, the task should be imported to producer to generate tasks.

After creating your code, run `tox`* which is already configured to lint and format your code, then run any tests. Fix anything if needed, that's it

\* If you need to install tox, or don't know what it is, [take a look here](https://tox.wiki)

## How to configure:
Use the config file located at [config.yaml](/src/app/config.yaml)

## How to execute:
Commands should be executed at git root directory!
### producer

Change directory to producer `cd src/app/producer` then execute `python main.py`

This will create some tasks in sqlite db, consumer will proccess them.


### consumer

Change directory to consumer with `cd src/app/consumer` then execute `python main.py`

Consumer will start an flask server on port 5000 (default),  [open it](127.0.0.1:5000) on your browser then click on `Start`, you should see on the terminal:

```
The following commands are available:
+ consumer.tasks.example.open_an_url
```

This consumer depends on chromedriver for tasks, so it should automatically download/update chromedriver then process any created task.
