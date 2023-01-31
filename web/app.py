"""
Austin Warren's Flask API.
"""

from flask import Flask, request, send_from_directory, abort
import configparser
import os

app = Flask(__name__)


@app.route("/<path:path>")
def pathCheck(path):
    #name = request.args.get("nameRequest")
    if os.path.exists("pages" + '/' + path):
            #with open(path)as f:
                #content = f.read()
        return send_from_directory("pages" + '/', path), 200

    elif("~" in path or ".." in path):
        abort(403)

    else:
        abort(404)

def parse_config(config_paths):
    config_path = None
    for f in config_paths:
        if os.path.isfile(f):
            config_path = f
            break

    if config_path is None:
        raise RuntimeError("Configuration file not found!")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

config = parse_config(["credentials.ini", "default.ini"])
#message = config["DEFAULT"]["message"]

#print(message)

@app.errorhandler(403)
def forbidden(e):
    return send_from_directory("pages/", "403.html"), 403

@app.errorhandler(404)
def notFound(e):
    return send_from_directory("pages/", "404.html"), 404


if __name__ == "__main__":
    app.run(debug=config["SERVER"]["DEBUG"], host ='0.0.0.0', port = config["SERVER"]["PORT"])
