from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __repr__(self):
        return f"<User username={self.username}>"

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(max_length=75)
    slug = models.SlugField(max_length=75, null=True, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Genre name={self.name}>"

class Artist(models.Model):
    name = models.CharField(max_length=255)
    birthplace = models.CharField(max_length=255)
    birthdate = models.DateField(null=True, blank=True)

    def __repr__(self):
        return f"<Artist name={self.name}>"

    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return f"<Album title={self.title} >"

    def __str__(self):
        return self.title

