## How to develop
This project is a template and uses [huey](https://huey.readthedocs.io) for handling tasks. I've created this template to use in some projects and decided to publish it here as I haven't found much about huey when I started using it.

New tasks can be created under [commons/tasks](/src/commons/tasks) directory, the task should be imported to producer to generate tasks.

After creating your code, run `tox`* which is already configured to lint and format your code, then run any tests. Fix anything if needed, that's it
Use `tox l` to view all available environments, then run one using `tox -e <env_name>`

\* If you don't know what it is, [take a look here](https://tox.wiki). It will be installed when you run `pip install -r requirements.txt`

## How to configure:
Use the config file located at [config.yaml](/src/config.yaml)

## How to execute:
Commands should be executed at git root directory, where `build_scripts`, `src` and `tests` folders are.

Changing directory to either producer/consumer will help as paths that use dot notation will begin from the folder that you changed into, example:  
`cd src/producer` then run `main.py` either on vscode or terminal,  
This will cause parsing of `config.yaml` to handle dot path as the current folder (`src/producer`), and double dot as upper folder (`src`)  
This is not a big issue but can led to unexpected things, if you don't cd and run from git root the `task.db` will be created here instead of being in `src`  

### producer
Change directory to producer `cd src/producer` then execute `python main.py`

This will create some tasks in sqlite db, consumer will process them.

### consumer
Change directory to consumer with `cd src/consumer` then execute `python main.py`

Consumer will start an flask server on port 5000 (default), [open it](127.0.0.1:5050) on your browser then click on `Start`, you should see on the terminal:

```
The following commands are available:
+ consumer.tasks.example.open_an_url
```

This consumer depends on chromedriver for tasks, so it should automatically download/update chromedriver then process any created task.

## Testing
There are some example tests in [tests](/tests) folder in git root, as our producer don't have any relevant code, there are tests only for consumer flask endpoints and tasks.
The tests are run using `tox` command, every environment runs all tests.

### coverage
When using `tox` to test, coverage report are generated as well, this can be served using:
`python -m http.server -d htmlcov`
in project root, then [open it in your browser](127.0.0.1:8000)

## Builds
The current code was tested on Windows 11 and Python 3.8, using `tox -e build_producer_consumer_exe` will use `build_scripts` to to generate two .exe files in the deploy folder using pyarmor. 

## Docker run
Run using `docker compose up -d --build`, then on terminal run `docker ps` to view running images:
```terminal
CONTAINER ID   IMAGE                                   COMMAND                  CREATED         STATUS                 PORTS                     NAMES
2627969d19d5   huey_producer_consumer_flask-consumer   "python app/main.py"     3 minutes ago   Up 3 minutes           0.0.0.0:50000->5000/tcp   huey_producer_consumer_flask-consumer-1

```
as producer dies rather quickly its normal to have only the consumer running