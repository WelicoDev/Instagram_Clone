from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# swagger settings
schema_view = get_schema_view(
   openapi.Info(
      title="Instagram Clone Project Api",
      default_version='v0.2.0',
      description="Welcome to the API Documentation",
   ),
   public=True,
   permission_classes=[permissions.AllowAny, ]
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/' , include('users.urls')),
    path('post/' , include('post.urls')),
    # swagger links for the api documentation
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]+static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
