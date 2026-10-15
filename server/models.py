"""
Database models for the Flask-SQLAlchemy Earthquake API.

Defines the SQLAlchemy database instance and models used to
store and retrieve historical earthquake data.
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Initialize SQLAlchemy metadata for database schema management
metadata = MetaData()

# Create the SQLAlchemy database instance
db = SQLAlchemy(metadata=metadata)

class Earthquake(db.Model):
    """
    Represents an earthquake record in the database.

    Maps earthquake information to the 'earthquakes' table
    using SQLAlchemy's Object-Relational Mapping (ORM).

    Attributes:
        id (int): Unique identifier and primary key.
        magnitude (float): Recorded magnitude of the earthquake.
        location (str): Geographic location of the earthquake.
        year (int): Year in which the earthquake occurred.
    """
    
    __tablename__ = 'earthquakes'

    id = db.Column(db.Integer, primary_key=True)
    magnitude = db.Column(db.Float)
    location = db.Column(db.String)
    year = db.Column(db.Integer)

    def __repr__(self):
        """
        Return a readable string representation of an earthquake.

        Includes the earthquake's ID, magnitude, location,
        and year for easier debugging and inspection.

        Returns:
            str: Formatted earthquake information.

        Example:
            <Earthquake 1, 9.5, Chile, 1960>
        """
        return f'<Earthquake {self.id}, {self.magnitude}, {self.location}, {self.year}>'