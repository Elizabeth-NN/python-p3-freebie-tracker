

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie

if __name__ == '__main__':
    # Create an engine to connect to the SQLite database
    engine = create_engine('sqlite:///freebies.db')

    # Reset the database by clearing and reseeding
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Clear existing data
    session.query(Freebie).delete()
    session.query(Dev).delete()
    session.query(Company).delete()

    # Create sample companies
    company1 = Company(name="TechCorp", founding_year=1995)
    company2 = Company(name="InnovateInc", founding_year=2005)
    session.add_all([company1, company2])

    # Create sample devs
    dev1 = Dev(name="Alice")
    dev2 = Dev(name="Bob")
    session.add_all([dev1, dev2])

    # Commit the companies and devs to get their IDs
    session.commit()

    # Create sample freebies
    freebie1 = Freebie(item_name="T-Shirt", value=10, company=company1, dev=dev1)
    freebie2 = Freebie(item_name="Mug", value=5, company=company1, dev=dev2)
    freebie3 = Freebie(item_name="Sticker", value=2, company=company2, dev=dev1)
    session.add_all([freebie1, freebie2, freebie3])

    # Commit the freebies
    session.commit()

    print("Database reset and seeded successfully!")

    # Start an ipdb session for interactive debugging
    import ipdb; ipdb.set_trace()

    # Below are the test commands you can run in ipdb to verify all deliverables:

    # Test Freebie methods
    # freebie = session.query(Freebie).first()
    # print(freebie.dev)  # Should return a Dev instance (e.g., Alice)
    # print(freebie.company)  # Should return a Company instance (e.g., TechCorp)
    # print(freebie.print_details())  # Should print "Alice owns a T-Shirt from TechCorp" with colors

    # Test Company methods
    # company = session.query(Company).first()
    # print(company.freebies)  # Should return a list of Freebie instances
    # print(company.devs)  # Should return a list of Dev instances (Alice, Bob)
    # dev = session.query(Dev).filter_by(name="Bob").first()
    # new_freebie = company.give_freebie(dev, "Hat", 15)
    # session.add(new_freebie)
    # session.commit()
    # print(new_freebie.print_details())  # Should print "Bob owns a Hat from TechCorp"
    # oldest = Company.oldest_company(session)
    # print(oldest.name)  # Should print "TechCorp"

    # Test Dev methods
    # dev = session.query(Dev).filter_by(name="Alice").first()
    # print(dev.freebies)  # Should return a list of Freebie instances
    # print(dev.companies)  # Should return a list of Company instances (TechCorp, InnovateInc)
    # print(dev.received_one("T-Shirt"))  # Should return True
    # print(dev.received_one("Pen"))  # Should return False
    # freebie = next(f for f in dev.freebies if f.item_name == "Sticker")  # Explicitly select the Sticker
    # other_dev = session.query(Dev).filter_by(name="Bob").first()
    # dev.give_away(other_dev, freebie)
    # session.commit()
    # print(freebie.dev.name)  # Should print "Bob"
    # print(dev.total_freebie_value())  # Should print 10 (value of T-Shirt, since Sticker was given away)