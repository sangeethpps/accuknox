from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import User


def sign_up(request):
    context = {"exceptions": "","button_name": "Login", "button_url":"/core/login/"}
    if request.method == "POST":
        try:
            if request.POST['password1'] != request.POST['password2']:
                raise ValueError('Both Passwords Do Not Match !!')
            if User.objects.filter(email=request.POST['username']).exists():
                raise ValueError('User Already Exists Please Sign In')
            else:
                user_obj = User.objects.create_user(email=request.POST['username'], password=request.POST['password1'])
                login(request, user_obj)
                context["button_name"] = "Logout"
                context["button_url"] = "/core/logout"
                return redirect('/core/home', context=context)
        except Exception as e:
            context['exceptions'] = str(e)
            return render(template_name='signup.html', request=request, context=context)
    else:
        return render(template_name='signup.html', request=request, context=context)


def sign_in(request):
    context = {'button_name': 'Login', 'button_url': "/core/login", "exceptions": ""}
    try:
        if request.method == "POST":
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            if user:

                login(request, user)
                context["button_name"] = "Logout"
                context["button_url"] = "/core/logout"
                return redirect('/home', context=context)
            else:
                raise ValueError('Credentials Invalid !!!')
    except Exception as e:
        context["exceptions"] = str(e)
    return render(template_name='login.html', request=request, context=context)


@login_required
def home(request):
    context = {'button_name': 'Logout', 'button_url': "/core/logout"}
    return render(template_name='home.html', request=request, context=context)


def logout_view(request):
    context = {'button_name': 'Login', 'button_url': "/core/login"}
    logout(request)
    return redirect('/login/', context=context)
