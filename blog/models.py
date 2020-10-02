from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField

class Post(models.Model):
    title = models.CharField(max_length=200,)
    content = RichTextField()
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    #saved = models.MantToManyField(Us)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return f'{self.id} {self.title}'

    def get_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post-detail', args=[str(self.id)])
