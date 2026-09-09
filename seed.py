from app import app, db, Flight

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # 8 Flights
    f1 = Flight(flight_number='QR001', origin='DOH', destination='LHR', departure_time='08:00', arrival_time='13:00', price=500)
    f2 = Flight(flight_number='QR002', origin='DOH', destination='JFK', departure_time='10:00', arrival_time='17:00', price=900)
    f3 = Flight(flight_number='QR003', origin='LHR', destination='DOH', departure_time='09:00', arrival_time='17:00', price=550)
    f4 = Flight(flight_number='QR004', origin='LHR', destination='JFK', departure_time='11:00', arrival_time='15:00', price=700)
    f5 = Flight(flight_number='QR005', origin='JFK', destination='DOH', departure_time='18:00', arrival_time='23:00', price=850)
    f6 = Flight(flight_number='QR006', origin='JFK', destination='LHR', departure_time='12:00', arrival_time='16:00', price=600)
    f7 = Flight(flight_number='QR007', origin='DOH', destination='CDG', departure_time='07:00', arrival_time='12:00', price=450)
    f8 = Flight(flight_number='QR008', origin='CDG', destination='DOH', departure_time='14:00', arrival_time='19:00', price=480)
    
    db.session.add_all([f1, f2, f3, f4, f5, f6, f7, f8])
    db.session.commit()
    print("Database fully recreated with 8 flights!")
