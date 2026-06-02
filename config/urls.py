from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.api.urls')),
    path('api/', include('accounts.api.user_urls')),
    path('api/', include('posts.api.urls')),
]