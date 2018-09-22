from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate,login, logout
from .Registrationform import Register_patient_doctor, Doctor_details, Patient_details, Relative_details
from django.urls import reverse
from datetime import datetime
from django.db.models import Q,Count
from django.contrib.sessions.backends.base import SessionBase
from django.http import HttpResponseRedirect,HttpResponse,HttpRequest, JsonResponse
from .models import CustomUser, Patient, Doctor, Relative, Device, Readings, DoctorAddress
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request,'accounts/base.html')

def signin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:home'))
    else:
        return render(request, 'accounts/Signin.html')

def register(request):
    return render(request, 'accounts/Registration.html')

def patientregister(request):
    if request.method=='POST':
        form = Register_patient_doctor(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(username=email, password=password)
            a = CustomUser.objects.get(email=email)
            user.is_patient = True
            user.save()
            login(request,user)
            return HttpResponseRedirect(reverse('accounts:detailInfo'))

    else:
        form = Register_patient_doctor()

    return render(request, 'accounts/EmailInfo.html', {'form':form})

def doctorregister(request):
    if request.method=='POST':
        form = Register_patient_doctor(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(username=email, password=password)
            a = CustomUser.objects.get(email=email)
            user.is_doctor = True
            user.save()
            login(request,user)
            return HttpResponseRedirect(reverse('accounts:detailInfo'))

    else:
        form = Register_patient_doctor()

    return render(request, 'accounts/EmailInfo.html', {'form':form})

@login_required()
def detail_info(request):
    #user = CustomUser.objects.get(email=mail)
    user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
    if user.is_patient==True:
        patient = Patient(patient_id=user)
        if request.method=='POST':
            form = Patient_details(request.POST, request.FILES)
            if form.is_valid():
                patient.first_name = form.cleaned_data['first_name']
                patient.last_name = form.cleaned_data['last_name']
                patient.mobileno= form.cleaned_data['mobileno']
                patient.date_of_birth = form.cleaned_data['date_of_birth']
                patient.gender = form.cleaned_data['gender']
                patient.city = form.cleaned_data['city']
                patient.image = form.cleaned_data['Profile_pic']
                patient.join_date = datetime.today().date()

                patient.save()
                return HttpResponseRedirect(reverse('accounts:home'))

        else:
            form = Patient_details()
        return render(request, 'accounts/DetailInfo.html', {'form':form})

    elif user.is_doctor==True:
        doctor = Doctor(doctor_id=user)
        if request.method=='POST':
            form = Doctor_details(request.POST, request.FILES)

            if form.is_valid():
                doctor.first_name = form.cleaned_data['first_name']
                doctor.last_name = form.cleaned_data['last_name']
                doctor.mobileno= form.cleaned_data['mobileno']
                doctor.date_of_birth = form.cleaned_data['date_of_birth']
                doctor.gender = form.cleaned_data['gender']
                doctor.speciality = form.cleaned_data['speciality']
                doctor.years_of_experience = form.cleaned_data['years_of_experience']
                doctor.city = form.cleaned_data['city']
                doctor.image = form.cleaned_data['Profile_pic']
                doctor.join_date = datetime.today().date()
                doctor.degree = form.cleaned_data['degrees']
                doctor.medical_registration_no = form.cleaned_data['medical_registration_no']

                doctor.save()
                return render(request, 'accounts/DetailInfo.html', {'DocDetailsSuccessfullySaved': "success"})

        else:
            form = Doctor_details()
        return render(request, 'accounts/DetailInfo.html', {'form': form})

def addressInfo(request):
    user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
    if user.is_doctor==True:
        doctor = Doctor.objects.get(doctor_id=user)
        docAddress = DoctorAddress(doctor=doctor)
        api_key = settings.GOOGLE_MAPS_API_KEY
        if request.method=='POST':
            docAddress.clinic_name = request.POST['clinic_name']
            docAddress.clinic_address = request.POST['clinic_address']
            docAddress.lat = request.POST['lat']
            docAddress.lng = request.POST['lng']
            docAddress.save()

            return HttpResponseRedirect(reverse('accounts:home'))

        else:
            return render(request, 'accounts/addressInfo.html', {'Doctor':doctor, 'api_key':api_key})


def login_user(request):
    email = request.POST['MailID']
    password = request.POST['password']
    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request,user)
        sessionbase = SessionBase()
        sessionbase.set_expiry(0)
        return HttpResponseRedirect(reverse('accounts:home'))

    else:
        return render(request, 'accounts/Signin.html', {'error_msg': "Email ID or Password incorrect."})



@login_required()
def profile(request):
    #user = CustomUser.objects.get(email=mail)
    user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
    if user.is_patient==True:
        patient = Patient.objects.get(patient_id_id=user)
        dob = patient.date_of_birth
        age = calculate_age(dob)
        gender = patient.gender
        if gender=='M':
            return render(request,'accounts/profile.html', {'Patient':patient, 'user':user, 'gender':gender, 'age':age})
        else:
            return render(request, 'accounts/profile.html', {'Patient':patient, 'user':user, 'age':age})

    elif user.is_doctor==True:
        doctor = Doctor.objects.get(doctor_id_id=user)
        dob = doctor.date_of_birth
        age = calculate_age(dob)
        gender = doctor.gender
        if gender=='M':
            return render(request, 'accounts/profile.html', {'Doctor': doctor, 'user': user, 'gender':gender, 'age':age})
        else:
            return render(request, 'accounts/profile.html', {'Doctor': doctor, 'user': user, 'age':age})

@login_required()
def home(request):
    #user = CustomUser.objects.get(email=mail)
    user = CustomUser.objects.get(pk=request.session['_auth_user_id'])

    if user.is_patient==True:
        patient = Patient.objects.get(patient_id_id=user)
        if patient.id==1:
             readings = Readings(patient_id=patient)
             readings.heart_beat=58
             readings.SpO2 = 58
             readings.body_temperature=40
             readings.blood_pressure_Diastolic= 90
             readings.blood_pressure_Systolic=120
             readings.date_time = datetime.now()
             readings.save()

        gender = patient.gender
        if gender=='M':
            if patient.doc_assigned==False and patient.has_device==False:
                return render(request, 'accounts/home.html', {'Patient': patient, 'gender':gender})
            elif patient.doc_assigned==True and patient.has_device==False:
                doc=Doctor.objects.get(pk=patient.doctor_id)
                return render(request, 'accounts/home.html', {'Patient': patient, 'gender': gender, 'DocAssigned':doc,'fname':doc.first_name,
                                                              'lastname':doc.last_name})
            elif patient.doc_assigned==False and patient.has_device==True:
                return render(request, 'accounts/home.html', {'Patient': patient, 'gender':gender,'Device':'device'})
            else:
                doc = Doctor.objects.get(pk=patient.doctor_id)
                device = Device.objects.get(patient_id=patient)
                readings = Readings.objects.filter(patient_id_id=1)
                Current_Readings = []
                for rd in readings:
                    if rd.date_time > patient.last_access:
                        Current_Readings.extend([rd])

                return render(request, 'accounts/home.html',
                              {'Patient': patient, 'gender': gender, 'DocAssigned':doc ,'Device': device, 'fname':doc.first_name, 'lastname':doc.last_name, 'Current_Readings':Current_Readings})


        else:
            if patient.doc_assigned==False and patient.has_device==False:
                return render(request, 'accounts/home.html', {'Patient': patient.first_name})
            elif patient.doc_assigned==True and patient.has_device==False:
                doc=Doctor.objects.get(pk=patient.doctor_id)
                return render(request, 'accounts/home.html', {'Patient': patient.first_name, 'DocAssigned':doc,'fname':doc.first_name,
                                                              'lastname':doc.last_name})
            elif patient.doc_assigned==False and patient.has_device==True:
                return render(request, 'accounts/home.html', {'Patient': patient.first_name, 'Device':'device'})
            else:
                doc = Doctor.objects.get(pk=patient.doctor_id)
                device = Device.objects.get(patient_id=patient)
                readings = Readings.objects.filter(patient_id_id=1)
                Current_Readings = []
                for rd in readings:
                    if rd.date_time > patient.last_access:
                        Current_Readings.extend([rd])

                return render(request, 'accounts/home.html',
                              {'Patient': patient, 'DocAssigned':doc ,'Device': device, 'fname':doc.first_name, 'lastname':doc.last_name, 'Current_Readings':Current_Readings})



    elif user.is_doctor==True:
        doctor = Doctor.objects.get(doctor_id_id=user)
        gender = doctor.gender
        p_count = doctor.patient_count
        if gender=='M':
            if p_count!=0:
                count = Patient.objects.filter(doctor_id=doctor)

                return render(request, 'accounts/home.html', {'Doctor': doctor, 'gender':gender, 'P_Count':p_count,'Count':count})
            else:
                return render(request, 'accounts/home.html', {'Doctor': doctor, 'gender': gender})
        else:
            if p_count!=0:
                count = Patient.objects.filter(doctor_id=doctor)
                return render(request, 'accounts/home.html', {'Doctor': doctor, 'P_Count':p_count, 'Count':count})
            else:
                return render(request, 'accounts/home.html', {'Doctor': doctor})



@login_required()
def relativeinfo(request):

    if request.method=='POST':
        user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
        patient = Patient.objects.get(patient_id_id=user)
        gender = patient.gender
        relative = Relative(patient_id=patient)
        form = Relative_details(request.POST)
        if form.is_valid():
            relative.first_name = form.cleaned_data['first_name']
            relative.last_name = form.cleaned_data['last_name']
            relative.gender = form.cleaned_data['gender']
            relative.mobileno = form.cleaned_data['mobileno']
            relative.relation_to_user = form.cleaned_data['relation_to_user']
            relative.date_of_birth = form.cleaned_data['date_of_birth']
            relative.save()

            if gender=='M':
                return render(request, 'accounts/relativeinfo.html',
                           {'Patient':patient,'confirmation': "Relative information recorded succesfully", 'gender':gender})
            else:
                return render(request, 'accounts/relativeinfo.html',
                              {'Patient':patient,'confirmation': "Relative information recorded succesfully"})

    else:
        try:
            user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
            patient = Patient.objects.get(patient_id_id=user)
            gender = patient.gender
            relative = Relative.objects.get(patient_id_id=patient)
            dob = relative.date_of_birth
            age = calculate_age(dob)
            if gender=='M':
                return render(request, 'accounts/relativeinfo.html',
                          {'Patient':patient, 'relative': relative, 'gender':gender, 'age':age})
            else:
                return render(request, 'accounts/relativeinfo.html',
                              {'Patient':patient, 'relative': relative, 'age':age})


        except Relative.DoesNotExist:
            form = Relative_details()
            if gender=='M':
                return render(request, 'accounts/relativeinfo.html', {'Patient':patient,'form': form, 'None':"None", 'gender':gender})
            else:
                return render(request, 'accounts/relativeinfo.html', {'Patient':patient,'form': form, 'None':"None"})



@login_required()
def searchDoc(request):
    user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
    patient=Patient.objects.get(patient_id_id=user)
    gender = patient.gender
    if request.method=='POST':
        searchCriteria=request.POST['searchCriteria']

        doctor_list = Doctor.objects.filter(Q(speciality=searchCriteria) | Q(first_name=searchCriteria) | Q(city=searchCriteria))
        if gender=='M':
            if doctor_list:
                return render(request, 'accounts/DocSearch.html', {'Patient':patient, 'doctor_list':doctor_list, 'speciality':searchCriteria, 'gender':gender})
            else:
                return render(request, 'accounts/DocSearch.html', {'Patient':patient, 'gender':gender,'error_msg':"OOPS!!! nothing matched, please refine your search criteria."})
        else:
            if doctor_list:
                return render(request, 'accounts/DocSearch.html', {'Patient':patient, 'doctor_list':doctor_list, 'speciality':searchCriteria})
            else:
                return render(request, 'accounts/DocSearch.html', {'Patient':patient, 'error_msg':"OOPS!!! nothing matched, please refine your search criteria."})


    else:
        if gender=='M':
            return render(request,'accounts/DocSearch.html', {'Patient':patient, 'gender':gender})
        else:
            return render(request, 'accounts/DocSearch.html', {'Patient':patient})


@login_required()
def doctordetail(request,id):
    user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
    patient = Patient.objects.get(patient_id_id=user)
    hasDoc = patient.doc_assigned
    gender = patient.gender
    doctor = Doctor.objects.get(pk=id)
    dob = doctor.date_of_birth
    age = calculate_age(dob)
    dAddress = DoctorAddress.objects.get(doctor_id=doctor)

    if request.method == 'POST':
        if 'bookdoc'in request.POST:
            patient.doctor = doctor
            patient.doc_assigned = True
            patient.save()
            doctor.patient_count += 1;
            doctor.save()

            if gender == 'M':
                return render(request, 'accounts/doctordetail.html', {'Patient':patient, 'gender':gender, 'doc': doctor, 'dAddress':dAddress,
                                                                      'DocSelected': "DocSelected", 'age':age})
            else:
                return render(request, 'accounts/doctordetail.html', {'Patient': patient, 'doc': doctor, 'dAddress':dAddress, 'DocSelected': "DocSelected", 'age':age})
        else:
            if gender == 'M':
                return render(request, 'accounts/doctordetail.html', {'Patient':patient, 'gender':gender, 'doc': doctor, 'dAddress':dAddress, 'NoDocSelected':"NoDocSelected", 'age':age})
            else:
                return render(request, 'accounts/doctordetail.html', {'Patient': patient, 'doc': doctor, 'dAddress':dAddress, 'NoDocSelected': "NoDocSelected", 'age':age})

    else:
        if gender=='M':
            if hasDoc == True:
                return render(request, 'accounts/doctordetail.html', {'Patient':patient, 'gender':gender, 'doc': doctor, 'dAddress':dAddress, 'hasDoc':hasDoc, 'age':age})
            else:
                return render(request, 'accounts/doctordetail.html', {'Patient': patient, 'gender': gender, 'doc': doctor, 'dAddress':dAddress, 'age':age})
        else:
            if hasDoc == True:
                return render(request, 'accounts/doctordetail.html', {'Patient':patient, 'doc': doctor, 'dAddress':dAddress, 'hasDoc':hasDoc, 'age':age})
            else:
                return render(request, 'accounts/doctordetail.html', {'Patient': patient, 'doc': doctor, 'dAddress':dAddress, 'age':age})

@login_required()
def docLocator(request, id):
    user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
    patient = Patient.objects.get(patient_id_id=user)
    gender = patient.gender
    doctor = Doctor.objects.get(pk=id)
    dAddress = DoctorAddress.objects.get(doctor_id=doctor)
    api_key = settings.GOOGLE_MAPS_API_KEY

    if gender == 'M':
        return render(request, 'accounts/doctorLocator.html', {'Patient':patient, 'gender':gender, 'dAddress':dAddress, 'api_key':api_key})
    else:
        return render(request, 'accounts/doctorLocator.html', {'Patient': patient, 'dAddress': dAddress, 'api_key':api_key})

@login_required()
def assigned_doctor(request):
    user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
    patient = Patient.objects.get(patient_id_id=user)
    gender=patient.gender
    if gender=='M':
        if patient.doc_assigned==True:
            id = patient.doctor_id
            doctor = Doctor.objects.get(id=id)
            dob = doctor.date_of_birth
            age = calculate_age(dob)
            dAddress = DoctorAddress.objects.get(doctor_id=doctor)
            return render(request,'accounts/assignedDoctor.html', {'Patient':patient, 'gender':gender,'doc': doctor, 'dAddress':dAddress, 'age':age})
        else:
            return render(request, 'accounts/assignedDoctor.html', {'Patient':patient, 'gender': gender})
    else:
        if patient.doc_assigned==True:
            id = patient.doctor
            doctor = Doctor.objects.get(id=id)
            dob = doctor.date_of_birth
            age = calculate_age(dob)
            dAddress = DoctorAddress.objects.get(doctor_id=doctor)
            return render(request,'accounts/assignedDoctor.html', {'Patient':patient,'doc': doctor, 'dAddress':dAddress, 'age':age})
        else:
            return render(request, 'accounts/assignedDoctor.html', {'Patient':patient})


@login_required()
def myPatients(request):
    user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
    doctor = Doctor.objects.get(doctor_id_id=user)
    gender = doctor.gender
    p_count = doctor.patient_count
    if gender=='M':
        if p_count==0:
            return render(request,'accounts/myPatients.html', {'Doctor':doctor, 'gender':gender})
        else:
            count_of_patients = Patient.objects.filter(doctor_id=doctor)
            return render(request, 'accounts/myPatients.html', {'Doctor': doctor, 'gender': gender, 'P_Count':p_count, 'Count':count_of_patients})
    else:
        if p_count==0:
            return render(request,'accounts/myPatients.html', {'Doctor':doctor})
        else:
            count_of_patients = Patient.objects.filter(doctor_id=doctor)
            return render(request, 'accounts/myPatients.html', {'Doctor': doctor, 'P_Count':p_count, 'Count':count_of_patients})


def patientDetail(request, id):
    user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
    doctor = Doctor.objects.get(doctor_id_id=user)
    patient = Patient.objects.get(pk=id)
    api_key = settings.GOOGLE_MAPS_API_KEY

    return render(request, 'accounts/patientDetail.html', {'Doctor':doctor, 'api_key':api_key})

@login_required()
def view_device(request):
    user=CustomUser.objects.get(pk=request     .session['_auth_user_id'])
    patient=Patient.objects.get(patient_id_id=user)
    if patient.gender=='M':
        if patient.has_device==True:
            device = Device.objects.get(patient_id=patient)
            return render(request, 'accounts/patientDevice.html',{'Patient':patient,'Device':device, 'deviceid':device.deviceid, 'date':device.year_of_manufacture,
                                                              'product_id':device.product_id, 'gender':'M'})
        else:
            return render(request, 'accounts/patientDevice.html', {'Patient':patient,'gender':'M'})
    else:
        if patient.has_device==True:
            device = Device.objects.get(patient_id=patient)
            return render(request, 'accounts/patientDevice.html',{'Patient':patient, 'Device':device, 'deviceid':device.deviceid, 'date':device.year_of_manufacture,
                                                              'product_id':device.product_id})
        else:
            return render(request, 'accounts/patientDevice.html',{'Patient':patient})



def view_products(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
        if request.method=='POST':
            patient = Patient.objects.get(patient_id_id=user)
            device = Device.objects.filter(patient_id=None).first()
            device.patient=patient
            device.save()
            patient.has_device=True
            patient.save()

            return render(request, 'accounts/ProductFamily.html', {'Hi':"Hi Mofo",'Success': "You have succesfully bought this device"
                                                                                                  ",with this you can measure your health parameters and get medication from your dedicated doctor."})

        return render(request, 'accounts/ProductFamily.html',{'Hi':"Hi Mofo"})
    elif request.user.is_anonymous:
        return render(request, 'accounts/ProductFamily.html', {'Hello': "You Login"})




@login_required()
def get_Readings_data_as_json_fromDB(request):
    user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
    patient = Patient.objects.get(patient_id_id=user)
    readings = Readings.objects.filter(patient_id_id=patient).values('date_time','heart_beat','SpO2', 'body_temperature')[:10:-1]
    rd = list(readings)
    return JsonResponse(rd, safe=False)



@login_required()
def logout_user(request):
    user = CustomUser.objects.get(pk=request.session['_auth_user_id'])
    if user.is_patient==True:
        patient = Patient.objects.get(patient_id_id=user)
        patient.last_access=datetime.now()
        patient.save()
    elif user.is_doctor==True:
        doctor = Doctor.objects.get(doctor_id_id=user)
        doctor.last_access=datetime.now()
        doctor.save()

    logout(request)
    return render(request, 'accounts/base.html', {'logout_msg': "You have been succesfully logged out."})


def calculate_age(t):
    currentDate = datetime.today().date()
    age = int(currentDate.year - t.year)
    month_delta = int(currentDate.month - t.month)
    date_delta = int(currentDate.day - t.day)

    if month_delta < 0:
        age = age - 1
        return age
    elif date_delta < 0 and month_delta == 0:
        age = age - 1
        return age
    else:
        return age



