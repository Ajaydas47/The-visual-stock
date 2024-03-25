from django.db import models

# Create your models here.
class loguser(models.Model):
    username=models.CharField(max_length=50,unique=True)
    email=models.CharField(max_length=50)
    password=models.EmailField(max_length=20)
    def __str__(self):
        return self.username

class Complaint(models.Model):
    username=models.ForeignKey(loguser,on_delete=models.CASCADE)
    mail=models.CharField(max_length=50)
    subject=models.CharField(max_length=150)
    message=models.CharField(max_length=500)
    def __str__(self):
        return self.subject
    
class documents(models.Model):
    fname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    file_type = models.CharField(max_length=50)
    doc = models.FileField()
    inote = models.CharField(max_length=500)
    dates = models.DateField()  # Use DateField for date values
    

    def __str__(self):
        return self.dates.strftime("%Y-%m-%d")