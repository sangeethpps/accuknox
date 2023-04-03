from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from rest_framework.authtoken import views


# def redirect_to_login():
#     return redirect('core/login/')


urlpatterns = [
    path("", include('core.frontend.urls')),
    path("admin/", admin.site.urls),
    path('core/', include('core.frontend.urls')),
    path('core/api/', include('core.backend.urls')),
    path('api-token-auth/', views.obtain_auth_token)

]
