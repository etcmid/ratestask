import os
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta

from api.services import ApiService

api = Blueprint('api', __name__)

# db_url = "postgresql://postgres:password@db:5432/mydatabase"
api_service = ApiService(os.environ['DATABASE_URL'])

# Define a route for getting rates


@api.route("/rates")
def get_rates():
    try:
        # Get query parameters from the request
        date_from_str = request.args.get("date_from")
        date_to_str = request.args.get("date_to")
        origin = request.args.get("origin")
        destination = request.args.get("destination")

        # Convert date strings to date objects
        date_from = datetime.strptime(date_from_str, "%Y-%m-%d").date()
        date_to = datetime.strptime(date_to_str, "%Y-%m-%d").date()

        # Get prices from the ApiService and return them as JSON
        prices = api_service.get_prices(
            date_from, date_to, origin, destination)
        return jsonify(prices), 200

    except ValueError:
        # Return a bad request status if the date format is incorrect
        return jsonify({"error": "Incorrect date format. Please use YYYY-MM-DD."}), 400

    except Exception as e:
        # Return an internal server error status for any other exceptions
        return jsonify({"error": str(e)}), 500
