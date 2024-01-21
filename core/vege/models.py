from django.db import models
#Django user model for authentication
from django.contrib.auth.models import User

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

