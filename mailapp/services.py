from django.core.mail import EmailMessage
from .models import Mail

def send_email_service(recipient, subject, body, cc_list, attachment):
    try:
        email = EmailMessage(
            subject,
            body,
            to=[recipient],
            cc=cc_list
        )

        if attachment:
            email.attach(
                attachment.name,
                attachment.read(),
                attachment.content_type
            )

        email.send()

        Mail.objects.create(
            recipient=recipient,
            cc=', '.join(cc_list),
            subject=subject,
            body=body,
            attachment_name=attachment.name if attachment else '',
            status='sent'
        )

        return True, "Email sent successfully."

    except Exception as e:
        Mail.objects.create(
            recipient=recipient,
            cc=', '.join(cc_list),
            subject=subject,
            body=body,
            attachment_name=attachment.name if attachment else '',
            status='failed',
            error_message=str(e)
        )

        return False, str(e)