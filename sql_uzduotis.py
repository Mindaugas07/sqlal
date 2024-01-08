from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine("sqlite:///bankai_saskaitos.db")
Base = declarative_base()

association_table = Table(
    "association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("bank_id", Integer, ForeignKey("bank.id")),
    Column("person_id", Integer, ForeignKey("person.id")),
)


class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True)
    name = Column("Name", String)
    surname = Column("Surname", String)
    person_identity_code = Column("Person code", String)
    phone_number = Column("Phone number", String)
    banks = relationship("Bank", secondary=association_table, back_populates="persons")
    accounts = relationship("BankAccount", back_populates="person")

    def __repr__(self):
        return f"{self.name} {self.surname} {self.person_identity_code} {self.phone_number}"


class Bank(Base):
    __tablename__ = "bank"
    id = Column(Integer, primary_key=True)
    name = Column("Name", String)
    address = Column("Address", String)
    bank_code = Column("Bank code", String)
    swift_code = Column("Swift code", String)
    persons = relationship(
        "Person", secondary=association_table, back_populates="banks"
    )
    accounts = relationship("BankAccount", back_populates="bank")

    def __repr__(self):
        return f"{self.name} {self.address} {self.bank_code} {self.swift_code}"


class BankAccount(Base):
    __tablename__ = "bank_acc"
    id = Column(Integer, primary_key=True)
    account_number = Column("Account number", String)
    balance = Column("Balance", Float)
    person_id = Column(Integer, ForeignKey("person.id"))
    bank_id = Column(Integer, ForeignKey("bank.id"))
    person = relationship("Person", back_populates="accounts")
    bank = relationship("Bank", back_populates="accounts")

    def __repr__(self):
        return f"{self.account_number} {self.balance}"


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def get_all(items):
    print("-------------------")
    for item in items:
        print(item)
    print("-------------------")


while True:
    option = int(
        input(
            "Choose option: \n1 - show banks \n2 - show customers \n3 - show accounts \n4 - add customer\n5 - add bank\n"
        )
    )

    if option == 1:
        banks = session.query(Bank).all()
        get_all(banks)

    elif option == 2:
        persons = session.query(Person).all()
        get_all(persons)

    elif option == 3:
        accounts = session.query(BankAccount).all()
        get_all(accounts)

    elif option == 4:
        name = input("Enter customer name ")
        surname = input("Enter customer surname ")
        person_identity_code = input("Enter customer indentity code ")
        phone_number = input("Enter customer phone number ")

        customer_one = Person(
            name=name,
            surname=surname,
            person_identity_code=person_identity_code,
            phone_number=phone_number,
        )

        session.add(customer_one)
        session.commit()
        session.close()

    elif option == 5:
        name = input("Enter bank name ")
        address = input("Enter bank address ")
        bank_code = input("Enter bank code ")
        swift_code = input("Enter bank swift code ")

        bank_one = Bank(
            name=name, address=address, bank_code=bank_code, swift_code=swift_code
        )
        # acount_one = BankAccount(account_number="5465465", balance="145")

        # bank_one.accounts.append(acount_one)
        # customer_one.banks.append(bank_one)
        # print(customer_one.name)
        # print(bank_one)

        session.add(bank_one)
        session.commit()
        session.close()
