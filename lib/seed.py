#!/usr/bin/env python3

# lib/seed.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie

# Create an engine and session
engine = create_engine('sqlite:///freebies.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Clear existing data
session.query(Freebie).delete()
session.query(Dev).delete()
session.query(Company).delete()

# Create sample companies
company1 = Company(name="Maji-Mazuri", founding_year=1995)
company2 = Company(name="Tailoring", founding_year=2005)
session.add_all([company1, company2])

# Create sample devs
dev1 = Dev(name="Nic")
dev2 = Dev(name="Brian mwas")
session.add_all([dev1, dev2])
session.commit()

# Create sample freebies
freebie1 = Freebie(item_name="Hat", value=10, company=company1, dev=dev1)
freebie2 = Freebie(item_name="Smart Phone", value=5, company=company1, dev=dev2)
freebie3 = Freebie(item_name="Slippers", value=2, company=company2, dev=dev1)
session.add_all([freebie1, freebie2, freebie3])

# Commit the freebies
session.commit()

print("Database seeded successfully!")