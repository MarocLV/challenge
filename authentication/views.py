from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.urls import reverse

from .forms import LoginForm
# from. models import CustomUser, HitmanProfile
from .utils import check_credentials, new_user
from assignments.views import list_hits
from .models import HitmanProfile, CustomUser


def login_form(request):
    if request.session.get('user_id'):
        url = reverse('list_hits')
        return HttpResponseRedirect(url)
    else:
    
        if request.method == "POST":
           
            form = LoginForm(request.POST)
            
            
            if form.is_valid():
                
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]

                check_cred = check_credentials(email, password)
                if check_cred:
                    request.session['user_id'] = str(check_cred.id)
                    url = reverse('list_hits')
                    return HttpResponseRedirect(url)
                else:
                    messages.error(request, 'invalid credentials')
                    return HttpResponseRedirect("/auth/login/")
        else:
            form = LoginForm()
        
        return render(request, "login_form.html", {"form": form})
    

def logout(request):
    try:
        session_key = request.session.session_key
        get_session = Session.objects.get(session_key=session_key)
        get_session.delete()
    except:
        return HttpResponseForbidden("No permission")
    
    return HttpResponseRedirect("/auth/login/")


def register(request):
    if request.method == "POST":

        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = new_user(email, password)
            if user:
                return HttpResponse(f"user {user.username} registered")
            else:
                return HttpResponseBadRequest("The user could not be registered or already exists")
    else:
        form = LoginForm()
    
    return render(request, "register.html", {"form": form})


def list_hitmen(request):
    try:
        user_id = request.session.get('user_id')
        if user_id is None:
            raise ValueError("User ID not found in session")
        
        user = CustomUser.objects.get(id=user_id)
        
        if user.role.pk == 3:
            raise ValueError("User does not have the required role")
        elif user.role.pk != 3:
            h_profile = HitmanProfile.objects.filter(supervisor=user).values('id', 'user__email', 'user__id', 'user__is_active', 'user__role__name')
            profiles = [profile for profile in h_profile]
            print(profiles)
        
        return render(request, 'list_hitmen.html', {"profiles": profiles})
    
    except CustomUser.DoesNotExist:
        return HttpResponseForbidden("User does not exist")
    
    except ValueError as e:
        print(e)
        return HttpResponseForbidden("No Permission")


def hitmen_details(request, pk):
    try:
        user_id = request.session.get('user_id')
        if user_id is None:
            raise ValueError("User ID not found in session")
        
        user = CustomUser.objects.get(id=user_id)
        
        if user.role.pk == 3:
            raise ValueError("User does not have the required role")
        elif user.role.pk == 1:
            h_profile = HitmanProfile.objects.filter(supervisor=pk).values('id', 'user__username', 'user__email', 'user__id', 'user__is_active', 'user__role__name', 'user__description', 'supervisor__email')
            profiles = [profile for profile in h_profile]
            
        
        return render(request, 'list_hitmen_det.html', {"profiles": profiles})
    
    except CustomUser.DoesNotExist:
        return HttpResponseForbidden("User does not exist")
    
    except ValueError as e:
        print(e)
        return HttpResponseForbidden("No Permission")