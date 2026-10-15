# server/app.py
#!/usr/bin/env python3

"""
Flask application for the Earthquake Management API.

Provides RESTful endpoints for retrieving historical earthquake
records from a SQLite database using Flask-SQLAlchemy.

Supported functionality:
    - Retrieve an earthquake by its unique ID.
    - Filter earthquakes by a minimum magnitude.
    - Accept integer and floating-point magnitude values.
    - Return structured JSON responses with appropriate HTTP
      status codes.
"""

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure JSON output formatting
app.json.compact = False

# Initialize database migration support and connect SQLAlchemy
migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    """
    Return a welcome message for the API.

    Returns:
        Response: JSON welcome message with HTTP status 200.
    """
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    """
    Retrieve an earthquake record by its unique ID.

    Queries the database for an earthquake matching the
    provided ID and returns its attributes as JSON.

    Args:
        id (int): Unique identifier of the requested earthquake.

    Returns:
        Response:
            200: JSON containing the earthquake's ID, magnitude,
                 location, and year.
            404: JSON error message if no matching record exists.
    """

    # Query the database for the requested earthquake
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()

    if earthquake:
        # Build the JSON response for a matching record
        body ={
            'id': earthquake.id,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location,
            'year': earthquake.year
        }
        status = 200

    else:
        # Return an error message when no matching record exists
        body = {'message': f"Earthquake {id} not found."}
        status = 404

    # Return the response with the appropriate HTTP status
    return make_response(body, status)

@app.route('/earthquakes/magnitude/<int:magnitude>')
@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_by_magnitude(magnitude):
    """
    Retrieve earthquakes meeting a minimum magnitude threshold.

    Queries the database for all earthquakes with a magnitude
    greater than or equal to the requested value.

    Supports BOTH integer and floating-point URL parameters.

    Args:
        magnitude (int | float): Minimum earthquake magnitude
            to include in the results.

    Returns:
        Response:
            200: JSON containing:
                - count (int): Number of matching earthquakes.
                - quakes (list): List of matching earthquake
                  records, each containing ID, magnitude,
                  location, and year.

            If no earthquakes match, returns an empty list
            and a count of zero with HTTP status 200.
    """

    # Initialize a list to store matching earthquake records
    earthquakes = []

    # Query earthquakes with magnitudes at or above the threshold
    for earthquake in Earthquake.query.filter(
        Earthquake.magnitude>=magnitude
    ).all():

        # Convert each SQLAlchemy object into a JSON-compatible dictionary
        earthquake_dict = {
            'id': earthquake.id,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location,
            'year': earthquake.year,
        }

        # Add the earthquake dictionary to the results list
        earthquakes.append(earthquake_dict)

    # Construct the response with the total count and matching records
    body = {
        'count': len(earthquakes),
        'quakes': earthquakes
    }

    return make_response(body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
