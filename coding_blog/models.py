from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    class Meta():
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(blank=False)
    published_date = models.DateTimeField(null=False, blank=False, default=timezone.now)

    def __str__(self):
        return f"{self.author}, {self.title}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post} by {self.user}"


class Comment(models.Model):
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(null=False, blank=False, default=timezone.now)
    text = models.TextField(blank=False)

    def __str__(self):
        return f"{self.post} comment by {self.author}, {self.date}"



