from django import forms
from .models import Delegate


class DelegateMeetingForm(forms.Form):
    Day_Choices = [
        ('Day 1 - 3rd November', 'Day 1 - 3rd November'),
        ('Day 2 - 4th November', 'Day 2 - 4th November'),
        ('Both Days', 'Both Days')

    ]
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    company_name = forms.CharField(label='Company Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    day_of_participation = forms.MultipleChoiceField(
        label='Day of Participation',
        choices=Day_Choices,
        widget=forms.CheckboxSelectMultiple
    )

    delegates = forms.ModelMultipleChoiceField(
        queryset= Delegate.objects.filter(is_active=True),
        label = 'Select at least 30 vendors',
        widget = forms.CheckboxSelectMultiple(),
        help_text='You can select multiple vendors by holding down the Ctrl key (Windows) or the Command key (Mac).'
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delegates'].required = True
        self.fields['delegates'].error_messages['required'] = 'Please select at least 40 Vendors.'


class DelegateMeetingFormBootstrap(DelegateMeetingForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget_class = 'form-control'

            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                widget_class = 'form-check-input'
            elif isinstance(field.widget, forms.CheckboxInput):
                widget_class = 'form-check-input'
            elif isinstance(field.widget, forms.RadioSelect):
                widget_class = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                widget_class = 'form-select'

            field.widget.attrs.update({
                'class': widget_class,
                'placeholder': field.label,
                'aria-label': field.label,
            })
