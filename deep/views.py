from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from .models import User, Poster
from .forms import UserForm, PosterForm
import urllib.parse

def user_list(request):
    users = User.objects.all().order_by('-created_at')
    return render(request, 'users/user_list.html', {'users': users})

def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'users/user_form.html', {'form': form, 'title': 'Create User'})

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form, 'title': 'Update User'})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})

def share_poster(request, poster_id):
    poster = get_object_or_404(Poster, id=poster_id)
    
    # Create WhatsApp share message
    message = f"Check out this poster: {poster.title}"
    if poster.description:
        message += f"\n\n{poster.description}"
    
    # URL encode the message for WhatsApp
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/?text={encoded_message}"
    
    return redirect(whatsapp_url)

def vip_posters(request):
    posters = Poster.objects.filter(is_active=True)
    return render(request, 'users/vip_posters.html', {'posters': posters})

def poster_list(request):
    posters = Poster.objects.filter(is_active=True)
    return render(request, 'users/poster_list.html', {'posters': posters})

def poster_create(request):
    if request.method == 'POST':
        form = PosterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('poster_list')
    else:
        form = PosterForm()
    return render(request, 'users/poster_form.html', {'form': form, 'title': 'Create Poster'})