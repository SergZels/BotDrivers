from django.db import models

# Create your models here.
from datetime import date
# Create your models here.
class Cod(models.Model):
    cod = models.CharField(max_length= 200)
    stayt = models.CharField(max_length= 200, default="free")
    #dr = models.OneToOneField(Driver, on_delete=models.SET_NULL, null=True, blank=True)
class Driver(models.Model):
    name = models.CharField(max_length= 100)
    text = models.TextField(max_length=700)
    cod = models.OneToOneField(Cod, on_delete=models.CASCADE, blank=True,default="")
    telegramId = models.CharField(max_length=100, default="")
    def __str__(self):
        return f"{self.name} {self.text}"


class Publications(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True )
    data = models.DateField(auto_now_add=True)
    dataOfStartRoute = models.DateField(default="2020-10-20")
    summ = models.CharField(max_length=200, default="0")
    allowed = models.CharField(max_length=200, default="")
    text = models.TextField(max_length=400)
    PublicationsAllowed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Drivers Publications"

    def __str__(self):
        return f"{self.driver} - {self.data}"

