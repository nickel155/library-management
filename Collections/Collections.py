import uuid

from mongoengine import (Document, StringField, ObjectIdField, ReferenceField, IntField, EmbeddedDocument,
                         EmbeddedDocumentListField, DateField)


class TimePeriod(EmbeddedDocument):
    from_date = StringField()
    to_date = StringField()


class Book(Document):
    book_id = IntField(primary_key=True)
    title = StringField()
    author = StringField()
    genre = StringField()
    publication_date = StringField()
    count = IntField()
    mediatype = StringField()


class BookInstance(Document):
    instance_id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    book_id = ReferenceField(Book)
    reservations = EmbeddedDocumentListField(TimePeriod)


class Member(Document):
    member_id = IntField(primary_key=True)
    name = StringField()
    email = StringField()
    contact_no = StringField()
    join_date = DateField()
    password = StringField()


class Reservation(Document):
    reservation_id = IntField(primary_key=True)
    member_id = ReferenceField(Member)
    book_id = StringField()
    reservation_date = StringField()
    reservation_start_dare = StringField()
    reservation_end_dare = StringField()
    reservation_status = StringField()


class Payment(Document):
    payment_id = ObjectIdField(primary_key=True)
    transaction = StringField()
    card_type = StringField()
    amount = StringField()
    payment_status = StringField()


class Staff(Document):
    staff_id = IntField(primary_key=True)
    name = StringField()
    role = StringField()
    email = StringField()
    password = StringField()


class Counter(Document):
    name = StringField(unique=True)
    sequence_value = IntField(default=1000)

    def increment(self):
        self.sequence_value += 1
        self.save()
        return self.sequence_value
