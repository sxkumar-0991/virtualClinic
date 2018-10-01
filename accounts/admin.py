from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Doctor, Patient, Device, Relative, Readings
from django.contrib.auth.forms import ReadOnlyPasswordHashField

admin.site.register(Relative)
admin.site.register(Readings)

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput, help_text="Enter same Password value")

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError("Passwords didn't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_active', 'is_staff', 'is_admin', 'is_doctor', 'is_patient')

    def clean_password(self):
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_admin', 'is_doctor',  'is_patient')
    list_filter = ('is_admin',)
    fieldsets = (
        ('General Information', {'fields':('email', 'password')}),
        ('User Type', {'fields':('is_doctor', 'is_patient')}),
        ('Permissions', {'fields':('is_admin','is_staff')}),
    )
    add_fieldsets = (
        (None, {'classes':('wide',), 'fields':('email','password1', 'password2')}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()



admin.site.register(CustomUser,UserAdmin)
admin.site.unregister(Group)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'first_name', 'doctor')
    fieldsets = (('General Information', {'fields': ('patient_id', 'first_name', 'last_name', 'mobileno', 'date_of_birth', 'gender', 'city')}),
                 ('Doctor Information', {'fields': ('doc_assigned', 'doctor')}), ('Device Information', {'fields':('has_device',)}))


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'first_name', 'speciality', 'years_of_experience', 'patient_count')
    fieldsets = (('General Information', {'fields': ('doctor_id', 'first_name', 'last_name', 'mobileno', 'date_of_birth', 'gender', 'city')}),
                 ('Professional Information', {'fields': ('speciality', 'years_of_experience', 'patient_count')}))


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('deviceid', 'year_of_manufacture', 'patient', 'product_id')
