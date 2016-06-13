from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Movie(models.Model):
	movie_no = models.IntegerField(unique = True)
	name = models.CharField(max_length = 250)

class Count(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	count = models.IntegerField(validators=[MaxValueValidator(5),\
											 MinValueValidator(0)], default = 0)

class Genres(models.Model):
	movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
	genres = models.CharField(max_length = 40)

class Rating(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
	rating = models.IntegerField(validators=[MaxValueValidator(5),\
											 MinValueValidator(0)], default = 0)
#I will save the movies as it is only necessary to look up recommended ones
#I will store the other ratings as a static file because otherwise need
#to look up everything each time 
#I will just get hold of the user data when needed

#class User(User):
	#id = Model.IntegerField(primary_key = True)

# Create your models here.

# If you mean to do aggregation and are using Django 1.1 (currently in alpha 1), you can use the new aggregation features of the ORM:

# from django.db.models import Count
# Members.objects.values('designation').annotate(dcount=Count('designation'))
# This results in a query similar to

# SELECT designation, COUNT(designation) AS dcount
#FROM members GROUP BY designation