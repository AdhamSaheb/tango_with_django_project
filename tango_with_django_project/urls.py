from django.conf.urls import url , include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


from rango import views

urlpatterns = [

	url(r'^rango/', include('rango.urls')),
# above maps any URLs starting
# with rango/ to be handled by
# the rango application

	url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

