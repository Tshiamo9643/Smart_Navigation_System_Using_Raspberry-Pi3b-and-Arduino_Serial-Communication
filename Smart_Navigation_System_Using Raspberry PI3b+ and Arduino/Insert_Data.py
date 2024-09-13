from SDNS_App import db, Data

sample_data = [
    Data(timestamp='2024-07-01 12:00:00', distance1=38.0, distance2=35.0, distance3=40.0, latitude='-25.74486', longitude='28.18783', date='07/01/2024'),
    Data(timestamp='2024-07-01 12:05:00', distance1=40.0, distance2=30.0, distance3=45.0, latitude='36.1699', longitude='-115.1398', date='07/01/2024')
]

if __name__ == '__main__':
    from SDNS_App import app  # Import the app context
    with app.app_context():
        db.session.add_all(sample_data)
        db.session.commit()
        print("Sample data inserted.")
