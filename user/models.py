from django.db import models

# Create your models here.
class contactus(models.Model):
    Name=models.CharField(max_length=100)
    Mobile=models.CharField(max_length=20)
    Email=models.CharField(max_length=40)
    Message=models.TextField()
    def __str__(self):
        return self.Name
    #####################################

class category(models.Model):
    Name=models.CharField(max_length=50)
    Cpic=models.ImageField(upload_to='static/category',default="")
    def __str__(self):
        return self.Name
####################################################
class maincate(models.Model):
    Name=models.CharField(max_length=20)
    picture=models.ImageField(upload_to='static/mcategory/',default="")
    cdate=models.DateField()
    def __str__(self):
       return self.Name

#####################################################
class myproduct(models.Model):
    pprice=models.FloatField()
    dprice=models.FloatField()
    psize=models.CharField(max_length=300)
    pcolor=models.CharField(max_length=30)
    pdes=models.TextField()
    pdel=models.CharField(max_length=80)
    ppic=models.ImageField(upload_to='static/product/',default="")
    pdate=models.DateField()
    pcategory=models.ForeignKey(category,on_delete=models.CASCADE,null=True)
    mcategory=models.ForeignKey(maincate,on_delete=models.CASCADE,null=True)

##################################################
class register(models.Model):
    Name=models.CharField(max_length=200)
    Email=models.CharField(max_length=100,primary_key=True)
    Mobile=models.CharField(max_length=20)
    Ppic=models.ImageField(upload_to='static/profile',null=True)
    Passwd=models.CharField(max_length=128)   
    Address=models.TextField()


  ###########################################
class morder(models.Model):
    userid=models.CharField(max_length=70)
    pid=models.IntegerField()
    remarks=models.CharField(max_length=20)
    odate=models.DateField()
    status=models.BooleanField()
##########################################


class mcart(models.Model):

    userid=models.CharField(max_length=60)
    pid=models.IntegerField()
    cdate=models.CharField(max_length=60)
    status=models.BooleanField()