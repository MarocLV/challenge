from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models import Q

from .models import HitAssignation
from authentication.models import CustomUser, HitmanProfile
from .forms import HitmanAssignationForm, HitCreation


def assign_hitman(request):
    try:
        user_id = request.session.get('user_id')
        if user_id is None:
            raise ValueError("User ID not found in session")
        
        user = CustomUser.objects.get(id=user_id)
        
        if user.role.pk != 1:
            raise ValueError("User does not have the required role")
        
        if request.method == "POST":
            form = HitmanAssignationForm(request.POST)
            
            if form.is_valid():
                hitman = form.cleaned_data['user']
                supervisor = form.cleaned_data['supervisor']
                
                new_hitman = HitmanProfile.objects.create(user=hitman, supervisor=supervisor)
                
                return HttpResponse(f"Hitman {hitman.email} assigned to {supervisor.email}")
        else:
            form = HitmanAssignationForm()
        
        return render(request, "hitman_assign.html", {"form": form})
    
    except CustomUser.DoesNotExist:
        return HttpResponseForbidden("User does not exist")
    
    except ValueError as e:
        print(e)
        return HttpResponseForbidden("No Permission")



def list_hits(request):
    user_id = request.session.get('user_id')
    if request.method == "GET":
        user = CustomUser.objects.get(id=user_id)
        if user.role.pk == 1:
            hit_list = HitAssignation.objects.all().values()
            print(hit_list, "boss")
        elif user.role.pk == 2:
            hit_list = HitAssignation.objects.filter(Q(assignee__user__pk=user_id) | Q(assignee__supervisor__pk=user_id)).values()
            print(hit_list, "manager")
        elif user.role.pk == 3:
            hit_list = HitAssignation.objects.filter(assignee__user__pk=user_id).values()
            print(hit_list, "hitman")
        hit_list = [hit for hit in hit_list]
        print(hit_list)
        return render(request, 'hits_list.html', {'hits': hit_list})
    

# def hits_details(request, id):
#     if request.method == "POST":
#         # create a form instance and populate it with data from the request:
#         form = LoginForm(request.POST)
        
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             email = form.cleaned_data["email"]
#             password = form.cleaned_data["password"]

#             user = new_user(email, password)
#             if user:
#                 return HttpResponse(f"user {user.username} registered")
#             else:
#                 return HttpResponseBadRequest("The user could not be registered or already exists")
#             # ...
#             # redirect to a new URL:
            
#         # if a GET (or any other method) we'll create a blank form
#     else:
#         form = LoginForm()
    
#     return render(request, "register.html", {"form": form})


def create_hit(request):
    try:
        user_id = request.session.get('user_id')
        if user_id is None:
            raise ValueError("User ID not found in session")
        
        user = CustomUser.objects.get(id=user_id)
        
        if user.role.pk == 3:
            raise ValueError("User does not have the required role")
        elif user.role.pk != 3:
            h_profile = HitmanProfile.objects.filter(user=user).first()
         
        if request.method == "POST":
           
            form = HitCreation(request.POST)
            
            
            if form.is_valid():
                
                target_name = form.cleaned_data["target_name"]
                description = form.cleaned_data["description"]

                new_hit = HitAssignation.objects.create(target_name=target_name, description=description, creator=h_profile)
                
                
                return HttpResponse(f"Hit with id {new_hit.pk} created")
            
        else:
            form = HitCreation()
        
        return render(request, "hit_creation.html", {"form": form})
    
    except CustomUser.DoesNotExist:
        return HttpResponseForbidden("User does not exist")
    
    except ValueError as e:
        print(e)
        return HttpResponseForbidden("No Permission")