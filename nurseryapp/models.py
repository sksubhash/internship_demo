from django.db import models
from django.conf import settings


class tblplants(models.Model):
    name = models.CharField(max_length=254)
    descriptions = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.SmallIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plant_image = models.FileField(upload_to='plants')

    class Meta:
        db_table = "tblplants"


class tblorder(models.Model):
    customer_name = models.CharField(max_length=254)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plant = models.ForeignKey(tblplants, on_delete=models.DO_NOTHING)
    quantity = models.SmallIntegerField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    order_status = models.SmallIntegerField(default=0)

    class Meta:
        db_table = "tblorder"


class tblreg(models.Model):
    address = models.TextField()
    user_email = models.EmailField(max_length=254)
    image = models.FileField(upload_to='nurseries')

    class Meta:
        db_table = "tblreg"
