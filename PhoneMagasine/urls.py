from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Pastebin API')
from PhoneMagasine import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('customuser.urls')),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),

    path('api/', include('rest_framework.urls')),
    path('swagger/', schema_view),
    path('', include('magasine.urls')),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
