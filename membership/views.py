from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Membership
from .forms import MembershipForm

# List all memberships
class MembershipListView(ListView):
    model = Membership
    template_name = 'membership/membership_list.html'
    context_object_name = 'memberships'

# Create new membership
class MembershipCreateView(CreateView):
    model = Membership
    form_class = MembershipForm
    template_name = 'membership/membership_form.html'
    success_url = reverse_lazy('membership_list')

# Update existing membership
class MembershipUpdateView(UpdateView):
    model = Membership
    form_class = MembershipForm
    template_name = 'membership/membership_form.html'
    success_url = reverse_lazy('membership_list')

# Delete membership
class MembershipDeleteView(DeleteView):
    model = Membership
    template_name = 'membership/membership_confirm_delete.html'
    success_url = reverse_lazy('membership_list')

# View membership details
class MembershipDetailView(DetailView):
    model = Membership
    template_name = 'membership/membership_detail.html'
    context_object_name = 'membership'
