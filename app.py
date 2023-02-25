import json
import os
import sys
import traceback

import jwt
from dotenv import load_dotenv
from flask import Flask, request, Response
from machaao import Machaao

from generate_index import ExtDataIndex

load_dotenv()
app = Flask(__name__)

MESSENGERX_BASE_URL = os.environ.get("MESSENGERX_BASE_URL")
OPEN_AI_KEY = os.environ.get("OPENAI_API_KEY")

param_list = [MESSENGERX_BASE_URL, OPEN_AI_KEY]

for param in param_list:
    if param is None:
        raise Exception("Environment variables not set in .env file")


def exception_handler(exception, data=None):
    caller = sys._getframe(1).f_code.co_name
    print(f"{caller} function failed")
    if hasattr(exception, 'message'):
        print(exception.message)
    else:
        print("Unexpected error: ", sys.exc_info()[0])

    if data is not None:
        machaao = Machaao(data['api_token'], MESSENGERX_BASE_URL)

        payload = {
            "identifier": "BROADCAST_FB_QUICK_REPLIES",
            "users": [data['user_id']],
            "message": {
                "text": data['output_text'],
                "quick_replies": [{
                    "content_type": "text",
                    "payload": "Hi",
                    "title": "👋🏻 Hi"
                }]
            }
        }

        response = machaao.send_message(payload)
        return Response(
            mimetype="application/json",
            response=json.dumps({
                "error": True,
                "message": response.text
            }),
            status=400,
        )

    else:

        return Response(
            mimetype="application/json",
            response=json.dumps({
                "error": True,
                "message": "Server error occurred. Check logs for details"
            }),
            status=400,
        )


@app.route('/', methods=['GET'])
def index():
    return "ok"


def extract_data(api_token, req):
    messaging = None
    user_id = req.headers.get("machaao-user-id", None)
    raw = req.json["raw"]

    if raw != "":
        inp = jwt.decode(str(raw), api_token, algorithms=["HS512"])
        sub = inp.get("sub", None)
        if sub and type(sub) is dict:
            sub = json.dumps(sub)

        if sub:
            decoded = json.loads(sub)
            messaging = decoded.get("messaging", None)

    return {
        "user_id": user_id,
        "messaging": messaging
    }


@app.route('/machaao/hook', methods=['POST'])
def receive():
    _api_token = None
    _user_id = None
    try:
        _api_token = request.headers["bot-token"]
        _user_id = request.headers["machaao-user-id"]

        if not _api_token:
            return Response(
                mimetype="application/json",
                response=json.dumps({
                    "error": True,
                    "message": "Invalid Request, Check your token"
                }),
                status=400,
            )

        return incoming(request)

    except KeyError as k:
        traceback.print_exc(file=sys.stdout)
        exception_handler(k)
    except AttributeError as a:
        traceback.print_exc(file=sys.stdout)
        exception_handler(a)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        if _user_id and _api_token:
            data = dict()
            data['user_id'] = _user_id
            data['api_token'] = _api_token
            data['output_text'] = "Oops!! Our bot is currently unavailable"
            exception_handler(e, data)
        else:
            exception_handler(e)


def incoming(req):
    api_token = req.headers.get("bot-token", None)
    incoming_data = extract_data(api_token, req)
    print(f"incoming: {incoming_data}")

    machaao = Machaao(api_token, MESSENGERX_BASE_URL)
    messaging = incoming_data["messaging"]
    user_id = incoming_data["user_id"]
    message = messaging[0]["message_data"]["text"].lower()

    if message == "hi":
        output_text = "Hello!! I am an FAQ bot demonstrating the indexing performance of llama index on your External " \
                      "data source. Ask me an FAQ relevant to your data source"
    else:
        output_text = str(idx_obj.query(message)).strip()

    payload = {
        "identifier": "BROADCAST_FB_QUICK_REPLIES",
        "users": [user_id],
        "message": {
            "text": output_text,
            "quick_replies": [{
                "content_type": "text",
                "payload": "Hi",
                "title": "👋🏻 Hi"
            }]
        }
    }

    response = machaao.send_message(payload)
    output_payload = {
        "success": True,
        "message": response.text
    }

    return Response(
        mimetype="application/json",
        response=json.dumps(output_payload),
        status=200,
    )


if __name__ == '__main__':
    idx_obj = ExtDataIndex()
    app.run(debug=True)
