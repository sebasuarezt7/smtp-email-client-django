from django.shortcuts import render
from .models import Mail
from .services import send_email_service


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

        success, message = send_email_service(
            recipient, subject, body, cc_list, attachment
        )

        if success:
            return render(request, 'mailapp/home.html', {
                'success_message': message
            })
        else:
            return render(request, 'mailapp/home.html', {
                'error_message': message
            })

    return render(request, 'mailapp/home.html')


def history(request):
    emails = Mail.objects.all().order_by('-sent_at')
    return render(request, 'mailapp/history.html', {'emails': emails})