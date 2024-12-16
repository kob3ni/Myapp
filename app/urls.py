from django.contrib import admin
from django.urls import include, path

from app.settings import DEBUG
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace = 'main')),
    path('flight/', include('tickets.urls', namespace = 'flight')),
    path('user/', include('users.urls', namespace = 'user'))
]

if DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
        ]