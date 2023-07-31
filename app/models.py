from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
# Create your models here.

class Song(models.Model):
    genre = [
        ("Classic", "Classic"),
        ("Melody", "Melody"),
        ("Love", "Love"),
        ("Pop", "Pop"),
        ("Rock", "Rock"),
        ("Jazz", "Jazz"),
        ("Hiphop", "Hiphop"),
    ]

    language = [
        ("Tamil", "Tamil"),
        ("English", "English")
    ]
    def current_year():
        return datetime.date.today().year

    song_movie = models.CharField( max_length= 50,blank=True, default='Unknown')
    song_title = models.CharField( max_length= 50,blank=True, null=True)
    song_artist = models.CharField( max_length= 50,blank=True, null=True)
    song_language = models.CharField( max_length= 50, null=True, choices=language, default="Unknown")
    song_released = models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(1956), MaxValueValidator(current_year())])
    song_gener = models.CharField(max_length=20, choices=genre, default='Unknown')
    song_audio_file = models.FileField(blank=True, null=True)
    def __str__(self):
        return self.song_title

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    songs = models.ForeignKey(Song, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

