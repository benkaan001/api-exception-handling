from flask import Flask, jsonify, abort
from create_db import create_database
from db import fetch_blogs, fetch_blog, NotAuthorizedError, NotFoundError
from utils.logging_decorator import log_exceptions,create_logger

app = Flask(__name__)

@app.route('/')
def say_hello():
    return 'Hello'

@app.route('/blogs')
def all_blogs():
    return jsonify(fetch_blogs())


@app.route('/blogs/<id>')
@log_exceptions(logger=create_logger('logs/version3_logs.log'))
def get_blog(id):
    try:
        return jsonify(fetch_blog(id))
    except NotFoundError:
        abort(404, description="Resource not found.")
    except NotAuthorizedError:
        abort(403, description="Access denied.")

if __name__ == "__main__":
    create_database()
    app.run()