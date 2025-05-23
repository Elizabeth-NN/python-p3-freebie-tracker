from models import session, Company, Dev, Freebie

def test_relationships():
    # Check if database has data
    if session.query(Company).count() == 0:
        print("Database is empty. Please run seed.py first.")
        return

    # Test relationships
    company = session.query(Company).first()
    print(f"Company: {company.name}")
    print("Freebies:")
    for freebie in company.freebies:
        print(f"- {freebie.item_name} owned by {freebie.dev.name}")
    
    dev = session.query(Dev).first()
    print(f"\nDev: {dev.name}")
    print("Companies:")
    for company in dev.companies:
        print(f"- {company.name}")

if __name__ == '__main__':
    test_relationships()