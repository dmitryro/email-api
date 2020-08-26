#################
#### imports ####
#################
from datetime import datetime
from flask import Blueprint, Flask, json, jsonify, render_template, request, url_for, make_response
from flask import current_app
from flask_api import status    # HTTP Status Codes
from werkzeug.local import LocalProxy
from .utils import process_email, process_customer_email



email_blueprint = Blueprint('email', __name__, template_folder='templates')

logger = LocalProxy(lambda: current_app.logger)

@email_blueprint.route("/send", methods=['POST'])
def send_email():
    try:
        data = request.json
        full_name = data.get("full_name", "")
        title = data.get("title", "")
        message = data.get("message", "")
        subject = data.get("subject", "")
        email = data.get("email", "")

        process_email(full_name=full_name, email=email, title=title,
                      subject=subject, message=message)

        process_customer_email(full_name=full_name, email=email, title=title,
                               subject=subject, message=message)

        result = {"result": "success"}
        return make_response(jsonify(result),  status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Failed saving site - {e}")
        result = {"result": "failure"}
        return make_response(jsonify(result), status.HTTP_500_INTERNAL_SERVER_ERROR)
