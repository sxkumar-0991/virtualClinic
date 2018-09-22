from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('',views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('register/',views.register, name='register'),
    path('register/patient', views.patientregister, name = 'patientregister'),
    path('register/doctor', views.doctorregister, name='doctorregister'),
    path('details/', views.detail_info, name='detailInfo'),
    path('addressInfo', views.addressInfo, name='addressInfo'),
    path('login/', views.login_user, name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('relative-details/', views.relativeinfo, name='relativeinfo'),
    path('search-doctor/', views.searchDoc, name='searchDoc'),
    path('doctor-detail/<int:id>', views.doctordetail, name='doctordetail'),
    path('locate-doctor/<int:id>',views.docLocator, name='docLocator'),
    path('doctor/',views.assigned_doctor, name='doctor'),
    path('device/',views.view_device, name='viewDevice'),
    path('products/', views.view_products, name='Products'),
    path('api/get_Readings_data_as_json_fromDB', views.get_Readings_data_as_json_fromDB, name='get_Readings_data_as_json_fromDB'),
    path('mypatients/', views.myPatients, name='myPatients'),
    path('patient-detail/<int:id>', views.patientDetail, name='patientdetail'),

]