from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from photos import views

urlpatterns = [
    path( '', views.Home.as_view(), name = 'home' ),
    path( 'upload/', views.upload, name = 'jfu_upload' ),
    path( 'delete/<int:pk>', views.upload_delete, name = 'jfu_delete' ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
