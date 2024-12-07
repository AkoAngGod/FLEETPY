#apps/urls.py
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('creditpayment/', views.credit_payment, name='credit_payment'),    
    path('billing/', views.billing, name='billing'),
    path('receipt/<int:receipt_id>/', views.receipt, name='receipt'),
    path('driver-profile/', views.profile_loob, name='driver_profile'),
    path('editprofile/', views.edit_profile, name='edit_profile'),

    path('driverdashboard/', views.driverdashboard, name='driverdashboard'),

    path('', views.login_view),
    path('accounts/', include('django.contrib.auth.urls')),
    path("addaccount/", views.profile_loob, name="addaccount"),
    path('register/', views.profile_creation, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
