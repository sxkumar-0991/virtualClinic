from django import forms
#from django.contrib.auth.forms import UserCreationForm
from .admin import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import datetime, uuid
import re
from django.utils.translation import ugettext_lazy

class Register_patient_doctor(UserCreationForm):

    email_regex = RegexValidator(regex=r'[\w\S]+@\w+.\w{2,3}', message="Enter valid email id.")
    email = forms.EmailField(label="Email ID", required=True, validators=[email_regex])

    #password = forms.CharField(label="Password", required=True,)
    #renter_password = forms.CharField(label="Renter Password", required=True)


    class Meta:
        model = CustomUser
        fields = ('email', 'password1')

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email ID already exists, enter a different id for registration.")
        return email



class Doctor_details(forms.Form):
    Profile_pic = forms.ImageField(label=ugettext_lazy('Profile Picture'), required=True)
    first_name = forms.CharField(label="First Name", required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Enter First Name",
            'style': "padding: 5px; margin-bottom: 5px;"
        }))
    last_name = forms.CharField(label="Last Name", required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Enter Last Name",
            'style': "padding: 5px; margin-bottom: 5px;"
        }))
    mobile_regex = RegexValidator(regex=r'\d{10}', message="Mobile number should be of 10 digits")
    mobileno = forms.CharField(label="Mobile Number", required=True, max_length=10, validators=[mobile_regex], widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "10 digits Mobile Number",
            'style': "padding: 5px; margin-bottom: 5px;"
        }
    ))
    date_of_birth = forms.DateField(label="Date Of Birth", required=True, input_formats=('%d/%m/%Y',),widget=forms.DateInput(
        attrs={
            'class': 'form-control',
            'placeholder': "dd/mm/yyyy",
            'style': "padding: 5px; margin-bottom: 5px;"
        }))

    def clean_Profile_pic(self):
        pic = self.cleaned_data['Profile_pic']
        if pic is None:
            raise forms.ValidationError(ugettext_lazy("You have not uploaded your profile picture. It is required to avail best services from the Doctor."))
        return pic

    def clean_date_of_birth(self):
        data = self.cleaned_data['date_of_birth']
        if data > datetime.date.today():
            raise forms.ValidationError(ugettext_lazy("Date of Birth should be in the Past"))

        return data

    def clean_mobileno(self):
        mobileno = str(self.cleaned_data['mobileno'])
        pattern = r'^[6-9]\d{9}$'
        if re.search(pattern,mobileno):
            return mobileno
        else:
            raise forms.ValidationError(ugettext_lazy("Mobile number is invalid"))


    Gender_Options = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('T', 'Transgender'),
    )

    gender = forms.ChoiceField(choices=Gender_Options, label="Gender", required=True, widget=forms.Select(
        attrs={
            'class': 'form-control',
            'style': "padding: 5px; margin-bottom: 5px;"
        }))
    speciality = forms.CharField(label="Field of Specialization", required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Field of Specialization",
            'style': "padding: 5px; margin-bottom: 5px;"
        }))
    years_of_experience = forms.IntegerField(label="Years of Experience", required=True, widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Experience years",
            'style': "padding: 5px; margin-bottom: 5px;"
        }))
    city = forms.CharField(label="City", required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Where you Practice...",
            'style': "padding: 5px; margin-bottom: 5px;"
        }
    ))
    degree = forms.CharField(label="Medical Degrees", required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Medical degrees you hold",
            'style': "padding: 5px; margin-bottom: 5px;"
        }
    ))
    medical_registration_no = forms.CharField(label="Unique Permanent Registration Number", required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Enter Registration no....",
            'style': "padding: 5px; margin-bottom: 5px;"
        }
    ))




class Patient_details(forms.Form):
    Profile_pic = forms.ImageField(label=ugettext_lazy('Profile Picture'), required=True)
    first_name = forms.CharField(label="First Name", required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Enter First Name",
            'style': "padding: 5px; margin-bottom: 5px;"
        }))
    last_name = forms.CharField(label="Last Name", required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Enter Last Name",
            'style': "padding: 5px; margin-bottom: 5px;"
        }))
    mobile_regex = RegexValidator(regex=r'\d{10}', message="Mobile number should be of 10 digits")
    mobileno = forms.CharField(label="Mobile Number", required=True, max_length=10, validators=[mobile_regex],
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': "10 digits Mobile Number",
                                       'style': "padding: 5px; margin-bottom: 5px;"
                                   }
                               ))
    date_of_birth = forms.DateField(label="Date Of Birth", required=True, input_formats=('%d/%m/%Y',),
                                    widget=forms.DateInput(
                                        attrs={
                                            'class': 'form-control',
                                            'placeholder': "dd/mm/yyyy",
                                            'style': "padding: 5px; margin-bottom: 5px;"
                                        }))

    def clean_Profile_pic(self):
        pic = self.cleaned_data['Profile_pic']
        if pic is None:
            raise forms.ValidationError(ugettext_lazy("You have not uploaded your profile picture. It is required to avail best services from the Doctor."))
        return pic

    def clean_mobileno(self):
        mobileno = str(self.cleaned_data['mobileno'])
        pattern = r'^[6-9]\d{9}$'
        if re.search(pattern,mobileno):
            return mobileno
        else:
            raise forms.ValidationError(ugettext_lazy("Mobile number is invalid"))

    def clean_date_of_birth(self):
        data = self.cleaned_data['date_of_birth']
        if data > datetime.date.today():
            raise forms.ValidationError(ugettext_lazy("Date of Birth should be in the Past"))

        return data

    Gender_Options = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('T', 'Transgender'),
    )

    gender = forms.ChoiceField(choices=Gender_Options, label="Gender", required=True, widget=forms.Select(
        attrs={
            'class': 'form-control',
            'style': "padding: 5px; margin-bottom: 5px;"
        }))
    city = forms.CharField(label="City", required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Where you Practice...",
            'style': "padding: 5px; margin-bottom: 5px;"
        }
    ))



class Relative_details(forms.Form):
    first_name = forms.CharField(label=ugettext_lazy('First Name'), required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Enter First Name",
            'style': "padding: 5px; margin-bottom: 5px;"
        }
    ))
    last_name = forms.CharField(label=ugettext_lazy('Last Name'), required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Enter First Name",
            'style': "padding: 5px; margin-bottom: 5px;"
        }
    ))

    Gender_Options = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('T', 'Transgender'),
    )

    gender = forms.ChoiceField(choices=Gender_Options, label="Gender", required=True, widget=forms.Select(
        attrs={
            'class': 'form-control',
            'style': "padding: 5px; margin-bottom: 5px;"
        }))
    date_of_birth = forms.DateField(label="Date Of Birth", required=True, widget=forms.DateInput(
        attrs={
            'class': 'form-control',
            'placeholder': "dd/mm/yyyy",
            'style': "padding: 5px; margin-bottom: 5px;"
        }, format='%d/%m/%Y'), input_formats=('%d/%m/%Y',))

    mobile_regex = RegexValidator(regex=r'\d{10}', message="Mobile number should be of 10 digits")
    mobileno = forms.CharField(label="Mobile Number", required=True, max_length=10, validators=[mobile_regex],
                                widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "10 digits Mobile Number",
                'style': "padding: 5px; margin-bottom: 5px;"
            }
        ))
    relation_to_user = forms.CharField(label=ugettext_lazy('Relation with You'), required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'style': "padding: 5px; margin-bottom: 5px;"
        }))


    def clean_mobileno(self):
        mobileno = str(self.cleaned_data['mobileno'])
        pattern = r'^[6-9]\d{9}$'
        if re.search(pattern,mobileno):
            return mobileno
        else:
            raise forms.ValidationError(ugettext_lazy("Mobile number is invalid"))

    def clean_date_of_birth(self):
        data = self.cleaned_data['date_of_birth']
        if data > datetime.date.today():
            raise forms.ValidationError(ugettext_lazy("Date of Birth should be in the Past"))

        return data



