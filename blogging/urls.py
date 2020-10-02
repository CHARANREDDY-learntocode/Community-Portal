from django.contrib import admin
from django.urls import path,include
from users import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls'), name='blog'),
    path('user/', include('users.urls'), name='user'),
    path('post/', include('users.urls'), name='user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
