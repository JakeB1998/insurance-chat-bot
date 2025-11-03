import os

from flask import Flask, render_template, request, jsonify

from app.config.app_vars import LOGGER

from app.routes.main_routes import main_r
from app.routes.login_routes import login_r
from app.utils.bool_utils import to_bool

app = Flask(__name__)

app.secret_key = os.urandom(24)


app.register_blueprint(main_r)
app.register_blueprint(login_r)


@app.before_request
def log_request():
    LOGGER.info(f"Incoming Request: {request.method} {request.path} - {request.remote_addr}")
    if request.method == 'POST':
        try:
            LOGGER.info(f"Request JSON: {request.get_json()}")
        except Exception as e:
            LOGGER.warning(f"Could not parse JSON: {e}")


# Optionally, log responses too
@app.after_request
def log_response(response):
    LOGGER.info(f"Response Status: {response.status}")
    return response


if __name__ == '__main__':
    LOGGER.info("Starting app")

    expose = to_bool(os.environ.get("EXPOSE", False))
    threaded = to_bool(os.environ.get("THREADED", True))
    debug = to_bool(os.environ.get("DEBUG", False))
    kwargs = {}

    if expose:
        kwargs.update({"host": "0.0.0.0"})

    kwargs.update({"threaded": threaded, "debug": debug})
    app.run(**kwargs, processes=1)

