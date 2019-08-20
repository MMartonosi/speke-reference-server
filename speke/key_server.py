import logging

from flask import Flask, request
from oss2.exceptions import NoSuchKey

from key_cache import KeyCache
from key_generator import KeyGenerator
from key_server_common import ServerResponseBuilder

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


@app.route("/test", methods=["POST"])
def server_handler():
    try:
        body = request.data
        cache = KeyCache()
        generator = KeyGenerator()
        response = ServerResponseBuilder(body, cache, generator).get_response()
        return response
    except NoSuchKey as e:
        app.logger.error(e)
        return e.body, {"Content-Type": "text/xml"}
