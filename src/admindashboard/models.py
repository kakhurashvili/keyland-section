
# Create your models here.
from django.db import models

class UserActivityData(models.Model):
    active_users = models.IntegerField(default=0)
    inactive_users = models.IntegerField(default=0)
    date_label = models.CharField(max_length=20)

    def __str__(self):
        return self.date_label
    
class UserActivity(models.Model):
    interval_start = models.DateTimeField()
    interval_end = models.DateTimeField()
    signup_count = models.IntegerField()

    # Add any additional fields or methods as needed

    class Meta:
        verbose_name_plural = "User Activities"

    def __str__(self):
        return f"{self.interval_start} - {self.interval_end}"
