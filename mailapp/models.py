from django.db import models


class Mail(models.Model):
    sender = models.EmailField()
    recipient = models.EmailField()
    cc = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()

    attachment_name = models.CharField(max_length=255, blank=True, null=True)

    status = models.CharField(max_length=20)  # sent / failed
    error_message = models.TextField(blank=True, null=True)

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
class User(models.Model):
    sender = models.EmailField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.sender