# Dollarify

## Installation
By default, database authentication informations are stored in the database.ini file at the root of the project.
### database.ini:
```
[postgresql]
host=localhost
database=dollarify-api
user=postgres
password=SecurePas$1
port=5432
```

## Website (GUI)
The root of the website (based on Flask) is located in the <kbd>dollarify/__init__.py/</kbd> file.
To start the web server, run the command 