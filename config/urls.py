from django.contrib import admin
from django.urls import path, include

from config.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls'), name='portal'),
    path('accounts/', include('allauth.urls')),
]

if DEBUG:
    urlpatterns += [path("__debug__/", include('debug_toolbar.urls')),
    ]

