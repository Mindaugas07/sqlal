import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///emlpoyees.db")
Base = declarative_base()


class Employee(Base):
    __tablename__ = "Workers"
    id = Column(Integer, primary_key=True)
    name = Column("Name", String)
    surname = Column("Surname", String)
    birth_date = Column("Date of birth", String)
    position = Column("Position", String)
    salary = Column("Salary", Integer)
    created_date = Column("Creation date", DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, surname, birth_date, position, salary):
        self.name = name
        self.surname = surname
        self.birth_date = birth_date
        self.position = position
        self.salary = salary

    def __repr__(self):
        return f"{self.id} {self.name} {self.surname} {self.birth_date} - {self.position} {self.salary} USD: {self.created_date}"


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()
""":type: sqlalchemy.orm.Session"""

while True:
    option = int(
        input(
            "Choose option: \n1 - show employees \n2 - create amployee \n3 - change employee data \n4 - delete employee\n"
        )
    )

    if option == 1:
        workers = session.query(Employee).all()
        print("-------------------")
        for worker in workers:
            print(worker)
        print("-------------------")

    if option == 2:
        name = input("Enter worker name")
        surname = input("Enter worker surname")
        birth_date = input("Enter worker date of birth")
        position = input("Enter worker position")
        salary = input("Enter worker salary")
        worker = Employee(name, surname, birth_date, position, salary)
        session.add(worker)
        session.commit()

    if option == 3:
        workers = session.query(Employee).all()
        print("-------------------")
        for worker in workers:
            print(worker)
        print("-------------------")
        worker_id = int(input("Enter worker ID"))
        modified_worker = session.query(Employee).get(worker_id)
        modification = int(
            input(
                "What do you want to modify: 1 - name, 2 - surname, 3 - birth date, 4 - position, 5 - salary"
            )
        )
        if modification == 1:
            modified_worker.name = input("Enter worker name")
        if modification == 2:
            modified_worker.surname = input("Enter worker surname")
        if modification == 3:
            modified_worker.birth_date = input("Enter worker date of birth")
        if modification == 4:
            modified_worker.position = input("Enter worker position")
        if modification == 5:
            modified_worker.salary = input("Enter worker salary")
        session.commit()

    if option == 4:
        workers = session.query(Employee).all()
        print("-------------------")
        for worker in workers:
            print(worker)
        print("-------------------")
        modified_worker_id = int(input("Enter worker ID"))
        deleting_worker = session.query(Employee).get(modified_worker_id)
        session.delete(deleting_worker)
        session.commit()
