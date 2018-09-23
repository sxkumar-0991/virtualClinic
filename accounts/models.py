from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin,AbstractBaseUser,BaseUserManager
from django.core.validators import EmailValidator, RegexValidator
from django.urls import reverse

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email address.")
        email = self.normalize_email(email)
        customuser = self.model(email=email)
        customuser.set_password(password)
        customuser.save(using=self._db)
        return customuser

    def create_superuser(self, email, password):
        customuser = self.create_user(email=email, password=password)
        customuser.is_staff = True
        customuser.is_admin = True
        customuser.is_superuser = True
        customuser.save(using=self._db)
        return customuser




class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email ID'), unique=True, max_length=255)
    is_active = models.BooleanField(_('Active'),default=True)
    is_doctor = models.BooleanField(_('User is Doctor'), default=False)
    is_patient = models.BooleanField(_('User is Patient'), default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(_('User is Admin'), default=False)


    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_absolute_url(self):
        return reverse('accounts:home')

    def __str__(self):
        k = str(self.id)
        return k

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True



class Doctor(models.Model):
    doctor_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    first_name = models.CharField(_('First Name'), max_length=250, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=250, blank=True)
    mobile_regex = RegexValidator(regex=r'\d{10}', message="Enter valid 10 digits mobile number")
    mobileno = models.CharField(_('Mobile Number'), validators=[mobile_regex], max_length=10)
    date_of_birth = models.DateField(_('Date of Birth'), max_length=8)

    Gender_Options = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender'),
    )

    gender = models.CharField(_('Gender'), max_length=1, choices=Gender_Options, blank=True, help_text="Please select your gender.")
    speciality = models.CharField(_('Speciality'), max_length=250)
    years_of_experience = models.IntegerField(_('Years of Experience'))
    city = models.CharField(_('City'), max_length=200)
    patient_count = models.IntegerField(_('Count of Patients assigned'), default=0)
    image = models.ImageField(upload_to='Profile Image/doctor_profile_image/', blank=True)
    last_access = models.DateTimeField(_('Last Login Time'), null=True)
    degree = models.CharField(_('Medical Degree'), max_length=300)
    join_date = models.DateField(_('Join Date'), null=False)
    medical_registration_no = models.CharField(_('Unique Permanent Registration Number'), max_length=100)

    class Meta:
        db_table='doctor'
        ordering = ["years_of_experience", "doctor_id"]

    def get_url(self):
        return reverse('accounts:doctordetail', args=[str(self.id)])

    def getMap_url(self):
        return reverse('accounts:docLocator', args=[str(self.id)])

    def __str__(self):
        k = str(self.id)
        return k



class DoctorAddress(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False, blank=False)
    clinic_name = models.CharField(_('Hospital/Clinic Name'), max_length=350, null=False, blank=False)
    clinic_address = models.CharField(_('Hospital/Clinic Address'), max_length=450, null=False, blank=False)
    lat = models.DecimalField(max_digits=10, decimal_places=6, null=False)
    lng = models.DecimalField(max_digits=10, decimal_places=6, null=False)

    class Meta:
        db_table='doctor_address'
        ordering = ["doctor"]


class Patient(models.Model):
    patient_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    first_name = models.CharField(_('First Name'), max_length=250, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=250, blank=True)
    patient_pin = models.CharField(_('Patient Device Pin'),max_length=7, null=True)

    mobile_regex = RegexValidator(regex=r'\d{10}', message="Enter valid 10 digits mobile number")
    mobileno = models.CharField(_('Mobile Number'),validators=[mobile_regex], max_length=10)
    date_of_birth = models.DateField(_('Date of Birth'),max_length=8)


    Gender_Options = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender'),
    )

    gender = models.CharField(_('Gender'),max_length=1, choices=Gender_Options, blank=True, help_text="Please select your gender.")
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(_('City'),max_length=100)
    doc_assigned = models.BooleanField(_('Doctor Assigned'), default=False)
    has_device = models.BooleanField(_('Has Device'), default=False)
    image = models.ImageField(upload_to='Profile Image/patient_profile_image', blank=True)
    last_access = models.DateTimeField(_('Last Login Time'), null=True)
    join_date = models.DateField(_('Join Date'),null=False)

    class Meta:
        db_table = 'patient'
        ordering = ["date_of_birth"]

    def get_url(self):
        return reverse('accounts:patientdetail', args=[str(self.id)])

    def get_json_data(self):
        return reverse('accounts:get_Patient_Readings_data_as_json_fromDB' , args=[str(self.id)])

    def __str__(self):
        """
        String for representing the model object.
        """
        k = str(self.id)
        return k


class PatientAddress(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False, blank=False)
    address = models.CharField(_('Patient Address'), max_length=450, null=True, blank=True)

    class Meta:
        db_table='patient_address'
        ordering = ["patient"]



class Device(models.Model):
    """
    Model representing a Device.
    """

    deviceid = models.CharField(_('Device ID'), unique=True, max_length=7 , help_text="Bluetooth pin of the devce.")
    year_of_manufacture = models.DateField(_('Manufacturing Year'), max_length=8)
    patient = models.ForeignKey(Patient,on_delete=models.PROTECT, null=True, blank=True)
    product_id = models.CharField(_('Product ID'), unique=True, max_length=4, null=True, help_text="Unique Product ID of the device." )


    class Meta:
        db_table = 'device'
        ordering = ["year_of_manufacture", "patient"]

    def __str__(self):
        k = str(self.id)
        return k


class Readings(models.Model):
    """
    Model representing Readings.
    """

    patient_id = models.ForeignKey(Patient, on_delete=models.PROTECT, null=False)
    blood_pressure_Systolic  = models.CharField(_('Systolic Blood Pressure'), max_length=3)
    blood_pressure_Diastolic = models.CharField(_('Diastolic Blood Pressure'), max_length=3)
    heart_beat = models.CharField(_('HeartBeats per Minute'), max_length=3)
    SpO2 = models.CharField(_('SpO2 value'), max_length=6)
    body_temperature = models.CharField(_('Body Temperature'), max_length=3)
    date_time = models.DateTimeField(_('Date & Time'))

    class Meta:
        db_table = 'readings'
        ordering = ["-date_time"]

    def __str__(self):
        k = str(self.id)
        return k


class Relative(models.Model):
    """
    Model representing relatives.
    """

    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False)
    first_name = models.CharField(_('First Name'), max_length=250)
    last_name = models.CharField(_('Last Name'), max_length=250)
    Gender_Options = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender'),
    )

    gender = models.CharField(_('Gender'), max_length=1, choices=Gender_Options, blank=True, help_text="Please select your gender.")
    date_of_birth = models.DateField(_('Date of Birth'), max_length=8)
    mobile_regex = RegexValidator(regex=r'\d{10}', message="Enter valid 10 digits mobile number")
    mobileno = models.CharField(_('Mobile Number'), validators=[mobile_regex], max_length=10)
    relation_to_user = models.CharField(_('Relation with User'), max_length=150)


    class Meta:
        db_table = 'relative'
        ordering = ["patient_id","first_name","relation_to_user"]

    def get_absolute_url(self):
        return reverse('accounts:relative-detail', args=[self.id])


    def __str__(self):
        k = str(self.id)
        return k




