from django.db import models

# Create your models here.

class Asset(models.Model):
    name = models.CharField(max_length=100)
    service_time = models.DateTimeField()
    expiration_time = models.DateTimeField()
    serviced = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Notification(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=[('service', 'Service'), ('expiration', 'Expiration')])

    def __str__(self):
        return f"Notification for {self.asset.name} at {self.created_at}"

class Violation(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=[('service', 'Service'), ('expiration', 'Expiration')])

    def __str__(self):
        return f"Violation for {self.asset.name} at {self.created_at}"
