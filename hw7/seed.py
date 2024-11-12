import random
from datetime import date
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Group, Teacher, Subject, Grade

fake = Faker()

DATABASE_URL = 'postgresql://myuser:mysecretpassword@localhost:5432/mydatabase'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def seed_data():
    groups = [Group(name=f"Group {i+1}") for i in range(3)]
    session.add_all(groups)
    session.commit()

    teachers = [Teacher(fullname=fake.name()) for _ in range(4)]
    session.add_all(teachers)
    session.commit()

    subjects = [
        Subject(name=fake.word(), teacher=random.choice(teachers)) for _ in range(6)
    ]
    session.add_all(subjects)
    session.commit()

    students = [
        Student(fullname=fake.name(), group=random.choice(groups)) for _ in range(30)
    ]
    session.add_all(students)
    session.commit()

    for student in students:
        for subject in subjects:
            for _ in range(random.randint(5, 10)):
                grade = Grade(
                    student=student,
                    subject=subject,
                    grade=random.uniform(1, 10),
                    date=fake.date_this_year()
                )
                session.add(grade)
    session.commit()

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    seed_data()
    print("Database seeded successfully.")
