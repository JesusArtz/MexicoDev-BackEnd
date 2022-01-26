from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.template.loader import get_template
from .forms import *
from .models import *
from django.template import RequestContext
from django.core.mail import send_mail, EmailMultiAlternatives
import hashlib, datetime, random
from django.utils import timezone
from django.conf import settings


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
    if request.method == 'GET':
        registro = Registro(request.POST)
        context = {'registro': registro}

    if request.method == 'POST':
        registro = Registro(request.POST)
        context = {'registro':registro}
        if registro.is_valid():
            registro.is_active = False
            registro.save()  # guardar el usuario en la base de datos si es válido
            username = registro.cleaned_data['username']
            email = registro.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt + email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            # Obtener el nombre de usuario
            user = User.objects.get(username=username)

            # Crear el perfil del usuario
            new_profile = UserProfile(user=user, activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()

            Verificate(email)

            return HttpResponseRedirect('/verificacion/')



    return render(request,'registro.html', context)

def verificateSended(request):
    return render(request, 'email/emailSent.html')


def register_confirm(request, activation_key):
    # Verifica que el usuario ya está logeado
    if request.user.is_authenticated():
        HttpResponseRedirect('/home')

    # Verifica que el token de activación sea válido y sino retorna un 404
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    # verifica si el token de activación ha expirado y si es así renderiza el html de registro expirado
    if user_profile.key_expires < timezone.now():
        return render('user_profile/confirm_expired.html')
    # Si el token no ha expirado, se activa el usuario y se muestra el html de confirmación
    user = user_profile.user
    user.is_active = True
    user.save()
    return render('user_profile/confirm.html')

