from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for

from BookService import getAllBooks
from Collections.Collections import Member, Counter, Reservation

member_endpoints = Blueprint('member_endpoints', __name__, template_folder='templates')


@member_endpoints.route('/member-home')
def member_home():
    return render_template('member-home.html')

@member_endpoints.route('/member-dashboard')
def render_dashboard_for_member():
    member_id = request.args.get('member_id')
    my_reservations = list(Reservation.objects(member_id=member_id).order_by('-reservation_date'))
    latest_available_date = request.args.get('latest_available_date')
    is_book_reserved = str_to_bool(request.args.get('is_book_reserved'))
    is_book_available = str_to_bool(request.args.get('is_book_available'))
    member = Member.objects(member_id__exact=member_id).first()
    books = getAllBooks()
    return render_template('member-dashboard.html',
                           member=member,
                           books=books,
                           is_book_reserved=is_book_reserved,
                           is_book_available=is_book_available,
                           latest_available_date=latest_available_date,
                           my_reservations=my_reservations)


@member_endpoints.route("/member-validate", methods=['POST'])
def staff_validate():
    if request.method == 'POST':
        member_id = request.form.get('memberId')
        password = request.form.get('password')
        member = Member.objects(member_id__exact=member_id)
        if len(member) > 0:
            mem = member[0]
            if mem.password == password:
                return redirect(url_for('member_endpoints.render_dashboard_for_member',
                                        member_id=member_id,
                                        is_book_reserved=False,
                                        is_book_available=True))
            else:
                return render_template("member-home.html",
                                       isRegisteredMessage=False,
                                       is_login_error=True,
                                       doSignup=False)
        else:
            return render_template("member-home.html",
                                   isRegisteredMessage=False,
                                   is_login_error=True,
                                   doSignup=False)
    else:
        print("Please login")
    return render_template('staff-home.html')


@member_endpoints.route("/member-add", methods=['POST'])
def member_add():
    if request.method == 'POST' and request.form.get('registerEmail') is not None:
        members = Member.objects(email__exact=request.form.get('registerEmail'))
        if len(members) == 0:
            new_member_id = get_new_member_id()
            member = Member(
                member_id=new_member_id,
                name=request.form.get('registerName'),
                email=request.form.get('registerEmail'),
                contact_no=request.form.get('registerContactNo'),
                join_date=datetime.now(),
                password=request.form.get('registerPassword')
            )
            member.save()
            return render_template("member-home.html",
                                   isRegisteredMessage=True,
                                   is_login_error=False,
                                   doSignup=False,
                                   member_id=new_member_id)
        else:
            return render_template("member-home.html",
                                   isRegisteredMessage=False,
                                   is_login_error=False,
                                   doSignup=True,
                                   member_id=None)
    else:
        return render_template("member-home.html",
                               isRegisteredMessage=False,
                               is_login_error=False,
                               doSignup=False,
                               member_id=None)



@member_endpoints.route("/member-logout")
def student_logout():
    return redirect("/member-home")


def get_new_member_id():
    counter = Counter.objects(name="member_id_counter").first()
    if not counter:
        counter = Counter(name="member_id_counter", sequence_value=1000)
        counter.save()

    new_id = counter.increment()
    return new_id

def str_to_bool(value):
    if value == 'False':
        return False
    elif value == 'True':
        return True
    return True