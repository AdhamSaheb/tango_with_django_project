from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from rango import views
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^rango/', include('rango.urls')),
# above maps any URLs starting
# with rango/ to be handled by
# the rango application
	url(r'^admin/', admin.site.urls),
]
