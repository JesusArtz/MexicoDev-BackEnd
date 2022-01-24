from django.shortcuts import render, redirect
from .forms import *
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

def index(request):
    return render(request, 'index.html')

def Verificate(email):
    user = email
    context = {'user':user}
    template = get_template('email/index.html')
    content = template.render(context)

    mail = EmailMultiAlternatives(
        'Correo de verificacion',
        'Corre de verificacion para MexicoDev',
        settings.EMAIL_HOST_USER,
        [email],
    )
    mail.attach_alternative(content, 'text/html')
    mail.send()

def registro(request):
    registro = Registro()
    context = {
        'registro':registro
    }
    if request.method == 'POST':
        registro = Registro(request.POST)
        context = {
            'registro': registro
        }
        if registro.is_valid():
            registro.save()
            email=request.POST.get('email')
            Verificate(email)
            return redirect('verificacion')

    return render(request, 'registro.html', context)

def verificateSended(request):
    return render(request, 'email/emailSent.html')


