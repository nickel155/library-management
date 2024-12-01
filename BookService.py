from flask import Blueprint, render_template, request

from Collections.Collections import Book, Counter, BookInstance

book_endpoints = Blueprint('book_endpoints', __name__, template_folder='templates')


def getAllBooks():
    return Book.objects()


@book_endpoints.route('/add-book', methods=['POST'])
def add_book():
    if request.method == 'POST':
        new_book_id = get_new_book_id()
        count = int(request.form.get('count'))
        book = Book(book_id=new_book_id,
                    title=request.form.get('title'),
                    author=request.form.get('author'),
                    genre=request.form.get('genre'),
                    publication_date=request.form.get('publication-date'),
                    count=count,
                    mediatype=request.form.get('media-type'))
        book.save()
        for i in range(count):
            book_instance = BookInstance(
                book_id=new_book_id,
                reservations=[]
            )
            book_instance.save()
        return render_template("staff-dashboard.html",
                               isBookAdded=True,
                               isBookNotAdded=False,
                               book_id=new_book_id)
    else:
        return render_template("staff-dashboard.html",
                               isBookAdded=False,
                               isBookNotAdded=False,
                               book_id=None)


def get_new_book_id():
    counter = Counter.objects(name="book_id_counter").first()
    if not counter:
        counter = Counter(name="book_id_counter", sequence_value=1000000)
        counter.save()

    new_id = counter.increment()
    return new_id
