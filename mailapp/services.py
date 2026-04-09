import urllib.request
from django.core.mail import EmailMessage
from .models import Mail
from django.core.mail import EmailMessage, get_connection

""" This function is responsible for sending an email using the provided sender's email, password, recipient's email,
subject, body, cc list, and attachment. It establishes a connection to the SMTP server, creates an email message, 
and attempts to send it. If the email is sent successfully, it logs the email details in the Mail model with a status 
of 'sent'. If there is an error during the sending process, it logs the error message in the Mail model with a status of 'failed'. 
The function returns a tuple indicating whether the email was sent successfully and an accompanying message."""

def send_email_service(sender, password, recipient, subject, body, cc_list, attachment):
    try:
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host = 'smtp.gmail.com',
            port = 465,
            use_ssl = True,
            username = sender,
            password = password,
        )

        email = EmailMessage(
            from_email=sender,
            to=[recipient],
            subject=subject,
            body=body,
            cc=cc_list,
            connection=connection
        )

        if attachment:
            email.attach(
                attachment.name,
                attachment.read(),
                attachment.content_type
            )

        email.send()

        Mail.objects.create(
            sender=sender,
            recipient=recipient,
            cc=', '.join(cc_list),
            subject=subject,
            body=body,
            attachment_name=attachment.name if attachment else '',
            status='sent'
        )

        return True, "Email sent successfully."

    except Exception as e:
        print(f"Error sending email: {e}")
        Mail.objects.create(
            sender=sender,
            recipient=recipient,
            cc=', '.join(cc_list),
            subject=subject,
            body=body,
            attachment_name=attachment.name if attachment else '',
            status='failed',
            error_message=str(e)
        )
        print(sender)
        return False, str(e)