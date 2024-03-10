from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from . views import my_html_page 
from trains.views import ticket_booking
urlpatterns = [
    path('admin/', admin.site.urls),
    path('passengers/', include('passengers.urls')),
    path('', ticket_booking,name='home'), 
    path('trains/',include('trains.urls')), 
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)