
from django.shortcuts import render
from django.db.models.functions import Lower

from django.core.mail import send_mail, EmailMultiAlternatives
from .forms import DelegateMeetingForm
from .models import Delegate ,DelegateMeetingRegister

# Create your views here.

#delegate meeting register
def delegate_meeting_register(request):
    delegates = Delegate.objects.filter(is_active=True)

    if request.method == 'POST':
        form = DelegateMeetingForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            company_name = form.cleaned_data['company_name']
            email = form.cleaned_data['email']
            day_of_participation = form.cleaned_data['day_of_participation']
            delegates = form.cleaned_data['delegates']

            #Save the form data to the database
            meeting_register = DelegateMeetingRegister(
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                email=email,
                day_of_participation=day_of_participation,


            )
            meeting_register.save()
            meeting_register.delegates.set(delegates)

            #Prepare the list of selected delegates for the user email
            selected_vendor_names = "<br>".join([delegate.company_name for delegate in delegates])

            #Prepare email content for the user with HTML and Verdana font
            user_subject = 'HR Tech Saudi Summit 2025 - Meeting Choices'
            user_message = (f'<html><body style="font-family: Verdana;">'
                            f'Dear {first_name.capitalize()},<br><br>'
                            f'Thank you for submitting your choices for  HR Tech Saudi Summit 2025.<br><br>'
                            f'Your selected vendors are:<br>{selected_vendor_names}<br><br>'
                            f'We will share with you your meeting schedule closer to the event dates. '
                            f'Have a brilliant day ahead!<br><br>'
                            f'Best regards,<br><br>'
                            f'Team HRTS</body></html>')

            email_message = EmailMultiAlternatives(
                subject=user_subject,
                body='',
                from_email='fatima@hrtechsaudi.com',
                to=[email]
            )
            email_message.attach_alternative(user_message, "text/html")
            email_message.send()

            # Prepare email content for the admin with HTML
            admin_subject = 'New delegate meeting registration'
            admin_message = (f'<html><body>'
                             f'A new delegate meeting registration has been submitted:<br><br>'
                             f'First name: {first_name}<br>'
                             f'Last name: {last_name}<br>'
                             f'Company name: {company_name}<br>'
                             f'Email: {email}<br>'


                             f'Selected vendors:<br>{selected_vendor_names}</body></html>')

            admin_email_message = EmailMultiAlternatives(
                subject=admin_subject,
                body='',
                from_email='fatima@hrtechsaudi.com',
                to=['fatima@hrtechsaudi.com', 'jacqueline@hrtechsaudi.com']
            )
            admin_email_message.attach_alternative(admin_message, "text/html")
            admin_email_message.send()



            # Render success template with selected delegates
            return render(request, 'success.html', {'selected_delegates': delegates})
        else:
            error_message = 'Please select at least 30 items.'
            return render(request, 'delegate/delegate_meeting_register.html',
                          {'form': form, 'error_message': error_message, 'delegates': delegates})
    else:
        form = DelegateMeetingForm()

    return render(request, 'delegate/delegate_meeting_register.html', {'form': form, 'delegates': delegates})


# registration closed
# def delegate_meeting_register(request):
#     return render(request, 'delegate/delegate_meeting_finish.html')



