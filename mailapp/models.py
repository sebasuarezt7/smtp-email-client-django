from django.db import models

""" This model represents an email that has been sent or is in the process of being sent. It includes fields for the sender, recipient, cc, subject, body, attachment name, status, error message, and the timestamp when the email was sent. 
The Mail model is used to log the details of each email sent through the application, allowing for tracking and troubleshooting of email sending operations. The User model represents a user with an email and password, which can be used for authentication when sending emails. """
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