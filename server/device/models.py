from django.db import models

# Create your models here.

class Node(models.Model):
    id = models.AutoField(primary_key=True)
    ip_address = models.GenericIPAddressField(unique=True)
    node_name = models.CharField(max_length=50, null=True)
    total_menory = models.IntegerField(default=0, null=True)
    remaining_menory = models.IntegerField(default=0, null=True)
    state = models.CharField(max_length=50, null=True, default='offline')


    def __str__(self):
        return self.node_name



class Device(models.Model):
    id = models.AutoField(primary_key=True)
    ip_address = models.GenericIPAddressField(unique=True)
    node_name = models.CharField(max_length=50, null=True)