"""Seed database with sample data from CSV Files."""
# run with: python3 seed.py

from csv import DictReader
from app import db, init_app
from app.models import User, Message, Follows

app = init_app()
app.app_context().push()

db.drop_all()
db.create_all()

with open("generator/users.csv") as users:
    db.session.bulk_insert_mappings(User, DictReader(users))

with open("generator/messages.csv") as messages:
    db.session.bulk_insert_mappings(Message, DictReader(messages))

with open("generator/follows.csv") as follows:
    db.session.bulk_insert_mappings(Follows, DictReader(follows))

db.session.commit()
