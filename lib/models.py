

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

# Create the base class for declarative models
Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    # Columns for the companies table
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    # Relationship: A company has many freebies
    freebies = relationship('Freebie', back_populates='company')

    # Relationship: A company has many devs through freebies (many-to-many)
    # Added overlaps to silence the warning
    devs = relationship(
        'Dev',
        secondary='freebies',
        back_populates='companies',
        overlaps="company,freebies"
    )

    def __repr__(self):
        return f'<Company {self.name}>'

    def give_freebie(self, dev, item_name, value):
        """
        Creates a new Freebie instance associated with this company and the given dev.
        Args:
            dev (Dev): The Dev instance receiving the freebie
            item_name (str): The name of the freebie item
            value (int): The value of the freebie
        Returns:
            Freebie: The newly created Freebie instance
        """
        freebie = Freebie(item_name=item_name, value=value, company=self, dev=dev)
        return freebie

    @classmethod
    def oldest_company(cls, session):
        """
        Returns the Company instance with the earliest founding year.
        Args:
            session: The SQLAlchemy session to use for the query
        Returns:
            Company: The oldest company instance
        """
        from sqlalchemy import func
        return session.query(cls).order_by(cls.founding_year.asc()).first()

class Dev(Base):
    __tablename__ = 'devs'

    # Columns for the devs table
    id = Column(Integer(), primary_key=True)
    name = Column(String())

    # Relationship: A dev has many freebies
    # Added overlaps to silence the warning
    freebies = relationship(
        'Freebie',
        back_populates='dev',
        overlaps="devs"
    )

    # Relationship: A dev has many companies through freebies (many-to-many)
    # Added overlaps to silence the warning
    companies = relationship(
        'Company',
        secondary='freebies',
        back_populates='devs',
        overlaps="company,dev,freebies"
    )

    def __repr__(self):
        return f'<Dev {self.name}>'

    def received_one(self, item_name):
        """
        Checks if the dev has a freebie with the given item_name.
        Args:
            item_name (str): The name of the item to check for
        Returns:
            bool: True if the dev has a freebie with the item_name, False otherwise
        """
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        """
        Transfers a freebie to another dev if the freebie belongs to this dev.
        Args:
            dev (Dev): The dev to give the freebie to
            freebie (Freebie): The freebie to give away
        """
        if freebie.dev == self:
            freebie.dev = dev

    def total_freebie_value(self):
        """
        Calculates the total value of all freebies collected by the dev.
        Returns:
            int: The sum of the values of all freebies
        """
        return sum(freebie.value for freebie in self.freebies)

class Freebie(Base):
    __tablename__ = 'freebies'

    # Columns for the freebies table
    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    # Explicitly define the dev relationship with overlaps
    dev = relationship(
        'Dev',
        back_populates='freebies',
        overlaps="devs"
    )

    # Explicitly define the company relationship
    company = relationship(
        'Company',
        back_populates='freebies'
    )

    def print_details(self):
        """
        Returns a formatted string with the freebie's details, styled with colors.
        Returns:
            str: A string in the format '{dev name} owns a {item_name} from {company name}'
        """
        dev_name = f"{Fore.CYAN}{self.dev.name}{Style.RESET_ALL}"
        item_name = f"{Fore.GREEN}{self.item_name}{Style.RESET_ALL}"
        company_name = f"{Fore.MAGENTA}{self.company.name}{Style.RESET_ALL}"
        return f"{dev_name} owns a {item_name} from {company_name}"