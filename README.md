# Dollarify

Track investments, expenses and income in a single Web app.

## Installation

Create a virtual environnement (venv) for the project and activate it.

Install the build package:
> pip install -r requirements.txt

**Add FontAwesome 6 folder content in project root as 'footawesome/' folder.**

Setup secret key with env variable:
ALPHA_VANTAGE_API_KEY

Setup a postgresql db for development with env variables:
DB_NAME & DB_PASSWORD

Setup an Alpha Vantage API Key to retrieve stock data:
ALPHA_VANTAGE_API_KEY


for STMP server, setup env variables:
EMAIL_HOST_USER & EMAIL_HOST_PASSWORD



#### Running the project

Use the command:
> python manage.py runserver

## TODO:
- Get data on stock.
- Trade view with more indicators
- Trade list loading

- Set Income Source List for each user (or combine to Income Account directly)

@ Add the expenses option.
@ Add crypto trading option.
