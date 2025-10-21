from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import ServiceCategory, Service
from .forms import ServiceCategoryForm, ServiceForm

@login_required
def service_list(request):
    services = Service.objects.select_related('category').all()
    return render(request, 'services/service_list.html', {'services': services})

@login_required
def category_list(request):
    categories = ServiceCategory.objects.prefetch_related('service_set').all()
    return render(request, 'services/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('services:category_list')
    else:
        form = ServiceCategoryForm()
    return render(request, 'services/category_form.html', {'form': form, 'title': 'Create Category'})

@login_required
def category_edit(request, pk):
    category = get_object_or_404(ServiceCategory, pk=pk)
    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('services:category_list')
    else:
        form = ServiceCategoryForm(instance=category)
    return render(request, 'services/category_form.html', {'form': form, 'title': 'Edit Category'})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(ServiceCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('services:category_list')
    return render(request, 'services/category_confirm_delete.html', {'category': category})

@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service created successfully!')
            return redirect('services:service_list')
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form, 'title': 'Create Service'})

@login_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully!')
            return redirect('services:service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form, 'title': 'Edit Service'})

@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully!')
        return redirect('services:service_list')
    return render(request, 'services/service_confirm_delete.html', {'service': service})

@login_required
def get_services_api(request):
    category_id = request.GET.get('category_id')
    if category_id:
        services = Service.objects.filter(category_id=category_id, is_active=True)
    else:
        services = Service.objects.filter(is_active=True)
    
    services_data = []
    for service in services:
        services_data.append({
            'id': service.id,
            'name': service.name,
            'price': float(service.price),
            'duration': service.duration,
            'category_id': service.category.id,
            'category_name': service.category.name
        })
    
    return JsonResponse({'services': services_data})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(ServiceCategory, pk=pk)
    
    # Check if category has services
    if category.service_set.exists():
        messages.error(request, f'Cannot delete category "{category.name}" because it has services associated with it.')
        return redirect('services:category_list')
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('services:category_list')
    
    return render(request, 'services/category_confirm_delete.html', {'category': category})