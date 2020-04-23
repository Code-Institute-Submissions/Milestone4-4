from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

"""List of categories to be passed into dropdown of same name for each 
post creation."""
categories = [
    ('', 'Select Post Category'),
    ('crossfit', 'Crossfit'),
    ('olympic weightlifting', 'Olympic Weightlifting'),
    ('powerlifting', 'Powerlifting'),
    ('general', 'General'),
    ('physiotherapy', 'Physiotherapy'),
    ('health', 'Health'),
    ('nutrition', 'Nutrition'),
    ('gymnastics', 'Gymnastics'),
    ('personal training', 'Personal Training')
]


# Models

class Post(models.Model):
    """Model to define the fields required to create Forum Posts displayed in
    Community Forum"""
    title = models.CharField(max_length=150)
    post_text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=21, choices=categories)
    originator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class PostComment(models.Model):
    """Model to define the fields required to create the Comments under a
    community forum post"""
    comment_text = models.TextField()
    date_commented = models.DateTimeField(default=timezone.now)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text
