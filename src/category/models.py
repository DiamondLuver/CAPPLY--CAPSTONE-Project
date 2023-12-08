from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.text import slugify
import random, string
from django.contrib.auth.models import UserManager
from django.db import models
from PIL import Image
# Create your models here.
def randomString():
    um = UserManager()
    return( um.make_random_password( length=25 ) )

def random_slug():
    allowed_chars = ''.join((string.ascii_letters, string.digits))
    unique_slug = ''.join(random.choice(allowed_chars) for _ in range(32))
    return unique_slug

# COUNTRY MODEL
# SCHOLARSHIP MODEL


# COUNTRY
class Country(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
# SCHOLARSHIP
class Scholarship(models.Model):
    id = models.BigAutoField(primary_key=True)
    level = models.CharField(max_length=120)
    school = models.CharField(max_length=200)
    deadline = models.DateField(null=True)
    more_info = models.TextField()
    description = models.TextField(blank=True, null=True, max_length=275)
    link_web = models.CharField(max_length=200)
    country = models.CharField(max_length=120)
    default_slug = slugify(random_slug())
    slug = models.SlugField(null=False, unique=True)
    
    def get_absolute_url(self):
        return reverse("scholarship_detail", kwargs={"slug": self.slug})
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(random_slug())
        return super().save(*args, **kwargs)

# Level 
class Level(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, null = False, related_name ='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null = False, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    class Meta:
        ordering = ['created_on']
    def __str__(self):
        return 'Comment {} by {}'.format(self.content, self.user)
    
# REPLY
class Reply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    def __str__(self):
        return 'Reply {} by {}'.format(self.content, self.user)
    
# FAVORITE
class FavoriteScholarship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scholarship_school = models.CharField(max_length=100)
    scholarship_link = models.CharField(max_length=120, null=True)
   
    def __str__(self):
        return self.scholarship_school
   
class Favorited(models.Model):
    favorited = models.OneToOneField(FavoriteScholarship, on_delete=models.CASCADE, default=None)
    activation = models.BooleanField(default=False)

