from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path

import apps.core.urls

urlpatterns = [path("", include(apps.core.urls)), path("admin/", admin.site.urls)]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
