from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/hello')
def home():
    return "Goodbye from a Blueprint!"
