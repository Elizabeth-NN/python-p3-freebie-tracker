

from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Define the naming convention for foreign keys
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

# Create the base 
Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    # Columns for the companies table
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    #A company has many freebies
    freebies = relationship('Freebie', back_populates='company')

    #A company has many devs through freebies (many-to-many)
    
    devs = relationship(
        'Dev',
        secondary='freebies',
        back_populates='companies',
        # getting an error without it
        overlaps="company,freebies" 
    )

    def __repr__(self):
        return f'<Company {self.name}>'

    def give_freebie(self, dev, item_name, value):
       
        # Creates a new Freebie instance associated with this company and the given dev.
       
        freebie = Freebie(item_name=item_name, value=value, company=self, dev=dev)
        return freebie

    @classmethod
    def oldest_company(cls, session):
        # returns the Company instance with the earliest founding year.
        from sqlalchemy import func
        return session.query(cls).order_by(cls.founding_year.asc()).first()

class Dev(Base):
    __tablename__ = 'devs'

    # Columns for the devs table
    id = Column(Integer(), primary_key=True)
    name = Column(String())

    # A dev has many freebies
    freebies = relationship(
        'Freebie',
        back_populates='dev',
        overlaps="devs"
    )

    # A dev has many companies through freebies (many-to-many)
    companies = relationship(
        'Company',
        secondary='freebies',
        back_populates='devs',
        overlaps="company,dev,freebies"
    )

    def __repr__(self):
        return f'<Dev {self.name}>'

    def received_one(self, item_name):
        # Checks if the dev has a freebie with the given item_name
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):

        # Transfers a freebie to another dev if the freebie belongs to this dev.
        
        if freebie.dev == self:
            freebie.dev = dev

    def total_freebie_value(self):
        # Calculates the total value of all freebies collected by the dev.
        return sum(freebie.value for freebie in self.freebies)

class Freebie(Base):
    __tablename__ = 'freebies'

    # Columns for the freebies table
    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    #define the dev relationship with overlaps
    dev = relationship(
        'Dev',
        back_populates='freebies',
        overlaps="devs"
    )

    #define the company relationship
    company = relationship(
        'Company',
        back_populates='freebies'
    )

    def print_details(self):
       
        # Returns a formatted string with the freebie's details, styled with colors.
       
        dev_name = f"{Fore.CYAN}{self.dev.name}{Style.RESET_ALL}"
        item_name = f"{Fore.GREEN}{self.item_name}{Style.RESET_ALL}"
        company_name = f"{Fore.MAGENTA}{self.company.name}{Style.RESET_ALL}"
        return f"{dev_name} owns a {item_name} from {company_name}"