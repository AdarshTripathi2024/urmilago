from django.db import models

# Create your models here.
class Contact(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    email=models.EmailField()
    phone=models.CharField(max_length=15) 
    message=models.TextField()
    submitted_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.name}"

class Join(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField()
    email=models.EmailField(max_length=255)
    phone=models.CharField(max_length=15)
    address=models.CharField(max_length=255)
    occupation=models.CharField(max_length=100)
    message=models.TextField()
    submitted_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.name}"

class Subscriber(models.Model):
    id=models.AutoField(primary_key=True)
    email= models.EmailField(unique =True)
    is_verified = models.BooleanField(default =False)
    created_at = models.DateTimeField(auto_now_add =True)
    
    class Meta:
        db_table = 'subscriber'

    def __str__(self):
        return f"{self.id} - {self.email}"