"""
Account Service

This microservice handles the lifecycle of Accounts

Paths:
------
GET  /               - Returns service information
POST /accounts       - Creates a new Account
GET  /accounts       - Lists all Accounts
GET  /accounts/{id}  - Reads an Account
PUT  /accounts/{id}  - Updates an Account
DELETE /accounts/{id} - Deletes an Account
"""
from flask import Blueprint, jsonify, request, url_for, abort, make_response
from service.models import Account, DataValidationError

bp = Blueprint("accounts", __name__)


############################################################
# GET INDEX
############################################################
@bp.route("/", methods=["GET"])
def index():
    """Root URL response with information about the service"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            paths=url_for("accounts.list_accounts", _external=True),
        ),
        200,
    )


############################################################
# CREATE A NEW ACCOUNT
############################################################
@bp.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based on the data in the body
    """
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    location_url = url_for(
        "accounts.get_accounts", account_id=account.id, _external=True
    )
    return make_response(jsonify(message), 201, {"Location": location_url})


############################################################
# LIST ALL ACCOUNTS
############################################################
@bp.route("/accounts", methods=["GET"])
def list_accounts():
    """Returns a list of all Accounts"""
    accounts = Account.all()
    account_list = [account.serialize() for account in accounts]
    return make_response(jsonify(account_list), 200)


############################################################
# READ AN ACCOUNT
############################################################
@bp.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """
    Reads an Account
    This endpoint will read an Account based on the account_id that is requested
    """
    account = Account.find(account_id)
    if not account:
        abort(404, f"Account with id [{account_id}] could not be found.")
    return make_response(jsonify(account.serialize()), 200)


############################################################
# UPDATE AN EXISTING ACCOUNT
############################################################
@bp.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """
    Updates an Account
    This endpoint will update an Account based on the posted data
    """
    account = Account.find(account_id)
    if not account:
        abort(404, f"Account with id [{account_id}] could not be found.")
    account.deserialize(request.get_json())
    account.update()
    return make_response(jsonify(account.serialize()), 200)


############################################################
# DELETE AN ACCOUNT
############################################################
@bp.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """
    Deletes an Account
    This endpoint will delete an Account based on the account_id that is requested
    """
    account = Account.find(account_id)
    if account:
        account.delete()
    return make_response("", 204)


############################################################
# ERROR HANDLERS
############################################################
@bp.app_errorhandler(DataValidationError)
def request_validation_error(error):
    """Handles data validation errors with a 400 Bad Request"""
    return make_response(
        jsonify(status=400, error="Bad Request", message=str(error)), 400
    )


@bp.app_errorhandler(404)
def not_found(error):
    """Handles resources that cannot be found with a 404 Not Found"""
    return make_response(
        jsonify(status=404, error="Not Found", message=str(error)), 404
    )


@bp.app_errorhandler(405)
def method_not_supported(error):
    """Handles bad method calls with a 405 Method Not Allowed"""
    return make_response(
        jsonify(status=405, error="Method not Allowed", message=str(error)), 405
    )


@bp.app_errorhandler(415)
def mediatype_not_supported(error):
    """Handles unsupported media requests with a 415 Unsupported Media Type"""
    return make_response(
        jsonify(status=415, error="Unsupported media type", message=str(error)), 415
    )


############################################################
# UTILITY FUNCTIONS
############################################################
def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type", "")
    if content_type != media_type:
        abort(415, f"Content-Type must be {media_type}")
