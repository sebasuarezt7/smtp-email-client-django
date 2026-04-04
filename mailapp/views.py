from django.shortcuts import render
from django.core.mail import EmailMessage
from .models import Mail

def home(request):
    if request.method == 'POST':
        recipient = request.POST.get('recipients')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        cc_raw = request.POST.get('cc')
        attachment = request.FILES.get('attachment')

        cc_list = []
        if cc_raw:
            cc_list = [email.strip() for email in cc_raw.split(',') if email.strip()]

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

            return render(request, 'mailapp/home.html', {
                'success_message': 'Email sent successfully.'
            })

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

            return render(request, 'mailapp/home.html', {
                'error_message': f'Error sending email: {str(e)}'
            })

    return render(request, 'mailapp/home.html')


def history(request):
    emails = Mail.objects.all().order_by('-sent_at')
    return render(request, 'mailapp/history.html', {'emails': emails})