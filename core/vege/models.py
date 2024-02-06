from django.db import models
#Django user model for authentication
from django.contrib.auth.models import User

#Since in accounts we have created a custom user model we need to delete all migrations and db
#Also to use that model we need to add get_user_model from django.contrib.auth
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class Recipe(models.Model):
    # foreign key is used for reference from another table and 
    # on_delete=models.CASCADE is used if django reference table table where model is present got deleted then it will delete all the recipe by that user 
    # if on_delete = models.SET_NULL then all the recipe created by that user will be NULL.
    # on_delete = models.SET_DEFAULT then we can add default value to the recipes that got deleted for that user 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # User is in-built django feature and it contains field that must be in a user like username, first name, last name, email, etc. We can use then

    recipe_name = models.CharField(max_length=100)
    recipe_description = models.TextField()
    recipe_image = models.ImageField(upload_to="recipe")
    recipe_view_count = models.IntegerField(default=1)

class Department(models.Model):
    department = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.department
    
    class Meta:
        ordering = ['department']

class StudentID(models.Model):
    student_id = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.student_id
    
class Subject(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.subject_name
    
class Student(models.Model):
    department = models.ForeignKey(Department, related_name="depart", on_delete=models.CASCADE)
    student_id = models.OneToOneField(StudentID, related_name="studentid", on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    student_age = models.IntegerField(default=18)
    student_address = models.TextField()

    def __str__(self) -> str:
        return self.student_name
    
    class Meta:
        ordering = ['student_name']
        verbose_name = "student"

class SubjectMarks(models.Model):
    student = models.ForeignKey(Student, related_name="studentmarks", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.student.student_name} {self.subject.subject_name}'
        
    class Meta:
        # Each student must have single subject of same name. For example, Student cannot have two computer science subject in a report card.
        unique_together = ['student','subject']

class ReportCard(models.Model):
    student = models.ForeignKey(Student, related_name="studentreportcard",  on_delete = models.CASCADE)
    student_rank = models.IntegerField()
    date_of_report_card_generation = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['student_rank','date_of_report_card_generation']