from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Membership
from .forms import MembershipForm

@login_required
def membership_list(request):
    memberships = Membership.objects.select_related('user').all()
    return render(request, 'membership/membership_list.html', {
        'memberships': memberships,
        'user': request.user,  # logged-in user info
    })

@login_required
def membership_create(request):
    if request.method == 'POST':
        form = MembershipForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Membership added successfully!")
            return redirect('membership')
    else:
        form = MembershipForm()
    return render(request, 'membership/membership_form.html', {'form': form, 'title': 'Add Member'})

@login_required
def membership_edit(request, pk):
    membership = get_object_or_404(Membership, pk=pk)
    if request.method == 'POST':
        form = MembershipForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
            messages.success(request, "Membership updated successfully!")
            return redirect('membership')
    else:
        form = MembershipForm(instance=membership)
    return render(request, 'membership/membership_form.html', {'form': form, 'title': 'Edit Member'})

@login_required
def membership_delete(request, pk):
    membership = get_object_or_404(Membership, pk=pk)
    membership.delete()
    messages.success(request, "Membership deleted successfully!")
    return redirect('membership')
