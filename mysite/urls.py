from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from mysite import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),
    url(r'^djrichtextfield/', include('djrichtextfield.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)