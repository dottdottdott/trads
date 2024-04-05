from django.db import models
from django.utils.timezone import now

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200, unique=True)
    adddate = models.DateTimeField(auto_now_add=True, blank=True)
    followed = models.BooleanField(default=False)
    last_check = models.DateTimeField(auto_now_add=True, blank=True)
    trust_value = models.FloatField(default=5)
    photo = models.ImageField(upload_to='profile_pic', default='profile_pic/default.jpg')
    key = models.CharField(max_length=2500, null=True, blank=True)

class Content(models.Model):
    url = models.CharField(max_length=200, unique=True)
    signed = models.BooleanField(default=False)
    checksum = models.CharField(max_length=200, null=True, blank=True, default='')
    content = models.CharField(max_length=5000, null=True, blank=True, default='')
    cdate = models.DateTimeField(default=now)
    pdate = models.DateTimeField(null=True, blank=True, default=now)
    
    class Meta:
        abstract = True

class Post(Content):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    response = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    media = models.ImageField(upload_to='post_pic', null=True, blank=True)
    trust_value = models.FloatField(default=5)

class Message(Content):
    correspondent = models.ForeignKey(Author, on_delete=models.CASCADE)
    received = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)

class Vcard(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    bday = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    note = models.CharField(max_length=1000, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

class Preview(models.Model):
    url = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='preview_pic', null=True, blank=True)

class Reaction(Content):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    targetpost = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = [['author', 'targetpost']]
