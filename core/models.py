from django.db import models

class UserProgress(models.Model):
    username = models.CharField(max_length=150)  # Or use ForeignKey to User if doing full auth
    course = models.CharField(max_length=255)
    progress = models.IntegerField()  # percentage
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.course} ({self.progress}%)"