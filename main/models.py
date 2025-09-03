from django.db import models
import uuid
from django.db import models

class News(models.Model):
    CATEGORY_CHOICES = [
        ('transfer', 'Transfer'),
        ('update', 'Update'),
        ('exclusive', 'Exclusive'),
        ('match', 'Match'),
        ('rumor', 'Rumor'),
        ('analysis', 'Analysis'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    thumbnail = models.URLField(blank=True, null=True)
    news_views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def is_news_hot(self):
        return self.news_views > 20

    def increment_views(self):
        self.news_views += 1
        self.save()
# Create your models here.
# models.Model is the base class used to define models in Django.
# News is the name of the model we're defining.
# CATEGORY_CHOICES is a tuple that defines available news category options.
# id is a field of type UUIDField used as primary key with automatically generated values using uuid.uuid4.
# title is a field of type CharField for news title, with maximum length of 255 characters.
# content is a field of type TextField for news content that can hold long text.
# category is a field of type CharField with limited choices according to CATEGORY_CHOICES, with default value 'update'.
# thumbnail is a field of type URLField for storing news thumbnail image URL (optional).
# news_views is a field of type PositiveIntegerField that stores the number of news views, with default value 0.
# created_at is a field of type DateTimeField that automatically contains the date and time when data is created.
# is_featured is a field of type BooleanField to mark whether this news is displayed as featured news.
# The __str__ method is used to return a string representation of the object (in this case, the news title).
# The @property decorator is used to create read-only attributes whose values are calculated from other attributes. In this case, is_news_hot will be True if the news views are more than 20.
# The increment_views() method is used to increase the news views by 1 and save the changes to the database.