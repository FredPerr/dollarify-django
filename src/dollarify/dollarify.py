from flask import Flask


app = None

def create_app():
    return Flask("dollarify")
