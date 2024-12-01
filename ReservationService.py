from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for

from Collections.Collections import Book, Counter, BookInstance, Reservation, TimePeriod

reservation_endpoints = Blueprint('reservation_endpoints', __name__, template_folder='templates')

@reservation_endpoints.route('/reserve-book', methods=['POST'])
def reserve_book():
    book_id = request.form.get('book-id')
    member_id = request.form.get('member-id')
    from_date = datetime.strptime(request.form.get('from-date'), "%Y-%m-%d")
    to_date = datetime.strptime(request.form.get('to-date'), "%Y-%m-%d")
    book_instances = BookInstance.objects(book_id=book_id)
    is_book_available = False
    available_book_instance_id = None
    today = datetime.now().strftime("%Y-%m-%d")
    latest_available_date = None

    for book_instance in book_instances:
        is_book_available_instance = True
        time_periods = book_instance.reservations
        for time_period in time_periods:
            temp_from_date = datetime.strptime(time_period.from_date, "%Y-%m-%d")
            temp_to_date = datetime.strptime(time_period.to_date, "%Y-%m-%d")
            if temp_from_date < from_date:
                if temp_to_date >= from_date:
                    is_book_available_instance = False
                    latest_available_date = get_latest_available_date(latest_available_date, temp_to_date)
                    break
            elif temp_from_date <= to_date:
                is_book_available_instance = False
                latest_available_date = get_latest_available_date(latest_available_date, temp_to_date)
                break
        if is_book_available_instance:
            is_book_available = True
            available_book_instance_id = book_instance.id
            break

    if is_book_available:
        new_reservation_id = get_new_reservation_id()
        reservation = Reservation(
            reservation_id=new_reservation_id,
            member_id=member_id,
            book_id=available_book_instance_id,
            reservation_date=today,
            reservation_start_dare=from_date.strftime("%Y-%m-%d"),
            reservation_end_dare=to_date.strftime("%Y-%m-%d"),
            reservation_status='Booked'
        )
        reservation.save()
        book_instance = BookInstance.objects(instance_id=available_book_instance_id).first()
        current_time_period = TimePeriod(
            from_date=from_date.strftime("%Y-%m-%d"),
            to_date=to_date.strftime("%Y-%m-%d")
        )
        book_instance.reservations.append(current_time_period)
        book_instance.save()
        return redirect(url_for('member_endpoints.render_dashboard_for_member',
                                member_id=member_id,
                                is_book_reserved=True,
                                is_book_available=is_book_available))
    else:
        latest_available_date = latest_available_date.strftime("%Y-%m-%d")
        return redirect(url_for('member_endpoints.render_dashboard_for_member',
                                member_id=member_id,
                                is_book_reserved=False,
                                is_book_available=is_book_available,
                                latest_available_date=latest_available_date))



def get_new_reservation_id():
    counter = Counter.objects(name="reservation_id_counter").first()
    if not counter:
        counter = Counter(name="reservation_id_counter", sequence_value=1111111111)
        counter.save()

    new_id = counter.increment()
    return new_id

def get_latest_available_date(latest_available_date, temp_to_date):
    if latest_available_date is not None:
        return temp_to_date if temp_to_date < latest_available_date else latest_available_date
    return temp_to_date