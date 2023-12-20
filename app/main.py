import argparse
import logging
import os

from deploy import (
    create_deployment,
    delete_all_deployments,
    info_deployment,
    restart_machine,
)
from flask import Flask, Response, jsonify, render_template, request
from flask_simplelogin import SimpleLogin, login_required
from logger_config import l

app = Flask(__name__)

password_path = "./SIMPLELOGIN_PASSWORD"
password = ""

try:
    with open(password_path, "r") as file:
        password = file.read()
except FileNotFoundError:
    print(f"Error: File '{password_path}' not found.")
except Exception as e:
    print(f"Error: {e}")

# https://github.com/flask-extensions/Flask-SimpleLogin
app.config["SECRET_KEY"] = "something-secret"
app.config["SIMPLELOGIN_USERNAME"] = "vulnerabli"
app.config["SIMPLELOGIN_PASSWORD"] = password.strip()
SimpleLogin(app)


@app.route("/")
@login_required
def hello():
    # Run config and setup html file with table
    from app_config import setup_app

    data = setup_app()
    return render_template("main.html", data=data)


@app.route("/create", methods=["POST"])
@login_required
def create():
    try:
        if request.is_json:
            data = request.get_json()
            id = data.get("id")
            copies = data.get("copies")
        else:
            id = request.form.get("id")
            copies = request.form.get("copies")
        l.info(f"Generate {copies} copies for lab {id}")
        # Remember to check starting work directory!! run python3 ./main.py!
        yaml_directory = f"./deployments/lab{id}/"
        response = create_deployment(yaml_directory, int(copies), id)

        return jsonify(response)
    except Exception as e:
        l.error(f"create: {e}")
        return "Error while calling /create"


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    try:
        if request.is_json:
            data = request.get_json()
            id = data.get("id")
        else:
            id = request.form.get("id")
        l.info(f"Delete for id {id}")
        # Remember to check starting work directory!! run python3 ./main.py!
        yaml_directory = f"./deployments/lab{id}/"
        response = delete_all_deployments(yaml_directory)

        return jsonify(response)
    except Exception as e:
        l.error(f"delete: {e}")
        return "Error while calling /delete"


@app.route("/info", methods=["POST"])
@login_required
def info():
    try:
        if request.is_json:
            data = request.get_json()
            id = data.get("id")
            machines_id = data.get("machines_id")
        else:
            id = request.form.get("id")
            machines_id = data.get("machines_id")
        l.info(f"Info for id {id}")
        status = False
        try:
            pods_info, status, users = info_deployment(id)
            response = {"pods_info": pods_info, "status": status, "users": users}
        except ValueError:
            response = {
                "pods_info": "There is no running deployments or deployment is being generated.",
                "status": status,
            }

        return jsonify(response)
    except ValueError as e:
        l.error(f"value error in info: {e}")
        return "There is no running deployments or deployment is being generated."
    except Exception as e:
        l.error(f"info: {e}")
        return "Error while calling /info"


@app.route("/restart", methods=["POST"])
@login_required
def restart():
    try:
        if request.is_json:
            data = request.get_json()
            id = data.get("id")
            machine_id = data.get("machine_id")
        else:
            id = request.form.get("id")
            machine_id = data.get("machine_id")
        l.info(f"Restart for id {id} and user {machine_id}")
        response = restart_machine(id, machine_id)

        return jsonify(response)
    except Exception as e:
        l.error(f"restart: {e}")
        return "Error while calling /restart"


@app.route("/statusall", methods=["POST"])
@login_required
def status():
    try:
        if request.is_json:
            data = request.get_json()
            id = data.get("id")
        else:
            id = request.form.get("id")
        print(f"Checking status for id {id}")
        response = dict()
        try:
            pods_info, status, users = info_deployment(id)
            response = {"pods_info": pods_info, "status": status, "users": users}
            print("From statusall got", response, users)
        except Exception as e:
            l.info(f"statusall: got none machines for lab {id}")

        return jsonify(response)
    except Exception as e:
        l.error(f"statusall: {e}")
        return "Error while calling /statusall"


@app.route("/jscalls")
@login_required
def serve_js_calls():
    try:
        with open("./static/js/calls.js", "r") as js:
            js_code = js.read()

        response = Response(js_code, content_type="text/javascript")
    except Exception as e:
        l.error(f"serve_js_calls: {e}")

    return response


@app.route("/onload")
@login_required
def serve_onloadscript():
    try:
        with open("./static/js/onload.js", "r") as js:
            js_code = js.read()

        response = Response(js_code, content_type="text/javascript")
    except Exception as e:
        l.error(f"serve_onloadscript: {e}")

    return response


@app.route("/jsutils")
@login_required
def serve_js_utils():
    try:
        with open("./static/js/utils.js", "r") as js:
            js_code = js.read()

        response = Response(js_code, content_type="text/javascript")
    except Exception as e:
        l.error(f"serve_js_utils: {e}")

    return response


@app.route("/logout", methods=["GET"])
def logout():
    return hello()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--debug", type=bool, help="Run app with port 8080 and debug=True"
    )
    args = parser.parse_args()
    l.info(f"Running application in debug mode: {args.debug}")
    if args.debug:
        app.run(host="0.0.0.0", port=5001, debug=True)
    else:
        app.run(host="0.0.0.0", port=80, debug=False)
