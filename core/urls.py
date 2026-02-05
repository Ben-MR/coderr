
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('api/profile/', include('profile_app.api.urls')),
    path('api/', include('offers_app.api.urls')),
    path('api/', include('user_auth_app.api.urls')),
]
