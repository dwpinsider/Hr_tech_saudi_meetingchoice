# Create your views here.
from django.shortcuts import render
from django.db.models.functions import Lower

from django.core.mail import send_mail, EmailMultiAlternatives
from .forms import VendorMeetingForm
from .models import VendorPlanner, VendorMeetingRegister


#email html format
# def vendor_meeting_register(request):
#     vendors = VendorPlanner.objects.filter(is_active=True).order_by(Lower('company_name'))
#
#     if request.method == 'POST':
#         form = VendorMeetingForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             company_name = form.cleaned_data['company_name']
#             email = form.cleaned_data['email']
#             vendors = form.cleaned_data['vendors']
#             #Save the form data to the database
#             meeting_register = VendorMeetingRegister(
#                 first_name=first_name,
#                 last_name=last_name,
#                 company_name=company_name,
#                 email=email
#             )
#             meeting_register.save()
#             meeting_register.vendors.set(vendors)
#             #Prepare the list of selected delegates for the user email
#             selected_delegate_names = "<br>".join([vendor.company_name for vendor in vendors])
#
#             #email content for the user with HTML and Verdana font
#             user_subject = 'DWP Privé 2025 - Meeting Choices'
#             user_message = (f'<html><body style="font-family: Verdana;">'
#                             f'Dear {first_name.capitalize()},<br><br>'
#                             f'Thank you for submitting your choices for  DWP Privé 2025.<br><br>'
#                             f'Your selected delegates are:<br>{selected_delegate_names}<br><br>'
#                             f'We will share with you your meeting schedule closer to the event dates. '
#                             f'Your meeting schedule will comprise of Your Choices, Mutual Choices and Delegate Choices.<br><br>'
#                             f'Have a brilliant day ahead!<br><br>'
#                             f'Best regards,<br><br>'
#                             f'Team DWP</body></html>')
#
#             email_message = EmailMultiAlternatives(
#                 subject=user_subject,
#                 body='',
#                 from_email='nancy.jones@dwpcongress.net',
#                 to=[email]
#             )
#             email_message.attach_alternative(user_message, "text/html")
#             email_message.send()
#
#             #Prepare email content for the admin in HTML format
#             admin_subject = 'New Vendor meeting registration'
#             admin_message = (f'<html><body style="font-family: Verdana;">'
#                              f'A new vendor meeting registration has been submitted:<br><br>'
#                              f'First name: {first_name}<br>'
#                              f'Last name:{last_name}<br>'
#                              f'Company name: {company_name}<br>'
#                              f'Email: {email}<br>'
#                              f'Selected Delegates:<br>{selected_delegate_names}<br>'
#                              f'</body></html>')
#
#             admin_email_message = EmailMultiAlternatives(
#                 subject=admin_subject,
#                 body='',
#                 from_email='nancy.jones@dwpcongress.net',
#                 to=['nancy.jones@dwpcongress.net', 'judine@qnainternational.com','kate@qnainternational.com', 'lisa@qnainternational.com','karen@dwpcongress.net']
#             )
#             admin_email_message.attach_alternative(admin_message, "text/html")
#             admin_email_message.send()
#
#
#             # Render success template with selected delegates
#
#             return render(request, 'success.html', {'selected_Delegates': vendors})
#
#         else:
#             error_message = 'Please select at least 25 items.'
#             return render(request, 'vendor/vendor_meeting_register.html', {'form': form, 'vendors': vendors})
#
#
#
#     else:
#         form = VendorMeetingForm()
#     return render(request, 'vendor/vendor_meeting_register.html', {'form': form, 'vendors': vendors})

# Vendor meeting register want to be cloased
def vendor_meeting_register(request):
    return render(request, 'vendor/vendor_meeting_finish.html')