from models import session, Company, Dev, Freebie

def seed_data():
    # Clear existing data
    session.query(Freebie).delete()
    session.query(Company).delete()
    session.query(Dev).delete()
    session.commit()

    # Create companies
    google = Company(name="Google", founding_year=1998)
    microsoft = Company(name="Microsoft", founding_year=1975)
    apple = Company(name="Apple", founding_year=1976)

    # Create devs
    alice = Dev(name="Alice")
    bob = Dev(name="Bob")
    charlie = Dev(name="Charlie")

    # Add all to session
    session.add_all([google, microsoft, apple, alice, bob, charlie])
    session.commit()

    # Create freebies
    freebies = [
        Freebie(item_name="T-shirt", value=10, dev=alice, company=google),
        Freebie(item_name="Sticker", value=2, dev=alice, company=microsoft),
        Freebie(item_name="Mug", value=5, dev=bob, company=google),
        Freebie(item_name="Laptop", value=1000, dev=charlie, company=apple),
        Freebie(item_name="Hat", value=8, dev=charlie, company=google)
    ]
    
    session.add_all(freebies)
    session.commit()

if __name__ == '__main__':
    seed_data()