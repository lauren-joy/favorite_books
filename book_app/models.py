from django.db import models
from login_app.models import *
# Create your models here.
class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) == 0:
            errors['title'] = "Must provide a title"
        if len(postData['description']) < 5:
            errors['description'] = "description must be more than 5 characters"
        return errors


class Book(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
