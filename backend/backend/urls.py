"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from itskilleval.view.eval import EvalView
from itskilleval.view.job import JobView
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = _('IT skill evaluation')
admin.site.index_title = _('Management site')
admin.site.site_title = _('IT skill evaluation')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/v1/eval/<uuid:model_id>/', EvalView.as_view(), name='index'),
    path('api/v1/job/<uuid:job_id>/', JobView.as_view(), name='job_index')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
