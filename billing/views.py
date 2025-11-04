import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Customer, Bill, BillService
from services.models import ServiceCategory, Service
from .forms import CustomerForm, ServiceSelectionForm
from .utils import generate_pdf

logger = logging.getLogger('billing')


@login_required
def billing_view(request):
    # Initialize session data if not exists
    if 'selected_services' not in request.session:
        request.session['selected_services'] = []
    
    if 'customer_data' not in request.session:
        request.session['customer_data'] = {}

    # Load session data into form initial
    initial_data = request.session['customer_data']
    customer_form = CustomerForm(request.POST or None, initial=initial_data)
    service_form = ServiceSelectionForm(request.POST or None)

    selected_services = request.session['selected_services']

    # Handle POST requests
    if request.method == 'POST':
        print("=== POST REQUEST RECEIVED ===")
        print(f"POST data keys: {list(request.POST.keys())}")

        # --- Check Customer ---
        if 'check_customer' in request.POST:
            mobile = request.POST.get('mobile')
            print(f"Checking customer with mobile: {mobile}")

            if mobile and len(mobile) == 10:
                try:
                    customer = Customer.objects.get(mobile=mobile)
                    # Save customer data in session
                    request.session['customer_data'] = {
                        'name': customer.name,
                        'email': customer.email,
                        'mobile': customer.mobile
                    }
                    messages.info(request, f'Customer found: {customer.name}')
                except Customer.DoesNotExist:
                    # New customer, save entered mobile
                    request.session['customer_data'] = {'mobile': mobile}
                    messages.info(request, 'New customer - please fill details')
            else:
                messages.error(request, 'Please enter a valid 10-digit mobile number')

            return redirect('billing:billing')

        # --- Add Service ---
        elif 'add_service' in request.POST:
            # Preserve customer data before redirect
            if customer_form.is_valid():
                request.session['customer_data'] = customer_form.cleaned_data
            else:
                # Even if invalid, store what’s entered
                request.session['customer_data'] = {
                    'name': request.POST.get('name', ''),
                    'email': request.POST.get('email', ''),
                    'mobile': request.POST.get('mobile', ''),
                }

            if service_form.is_valid():
                service = service_form.cleaned_data['service']
                quantity = service_form.cleaned_data['quantity']

                # Add or update service in session
                service_data = {
                    'id': service.id,
                    'name': service.name,
                    'price': float(service.price),
                    'quantity': quantity
                }

                existing_index = next((i for i, s in enumerate(selected_services) if s['id'] == service.id), None)
                if existing_index is not None:
                    selected_services[existing_index]['quantity'] += quantity
                    messages.success(request, f'Updated {service.name} quantity to {selected_services[existing_index]["quantity"]}')
                else:
                    selected_services.append(service_data)
                    messages.success(request, f'Added {service.name} to bill')

                request.session['selected_services'] = selected_services
                service_form = ServiceSelectionForm()  # Reset
            else:
                messages.error(request, 'Please select a valid service and quantity')

            return redirect('billing:billing')

        # --- Remove Service ---
        elif 'remove_service' in request.POST:
            try:
                index = int(request.POST.get('remove_service'))
                if 0 <= index < len(selected_services):
                    removed = selected_services.pop(index)
                    request.session['selected_services'] = selected_services
                    messages.warning(request, f'Removed {removed["name"]} from bill')
            except (ValueError, IndexError):
                messages.error(request, 'Invalid service removal request.')

            return redirect('billing:billing')

        # --- Generate Bill ---
        elif 'generate_bill' in request.POST:
            print("=== GENERATE BILL BUTTON CLICKED ===")
            customer_form = CustomerForm(request.POST)

            if customer_form.is_valid():
                request.session['customer_data'] = customer_form.cleaned_data
                return generate_bill_manual(request, customer_form, selected_services)
            else:
                messages.error(request, 'Please fill all required customer fields (Name and Mobile)')

            return redirect('billing:billing')

        # --- New Bill ---
        elif 'new_bill' in request.POST:
            return reset_bill_session(request)

    # --- Calculate Bill Totals ---
    subtotal = sum(s['price'] * s['quantity'] for s in selected_services)
    tax_amount = subtotal * 0.05
    total_amount = subtotal + tax_amount

    categories = ServiceCategory.objects.prefetch_related('service_set').filter(service__is_active=True).distinct()

    # --- Render Context ---
    context = {
        'customer_form': customer_form,
        'service_form': service_form,
        'selected_services': selected_services,
        'categories': categories,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
    }

    return render(request, 'billing/billing.html', context)


@login_required
def blling_view(request):
    # Initialize session data if not exists
    if 'selected_services' not in request.session:
        request.session['selected_services'] = []
    
    if 'customer_data' not in request.session:
        request.session['customer_data'] = {}
    
    # Use session data to pre-populate the form
    initial_data = request.session['customer_data']
    customer_form = CustomerForm(request.POST or None, initial=initial_data)
    service_form = ServiceSelectionForm(request.POST or None)
    
    selected_services = request.session['selected_services']
    
    # Handle form submissions
    if request.method == 'POST':
        print("=== POST REQUEST RECEIVED ===")
        print(f"POST data keys: {list(request.POST.keys())}")
        
        if 'check_customer' in request.POST:
            mobile = request.POST.get('mobile')
            print(f"Checking customer with mobile: {mobile}")
            
            if mobile and len(mobile) == 10:
                try:
                    customer = Customer.objects.get(mobile=mobile)
                    # Update session data with customer info
                    request.session['customer_data'] = {
                        'name': customer.name,
                        'email': customer.email,
                        'mobile': customer.mobile
                    }
                    messages.info(request, f'Customer found: {customer.name}')
                    print(f"Customer found: {customer.name}")
                except Customer.DoesNotExist:
                    # Keep the mobile number in session for new customer
                    request.session['customer_data'] = {'mobile': mobile}
                    messages.info(request, 'New customer - please fill details')
                    print("New customer - mobile saved to session")
            else:
                messages.error(request, 'Please enter a valid 10-digit mobile number')
            
            # Redirect to refresh the form with updated data
            return redirect('billing:billing')
        
        elif 'add_service' in request.POST:
            if service_form.is_valid():
                service = service_form.cleaned_data['service']
                quantity = service_form.cleaned_data['quantity']
                
                # Add service to session
                service_data = {
                    'id': service.id,
                    'name': service.name,
                    'price': float(service.price),
                    'quantity': quantity
                }
                
                # Check if service already exists, update quantity if yes
                existing_index = None
                for i, s in enumerate(selected_services):
                    if s['id'] == service.id:
                        existing_index = i
                        break
                
                if existing_index is not None:
                    selected_services[existing_index]['quantity'] += quantity
                    messages.success(request, f'Updated {service.name} quantity to {selected_services[existing_index]["quantity"]}')
                else:
                    selected_services.append(service_data)
                    messages.success(request, f'Added {service.name} to bill')
                
                request.session['selected_services'] = selected_services
                service_form = ServiceSelectionForm()  # Reset form
            else:
                messages.error(request, 'Please select a valid service and quantity')
            
            return redirect('billing:billing')
        
        elif 'remove_service' in request.POST:
            service_index = int(request.POST.get('remove_service'))
            if 0 <= service_index < len(selected_services):
                removed_service = selected_services.pop(service_index)
                request.session['selected_services'] = selected_services
                messages.warning(request, f'Removed {removed_service["name"]} from bill')
            
            return redirect('billing:billing')
        
        elif 'generate_bill' in request.POST:
            print("=== GENERATE BILL BUTTON CLICKED ===")
            
            # Create a new form instance with POST data to validate
            customer_form = CustomerForm(request.POST)
            
            if customer_form.is_valid():
                print("Customer form is valid, calling generate_bill_manual")
                # Save customer data to session
                request.session['customer_data'] = customer_form.cleaned_data
                # Generate bill and redirect to success page
                return generate_bill_manual(request, customer_form, selected_services)
            else:
                print("Customer form is INVALID")
                print(f"Form errors: {customer_form.errors}")
                messages.error(request, 'Please fill all required customer fields (Name and Mobile)')
            
            return redirect('billing:billing')
        
        elif 'new_bill' in request.POST:
            return reset_bill_session(request)
    
    # Calculate totals
    subtotal = sum(service['price'] * service['quantity'] for service in selected_services)
    tax_amount = subtotal * 0.05
    total_amount = subtotal + tax_amount
    
    categories = ServiceCategory.objects.prefetch_related('service_set').filter(service__is_active=True).distinct()
    
    context = {
        'customer_form': customer_form,
        'service_form': service_form,
        'selected_services': selected_services,
        'categories': categories,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
    }
    
    return render(request, 'billing/billing.html', context)

def generate_bill_manual(request, customer_form, selected_services):
    """Generate bill without AJAX"""
    print("=== GENERATE BILL MANUAL CALLED ===")  # Debug
    print(f"Selected services count: {len(selected_services)}")  # Debug
    print(f"Customer form valid: {customer_form.is_valid()}")  # Debug
    
    if not selected_services:
        messages.error(request, 'Please add at least one service to generate bill')
        return redirect('billing:billing')
    
    try:
        # Save or get customer
        customer_data = customer_form.cleaned_data
        print(f"Customer data: {customer_data}")  # Debug
        
        customer, created = Customer.objects.get_or_create(
            mobile=customer_data['mobile'],
            defaults={
                'name': customer_data['name'],
                'email': customer_data['email']
            }
        )
        
        if not created:
            customer.name = customer_data['name']
            customer.email = customer_data['email']
            customer.save()
        
        print(f"Customer created/retrieved: {customer.name}")  # Debug
        
        # Calculate totals
        subtotal = sum(service['price'] * service['quantity'] for service in selected_services)
        tax_amount = subtotal * 0.05
        total_amount = subtotal + tax_amount
        
        print(f"Totals - Subtotal: {subtotal}, Tax: {tax_amount}, Total: {total_amount}")  # Debug
        
        # Create bill
        bill = Bill.objects.create(
            customer=customer,
            subtotal=subtotal,
            tax_amount=tax_amount,
            total_amount=total_amount,
            created_by=request.user
        )
        
        print(f"Bill created: {bill.bill_number}")  # Debug
        
        # Add services to bill
        for service_data in selected_services:
            service = Service.objects.get(id=service_data['id'])
            BillService.objects.create(
                bill=bill,
                service=service,
                quantity=service_data['quantity'],
                price=service_data['price']
            )
            print(f"Added service: {service.name}")  # Debug
        
        # Clear session
        reset_bill_session(request)
        
        print(f"Redirecting to success page with bill ID: {bill.id}")  # Debug
        messages.success(request, f'Bill #{bill.bill_number} generated successfully!')
        return redirect('billing:bill_success', bill_id=bill.id)
        
    except Exception as e:
        print(f"ERROR in generate_bill_manual: {str(e)}")  # Debug
        logger.error(f"Error generating bill: {str(e)}")
        messages.error(request, f'Error generating bill: {str(e)}')
        return redirect('billing:billing')

def reset_bill_session(request):
    """Reset the billing session"""
    request.session['selected_services'] = []
    request.session['customer_data'] = {}
    return redirect('billing:billing')

@login_required
def bill_success(request, bill_id):
    """Show bill success page"""
    print(f"=== BILL SUCCESS PAGE CALLED ===")  # Debug
    print(f"Bill ID: {bill_id}")  # Debug
    
    bill = get_object_or_404(Bill, id=bill_id)
    print(f"Bill found: {bill.bill_number}")  # Debug
    
    return render(request, 'billing/bill_success.html', {'bill': bill})
# Keep your existing utility views (they should still work)
@login_required
def download_pdf(request, bill_id):
    try:
        bill = Bill.objects.get(id=bill_id)
        pdf_buffer = generate_pdf(bill)
        
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="bill_{bill.bill_number}.pdf"'
        return response
        
    except Bill.DoesNotExist:
        messages.error(request, 'Bill not found')
        return redirect('billing:billing')
    except Exception as e:
        messages.error(request, f'Error generating PDF: {str(e)}')
        return redirect('billing:billing')

@login_required
def shae_whatsapp(request, bill_id):
    try:
        bill = Bill.objects.get(id=bill_id)
        
        # Create WhatsApp message
        message = f"""
*CURA SPA & WELLNESS - Bill Details*

*Bill Number:* {bill.bill_number}
*Customer:* {bill.customer.name}
*Mobile:* {bill.customer.mobile}
*Date:* {bill.created_at.strftime('%d-%m-%Y %H:%M')}

*Services:*
"""
        
        for bill_service in bill.billservice_set.all():
            message += f"• {bill_service.service.name} - ₹{bill_service.price} x {bill_service.quantity} = ₹{bill_service.total_price()}\n"
        
        message += f"""
*Summary:*
Subtotal: ₹{bill.subtotal}
Tax (5%): ₹{bill.tax_amount}
Discount: ₹{bill.discount}
*Total: ₹{bill.total_amount}*

Thank you for your business! 🎉
        """
        
        # URL encode the message
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        
        # Create WhatsApp URL
        whatsapp_url = f"https://wa.me/?text={encoded_message}"
        
        return redirect(whatsapp_url)
        
    except Bill.DoesNotExist:
        messages.error(request, 'Bill not found')
        return redirect('billing:billing')



from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
import urllib.parse

@login_required
def share_whatsapp(request, bill_id):
    try:
        bill = Bill.objects.get(id=bill_id)

        # ✅ Generate the same PDF as your download function
        pdf_buffer = generate_pdf(bill)

        # ✅ Save it temporarily to media/bills/
        filename = f"bill_{bill.bill_number}.pdf"
        pdf_path = f"bills/{filename}"
        default_storage.save(pdf_path, ContentFile(pdf_buffer.getvalue()))

        # ✅ Create full URL to the saved PDF
        pdf_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{pdf_path}")

        # ✅ Prepare WhatsApp message with the link
        message = f"""
*CURA SPA & WELLNESS - Bill Details*

Dear {bill.customer.name},

Your bill has been generated successfully. You can download it below:
{pdf_url}

*Bill Number:* {bill.bill_number}
*Total Amount:* ₹{bill.total_amount}
*Date:* {bill.created_at.strftime('%d-%m-%Y %H:%M')}

Thank you for choosing CURA SPA & WELLNESS 💆‍♀️💆‍♂️
"""

        # ✅ Encode and redirect to WhatsApp
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/?text={encoded_message}"
        return redirect(whatsapp_url)

    except Bill.DoesNotExist:
        messages.error(request, 'Bill not found')
        return redirect('billing:billing')
    except Exception as e:
        messages.error(request, f'Error sharing PDF: {str(e)}')
        return redirect('billing:billing')



@login_required
def bill_history(request):
    bills = Bill.objects.select_related('customer', 'created_by').prefetch_related('billservice_set').all()
    return render(request, 'billing/bill_history.html', {'bills': bills})

@login_required
def bill_detail(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    return render(request, 'billing/bill_detail.html', {'bill': bill})