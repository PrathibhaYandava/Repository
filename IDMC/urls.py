from django.contrib import admin
from django.urls import path
from Data_Quality import views

urlpatterns = [
    path('', views.login_view, name='login_page'),
    path('admin/', admin.site.urls),
    path('Home/', views.home_view, name='home'),
    path('ReportForm/', views.ReportForm, name='ReportForm'),
    path('onpremise/', views.onpremise),
    path('cloud/', views.cloud),
    path('FetchData1/', views.FetchData1, name='FetchData1'),
    path('login/', views.login_view, name='login_page'),
    path('signup/', views.signup_view, name='signup'),  # Updated URL pattern
]
