# Dollarify

A Complete Finance Overview in a single app.

## Installation

**Recommanded**: Create a virtual environnement (venv) for the project.

Install the build package:
> python3 -m pip install --upgrade build

Setup the develop mode:
> python3 -m pip install -e . 
> 
**or**

> python3 -m setup develop

Create a `config.ini` file at the root of the package folder (same level as `src/` folder). Add the following attributes inside:
```
[postgresql-database]
host=localhost
database=dollarify
user=db_username
password=pa$$w0rd
port=5432

[flask-dev-server]
port=8000
host=localhost
```

### Development Cycle

#### Building the project
Use the command:
> python3 -m build


#### Running the project

** Don't forget to activate the virtual environment. **

Use the command:
> dollarify [--production | -p] [--debug | -d]