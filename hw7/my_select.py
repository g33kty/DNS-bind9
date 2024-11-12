from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Group, Subject, Teacher
from sqlalchemy import create_engine

# Підключення до бази даних
DATABASE_URL = 'postgresql://myuser:mysecretpassword@localhost:5432/mydatabase'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    """
    Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    """
    result = session.query(
        Student.fullname,
        func.avg(Grade.grade).label('avg_grade')
    ).join(Grade).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return result

def select_2(subject_id):
    """
    Знайти студента із найвищим середнім балом з певного предмета.
    """
    result = session.query(
        Student.fullname,
        func.avg(Grade.grade).label('avg_grade')
    ).join(Grade).filter(Grade.subject_id == subject_id)\
    .group_by(Student.id).order_by(desc('avg_grade')).limit(1).all()
    return result

def select_3(subject_id):
    """
    Знайти середній бал у групах з певного предмета.
    """
    result = session.query(
        Group.name,
        func.avg(Grade.grade).label('avg_grade')
    ).select_from(Group)\
     .join(Student, Student.group_id == Group.id)\
     .join(Grade, Grade.student_id == Student.id)\
     .filter(Grade.subject_id == subject_id)\
     .group_by(Group.id).all()
    return result


def select_4():
    """
    Знайти середній бал на потоці (по всій таблиці оцінок).
    """
    result = session.query(func.avg(Grade.grade).label('avg_grade')).scalar()
    return result

def select_5(teacher_id):
    """
    Знайти які курси читає певний викладач.
    """
    result = session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()
    return result

def select_6(group_id):
    """
    Знайти список студентів у певній групі.
    """
    result = session.query(Student.fullname).filter(Student.group_id == group_id).all()
    return result

def select_7(group_id, subject_id):
    """
    Знайти оцінки студентів у окремій групі з певного предмета.
    """
    result = session.query(
        Student.fullname,
        Grade.grade
    ).join(Grade).filter(Student.group_id == group_id, Grade.subject_id == subject_id).all()
    return result

def select_8(teacher_id):
    """
    Знайти середній бал, який ставить певний викладач зі своїх предметів.
    """
    result = session.query(
        func.avg(Grade.grade).label('avg_grade')
    ).join(Subject).filter(Subject.teacher_id == teacher_id).scalar()
    return result

def select_9(student_id):
    """
    Знайти список курсів, які відвідує певний студент.
    """
    result = session.query(Subject.name)\
        .join(Grade).filter(Grade.student_id == student_id).group_by(Subject.id).all()
    return result

def select_10(student_id, teacher_id):
    """
    Список курсів, які певному студенту читає певний викладач.
    """
    result = session.query(Subject.name)\
        .join(Grade).filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id).group_by(Subject.id).all()
    return result

if __name__ == "__main__":
    print("Топ 5 студентів за середнім балом:", select_1())
    print("Найкращий студент по предмету 1:", select_2(1))
    print("Середній бал по групам для предмету 1:", select_3(1))
    print("Середній бал на потоці:", select_4())
    print("Курси викладача 1:", select_5(1))
    print("Студенти в групі 1:", select_6(1))
    print("Оцінки студентів у групі 1 по предмету 1:", select_7(1, 1))
    print("Середній бал викладача 1:", select_8(1))
    print("Курси студента 1:", select_9(1))
    print("Курси студента 1 від викладача 1:", select_10(1, 1))
