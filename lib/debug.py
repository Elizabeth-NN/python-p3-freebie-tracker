

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

    print("Database reset and seeded successfully!")

    # Start an ipdb session for interactive debugging
    import ipdb; ipdb.set_trace()

   

    # Test Freebie methods
    # freebie = session.query(Freebie).first()
    # print(freebie.dev)  # Should return a Dev instance (e.g., Nic)
    # print(freebie.company)  # Should return a Company instance (e.g., Maji-Mazuri)
    # print(freebie.print_details())  # Should print "Nic owns a Hat from Maji-Mazuri" with colors

    # Test Company methods
    # company = session.query(Company).first()
    # print(company.freebies)  # Should return a list of Freebie instances
    # print(company.devs)  # Should return a list of Dev instances (Nic, Brian mwas)
    # dev = session.query(Dev).filter_by(name="Brian mwas").first()
    # new_freebie = company.give_freebie(dev, "Hat", 15)
    # session.add(new_freebie)
    # session.commit()
    # print(new_freebie.print_details())  # Should print "Bob owns a Hat from Maji-Mazuri"
    # oldest = Company.oldest_company(session)
    # print(oldest.name)  # Should print "Maji-Mazuri"

    # Test Dev methods
    # dev = session.query(Dev).filter_by(name="Nic").first()
    # print(dev.freebies)  # Should return a list of Freebie instances
    # print(dev.companies)  # Should return a list of Company instances (Maji-Mazuri, Tailoring)
    # print(dev.received_one("Hat"))  # Should return True
    # print(dev.received_one("Pen"))  # Should return False
    # freebie = next(f for f in dev.freebies if f.item_name == "Slippers")  # Explicitly select the Slippers
    # other_dev = session.query(Dev).filter_by(name="Brian mwas").first()
    # dev.give_away(other_dev, freebie)
    # session.commit()
    # print(freebie.dev.name)  # Should print "Brian mwas"
    # print(dev.total_freebie_value())  # Should print 10 (value of Hat, since Slippers was given away)