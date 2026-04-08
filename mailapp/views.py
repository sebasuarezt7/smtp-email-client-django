from django.shortcuts import redirect, render
from .models import Mail, User
from .services import send_email_service
import smtplib
import ssl  


def home(request):
    if  'is_authenticated' not in request.session or not request.session['is_authenticated']:
        return render(request, 'mailapp/login.html')

    if request.method == 'POST':
        sender = request.session['sender']
        password = request.session['password']
        recipient = request.POST.get('recipients')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        cc_raw = request.POST.get('cc')
        attachment = request.FILES.get('attachment')

        cc_list = []
        if cc_raw:
            cc_list = [email.strip() for email in cc_raw.split(',') if email.strip()]
        
        success, message = send_email_service(
            sender, password, recipient, subject, body, cc_list, attachment
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
    emails = Mail.objects.filter(sender=request.session['sender']).order_by('-sent_at')
    return render(request, 'mailapp/history.html', {'emails': emails})

def login(request):
    if request.method == 'POST':
        sender = request.POST.get('sender')
        password = request.POST.get('password')
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as smtp:
                smtp.login(sender, password) #Authenticate with the SMTP server using the sender's email and app password
                request.session['sender'] = sender
                request.session['password'] = password
                request.session['is_authenticated'] = True
                return redirect('home')
        except Exception as e:
            return render(request, 'mailapp/login.html', {'error': str('Login failed: ' + str(e))})
    return render(request, 'mailapp/login.html')

def register(request):
    if request.method == 'POST':
        sender = request.POST.get('sender')
        password = request.POST.get('password')
        if User.objects.filter(sender=sender).exists():
            return render(request, 'mailapp/login.html', {'error': 'Email already registered.'})
        User.objects.create(sender=sender, password=password)
        return redirect('login')
    return render(request, 'mailapp/register.html')
