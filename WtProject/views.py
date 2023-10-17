import json
import os
from django.db.models import Max
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from WtProject import settings
from appuser.models import AppUser
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        print(form.data)
        if form.is_valid() or True:
            print('valid')
            # Access form field values
            full_name = form.cleaned_data['full_name']
            print(full_name)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            address = form.cleaned_data['address']
            pin_code = form.cleaned_data['pin_code']
            gender = form.cleaned_data['gender']
            picture_path = form.cleaned_data['picture_path']  

            max_sequence = AppUser.objects.aggregate(Max('user_name_sequence'))['user_name_sequence__max']
            if max_sequence is None:
                user_name_sequence = 10001
            else:
                user_name_sequence = int(max_sequence) + 1
        
            username = full_name[:1] + str(user_name_sequence)

            # Example: Create a new user
            user = AppUser.objects.create_user(username=username , user_name_sequence = user_name_sequence, full_name = full_name, email=email, password = password, gender = gender, address = address, pin_code = pin_code)
            
            # Additional logic for saving the profile picture if provided
            if picture_path:
                user.picture_path = picture_path
                user.save()

            # Log the user in
            login(request, user)
            
            # Redirect to a success page or home page
            return redirect('home') 
    else:
        form = RegistrationForm()
    
    return render(request, 'registration.html', {'form': form})    

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            username = AppUser.objects.get(username=username).username
        except AppUser.DoesNotExist:
            try:
                username = AppUser.objects.get(email=username).username
            except AppUser.DoesNotExist:
                pass
        print(username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Authentication with username failed, try with email
            email = request.POST['username']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

        # Handle invalid login credentials
        pass
    return render(request, 'login.html')    

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    user = request.user
    user_pin_code = user.pin_code
    username = user.username

    app_users = AppUser.objects.raw(
        "SELECT * FROM appuser_appuser u WHERE u.pin_code = %s AND u.username != %s AND u.id NOT IN (SELECT to_appuser_id FROM appuser_appuser_friends WHERE from_appuser_id = %s)",
        [user_pin_code, username, user.id]
    )
    
    app_users_list = list(app_users)
    data = {
        'logged_user': user,
        'app_users': app_users_list,
    }
    return render(request, 'home.html', data)

@login_required
def profile(request): 
    friends = request.user.friends.all()
    data = {
        'friends': friends,
    }
    return render(request, 'profile.html', data)

def add_friend(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id')
        try:
            logged_in_user = request.user

            user_to_add = AppUser.objects.get(id=user_id)

            logged_in_user.friends.add(user_to_add)

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': str(e)})

    return JsonResponse({'success': False})

def remove_friend(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id')
        try:
            logged_in_user = request.user

            user_to_remove = AppUser.objects.get(id=user_id)

            if user_to_remove in logged_in_user.friends.all():
                logged_in_user.friends.remove(user_to_remove)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error_message': 'User is not in your friends list.'})

        except AppUser.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'User does not exist.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': str(e)})

    return JsonResponse({'success': False})    