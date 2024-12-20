from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Profile
from decouple import config # type: ignore
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os
import requests

GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = config("REDIRECT_URI")

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            profile = Profile.objects.create(user=user)
            profile.save()
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

@login_required(login_url='common:login')
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('common:profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'common/profile.html', {'form': form})

def googlelogin(request):
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid email profile"
    )
    return redirect(google_auth_url)

def callback(request):
    code = request.GET.get("code")
    if not code:
        return "Authorization Failed"
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_response = requests.post(token_url, token_data)
    if token_response.status_code != 200:
        return f"Failed to fetch token: {token_response.json()}"
    
    token_info = token_response.json()
    access_token = token_info.get("access_token")
    id_token_value = token_info.get("id_token")
    
    try:
        id_info = id_token.verify_oauth2_token(
            id_token_value,
            google_requests.Request(),
            GOOGLE_CLIENT_ID
        )
        email = id_info["email"]
        name = id_info.get("name", "Unknown")
    except ValueError:
        return "Invalid token"

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        username = name
        user = User.objects.create_user(username=username, email=email)
        user.save()
        profile = Profile.objects.create(user=user)
        download_profile(id_info["picture"], email)
        profile.avatar = "profile_images/" + email
        profile.save()

    login(request, user)
    
    return redirect('/')

def download_profile(url, filename):
    media_path = os.path.join(settings.MEDIA_ROOT, "profile_images" , filename)
    try:
        response = requests.get(url, stream=True)
        with open(media_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    except requests.exceptions.RequestException as e:
        print(e)
    