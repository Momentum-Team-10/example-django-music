from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class User(AbstractUser):
    def __repr__(self):
        return f"<User username={self.username}>"

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(max_length=75)
    slug = models.SlugField(max_length=75, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Genre name={self.name}>"

    def save(self):
        self.slug = slugify(self.name)
        super().save()


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
    genres = models.ManyToManyField('Genre', related_name="albums")
    favorited_by = models.ManyToManyField(User, related_name="favorite_albums")

    def __repr__(self):
        return f"<Album title={self.title} >"

    def __str__(self):
        return self.title
