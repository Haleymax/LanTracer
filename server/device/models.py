from django.db import models

# Create your models here.

class Node(models.Model):
    id = models.AutoField(primary_key=True)
    ip_address = models.GenericIPAddressField(unique=True)
    node_name = models.CharField(max_length=50, null=True)
    total_menory = models.IntegerField(default=0, null=True)
    remaining_menory = models.IntegerField(default=0, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=50, null=True, default='offline')


    def __str__(self):
        return self.node_name



class Device(models.Model):
    id = models.AutoField(primary_key=True)
    ip_address = models.GenericIPAddressField(unique=True)
    node_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.node_name

class SharedKey(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=50, unique=True)
    value = models.BinaryField(max_length=50, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key