from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from . views import TrainCreateView,TrainUpdateView,TrainListView,TrainDeleteView,Home,leave_review

urlpatterns = [
    path('add_train/',TrainCreateView.as_view(),name='add_train'), 
    path('edit/<int:pk>/', TrainUpdateView.as_view(), name='train_edit'),
    path('admin_dashboard/', TrainListView.as_view(), name='admin_dashboard'), 
    path('train/<int:pk>/delete/', TrainDeleteView.as_view(), name='train_delete'), 
    path('train_details',Home.as_view(), name='train_details'),
    path('station_filtering/<slug:category_slug>/', Home.as_view(), name='station_filtering'), 
    path('train/review/<int:id>/',leave_review,name='leave_review'),
] 
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)