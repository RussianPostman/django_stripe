from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('simple_strape.urls', 'simple_strape'),
         namespace='simple_strape')),
]
