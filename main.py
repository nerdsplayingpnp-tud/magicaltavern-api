from flask import *
import json, time

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home_page():
    data_set = {"Page": "Home", "Message": "Loaded Homepage.", "Time": time.time()}
    return json.dumps(data_set)


@app.route("/user/", methods=["GET"])
def request_page():
    user_query = str(request.args.get("user"))  #  /user/?user=HASJK4AF_NAME

    data_set = {
        "Page": "Request",
        "Message": f"Request: {user_query}",
        "Time": time.time(),
    }
    return json.dumps(data_set)


if __name__ == "__main__":
    app.run(port=7777)
