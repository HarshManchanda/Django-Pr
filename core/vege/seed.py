# To create fake data for our db
# We will use faker library of python

from faker import Faker
fake = Faker()
import random
from .models import *
from django.db.models import Sum

def create_subject_marks(n):
    try:
        student_obj = Student.objects.all()
        for student in student_obj:
            subjects = Subject.objects.all()
            for subject in subjects:
                SubjectMarks.objects.create(
                    subject = subject,
                    student = student,
                    marks = random.randint(1,100)
                )
    except Exception as e:
        print(e)

def seed_db(n=10)->None:
    try:
        for _ in range(n):
            department_obj = Department.objects.all()
            random_index = random.randint(0,len(department_obj)-1)
            department = department_obj[random_index]
            student_id = f'Std-0{random.randint(100,999)}'
            student_name = fake.name()
            student_email = fake.email()
            student_age = random.randint(18,26)
            student_address = fake.address()

            student_id_obj = StudentID.objects.create(student_id = student_id)

            student_obj = Student.objects.create(
                department = department,
                student_id = student_id_obj,
                student_name = student_name,
                student_email = student_email,
                student_age = student_age,
                student_address = student_address,
            )
    except Exception as e:
        print(e)

def generate_report_card():
    print("Run...")
    ranks = Student.objects.annotate(marks = Sum('studentmarks__marks')).order_by('-marks','-student_age')
    
    i = 1
    for rank in ranks:
        ReportCard.objects.create(
            student = rank,
            student_rank = i
        )
        i += 1

