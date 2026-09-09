from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flights.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(10), nullable=False)
    origin = db.Column(db.String(3), nullable=False)
    destination = db.Column(db.String(3), nullable=False)
    departure_time = db.Column(db.String(20), nullable=False)
    arrival_time = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    bookings = db.relationship('Booking', backref='flight', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)

# --- ROUTES ---
from datetime import datetime

@app.route('/')
def index():
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', today=today)cp /storage/emulated/0/Download/app.py .cp /storage/emulated/0/Download/app.py .cp /storage/emulated/0/Download/app.py .

@app.route('/search', methods=['POST'])
def search():
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    passengers = request.form.get('passengers', default=1, type=int)
    flights = Flight.query.filter_by(origin=origin, destination=destination).all()
    return render_template('results.html', flights=flights, origin=origin, destination=destination, passengers=passengers)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/book/<int:flight_id>')
def book_flight(flight_id):
    if 'user_id' not in session:
        flash('Please login to book a flight.')
        return redirect(url_for('login'))
        
    flight = Flight.query.get_or_404(flight_id)
    booking = Booking(user_id=session['user_id'], flight_id=flight.id)
    db.session.add(booking)
    db.session.commit()
    
    flash(f'Successfully booked flight {flight.flight_number}!')
    return redirect(url_for('index'))

@app.route('/my-bookings')
def my_bookings():
    if 'user_id' not in session:
        flash('Please login to view your bookings.')
        return redirect(url_for('login'))
        
    user = User.query.get(session['user_id'])
    bookings = Booking.query.filter_by(user_id=user.id).all()
    
    return render_template('bookings.html', bookings=bookings, user=user)
    
@app.route('/cancel-booking/<int:booking_id>')
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    booking = Booking.query.get_or_404(booking_id)
    # Ensure the user can only delete their own bookings
    if booking.user_id == session['user_id']:
        db.session.delete(booking)
        db.session.commit()
        flash('Booking cancelled successfully.')
    else:
        flash('You cannot cancel this booking.')
        
    return redirect(url_for('my_bookings'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
