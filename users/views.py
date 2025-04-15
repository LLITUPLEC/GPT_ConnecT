from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from datetime import datetime
import requests


def location(ip: str):
    response = requests.get(f"http://ip-api.com/json/{ip}?lang=ru")
    result = response.json()
    record = []

    for key, value in result.items():
        record.append(value)
        print(f"[{key.title()}]: {value}")
    return tuple(record)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            secret_key = request.POST['secret_key']
            if secret_key != '27122024A':
                messages.info(request, 'ОШИБКА! Секретный код введён неверно!')
                return HttpResponseRedirect(f'/register')
            form.save()
            username = form.cleaned_data.get('username')
            with open('media/logging/log_reg.txt', 'a') as f:
                f.write(
                    f'\n{datetime.now()}: Зарегистрирован новый аккаунт. user-[{username}]')
            messages.success(request, f'Ваш аккаунт({username}) создан: можно войти на сайт.')
            return redirect('login')
    else:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        #  print(location(str(ip)))
        with open('media/logging/log_reg.txt', 'a') as f:
            f.write(
                f'\n{datetime.now()}: Попытка Зарегистрировать новый аккаунт. \n                 {location(str(ip))}')
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.user.username != 'tminnn':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        with open('media/logging/log_reg.txt', 'a') as f:
            f.write(
                f'\n{datetime.now()}: Переход в ЛК {request.user} ip-[{ip}]')
    return render(request, 'users/profile.html')

