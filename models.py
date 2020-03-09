"""Models for Body and their children (BodyChildRelation)."""
from uuid import uuid4
from django.db import models
from helpers.misc import get_url_friendly

class Book(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    str_id = models.CharField(max_length=50, editable=False, null=True)
    str_book = models.CharField(max_length=50, editable=False, null=True)
    
    name_author = models.CharField(max_length=50)
    canonical_name = models.CharField(max_length=50, blank=True)
    short_description = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    isbn_number = models.IntegerField(max_digits=13)

    def save(self, *args, **kwargs):
        self.str_id = get_url_friendly(self.str_book if not self.canonical_name else self.canonical_name)
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return self.str_book

    def get_absolute_url(self):
        return '/org/' + self.str_id

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ("name",)

class User(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    str_id = models.CharField(max_length=50, editable=False, null=True)
    str_username = models.CharField(max_length=50, editable=False, null=True)
    
    location_user = models.CharField(max_length=50)
    canonical_name = models.CharField(max_length=50, blank=True)
    roll_number = models.CharField(max_length = 10)
    phone_number = models.CharField(max_length = 10)


    def save(self, *args, **kwargs):
        self.str_id = get_url_friendly(self.str_username if not self.canonical_name else self.canonical_name)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.str_username

    def get_absolute_url(self):
        return '/org/' + self.str_id

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("name",)


class BookUserRelation(models.Model):
    """Foreign Key Many to One Relationship."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    parent = models.ForeignKey(User, on_delete=models.CASCADE, default=uuid4, related_name='children')
    child = models.ForeignKey(Book, on_delete=models.CASCADE, default=uuid4, related_name='parents')

    def __str__(self):
        return self.parent.str_username + " --> " + self.child.str_book

    class Meta:
        verbose_name = "User-Book Relation"
        verbose_name_plural = "User-Book Relations"
        ordering = ("parent__name",)
