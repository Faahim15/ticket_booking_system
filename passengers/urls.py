
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . views import UserRegistrationView,UserLoginView ,activate,logout_view,UserDetails,edit_profile,change_password,Deposit_money
urlpatterns = [
    path('registration/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),  
    path('active/<uid64>/<token>/',activate, name = 'activate'), 
    path('logout/', logout_view, name='logout'), 
    path('profile/',UserDetails,name='profile'),
    path('profile/edit/',edit_profile,name='edit_profile'),
    path('change_password/',change_password,name='change_password'),
    path('deposit_money/',Deposit_money,name='deposit_money'),
] 
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)