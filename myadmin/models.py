from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class MyAdmin(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100)
    role=models.CharField(max_length=20,default='admin')
    password=models.CharField(max_length=255)
    plain_password=models.CharField(max_length=150)
    last_login = models.DateTimeField(null=True, blank=True) 
    created_at=models.DateTimeField(auto_now_add=True)
    
    @property
    def is_authenticated(self):
        return True
        
    class Meta:
        db_table = 'admin'

    def set_password(self,raw):
        self.password=make_password(raw)
        self.save()

    def check_password(self,raw):
        return check_password(raw,self.password)

    def _str_(self):
        return self.name

class Blog(models.Model):
    TYPE_CHOICES = [
        ('social', 'Social'),
        ('education', 'Education'),
    ]
    id= models.AutoField(primary_key=True)      
    title = models.CharField(max_length=255)
    type= models.CharField(max_length=20, choices=TYPE_CHOICES)
    first = models.TextField()
    second = models.TextField()
    conclusion = models.TextField()
    image = models.ImageField(upload_to='images/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blog'

    def _str_(self):
        return self.name