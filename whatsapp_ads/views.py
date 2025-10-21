from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import WhatsAppUser
from .forms import WhatsAppUserForm
from .utils import send_whatsapp_message

def user_list(request):
    users = WhatsAppUser.objects.all()
    return render(request, 'whatsapp_ads/user_list.html', {'users': users})

def user_create(request):
    if request.method == 'POST':
        form = WhatsAppUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"{user.name} added successfully!")
            
            # If VIP, send poster
            if user.membership_type == 'vip':
                send_whatsapp_message(
                    user.mobile,
                    "Thank you for being a VIP member! 🎉 Here’s your exclusive poster.",
                    media_url="https://yourdomain.com/static/poster_vip.jpg"
                )
            return redirect('whatsapp_ads:user_list')
    else:
        form = WhatsAppUserForm()
    return render(request, 'whatsapp_ads/user_form.html', {'form': form})

def user_update(request, pk):
    user = get_object_or_404(WhatsAppUser, pk=pk)
    if request.method == 'POST':
        form = WhatsAppUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"{user.name} updated successfully!")
            return redirect('whatsapp_ads:user_list')
    else:
        form = WhatsAppUserForm(instance=user)
    return render(request, 'whatsapp_ads/user_form.html', {'form': form})

def user_delete(request, pk):
    user = get_object_or_404(WhatsAppUser, pk=pk)
    user.delete()
    messages.warning(request, f"{user.name} deleted successfully.")
    return redirect('whatsapp_ads:user_list')
