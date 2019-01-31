from django.contrib import admin
from django.urls import path, include

#hey 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bass/', include('bass.urls')),
]