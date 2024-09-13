from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_data.db'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50))
    distance1 = db.Column(db.Float)
    distance2 = db.Column(db.Float)
    distance3 = db.Column(db.Float)
    latitude = db.Column(db.String(50))
    longitude = db.Column(db.String(50))
    date = db.Column(db.String(50))

    def __repr__(self):
        return '<Data {}>'.format(self.timestamp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created.")

