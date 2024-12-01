from flask import Blueprint, render_template, request, redirect
from Collections.Collections import Staff, Counter

staff_endpoints = Blueprint('staff_endpoints', __name__,
                              template_folder='templates')


@staff_endpoints.route("/staff-home")
def staff_home():
    return render_template('staff-home.html')


def render_dashboard_for_staff(staff_mem):
    return render_template('staff-dashboard.html', staff_mem=staff_mem)


@staff_endpoints.route("/staff-validate", methods=['POST'])
def staff_validate():
    if request.method == 'POST':
        staff_id = request.form.get('staffId')
        password = request.form.get('password')
        staff = Staff.objects(staff_id__exact=staff_id)
        if len(staff) > 0:
            staff_mem = staff[0]
            if staff_mem.password == password:
                return render_dashboard_for_staff(staff_mem)
            else:
                return render_template("staff-home.html",
                                       isRegisteredMessage=False,
                                       is_login_error=True,
                                       doSignup=False)
        else:
            return render_template("staff-home.html",
                                   isRegisteredMessage=False,
                                   is_login_error=True,
                                   doSignup=False)
    else:
        print("Please login")
    return render_template('staff-home.html')

@staff_endpoints.route("/staff-add", methods=['POST'])
def staff_add():
    if request.method == 'POST' and request.form.get('registerEmail') is not None:
        staff = Staff.objects(email__exact=request.form.get('registerEmail'))
        if len(staff) == 0:
            new_id = get_new_id()
            staff = Staff(staff_id=new_id,
                              name=request.form.get('registerName'),
                              email=request.form.get('registerEmail'),
                              role=request.form.get('registerRole'),
                              password=request.form.get('registerPassword'))
            staff.save()
            return render_template("staff-home.html", isRegisteredMessage=True, is_login_error=False, doSignup=False,
                                   staff_id=new_id)
        else:
            return render_template("staff-home.html", isRegisteredMessage=False, is_login_error=False, doSignup=True,
                                   student_id=None)
    else:
        print('')

def get_new_id():
    counter = Counter.objects(name="staff_id_counter").first()
    if not counter:
        counter = Counter(name="staff_id_counter")
        counter.save()

    new_id = counter.increment()
    return new_id


@staff_endpoints.route("/staff-logout")
def student_logout():
    return redirect("/staff-home")
