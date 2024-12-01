from flask import Flask, render_template, redirect
from mongoengine import connect
from StaffService import staff_endpoints
from BookService import book_endpoints
from MemberService import member_endpoints
from ReservationService import reservation_endpoints

app = Flask(__name__)
app.register_blueprint(staff_endpoints)
app.register_blueprint(book_endpoints)
app.register_blueprint(member_endpoints)
app.register_blueprint(reservation_endpoints)

connect(host="mongodb://localhost:27017/library")

@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/home')
def home():  # put application's code here
    return redirect('/')



@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
