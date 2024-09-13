from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_data.db'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(80), nullable=False)
    distance1 = db.Column(db.Float, nullable=False)
    distance2 = db.Column(db.Float, nullable=False)
    distance3 = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.String(80))
    longitude = db.Column(db.String(80))
    date = db.Column(db.String(80))

    def __repr__(self):
        return f'<Data {self.timestamp}>'

@app.route('/')
def index():
    data = Data.query.all()
    gps_data = [(d.latitude, d.longitude, d.timestamp) for d in data]
    return render_template('Index.html', data=data, gps_data=gps_data)

if __name__ == '__main__':
    app.run(debug=True)
