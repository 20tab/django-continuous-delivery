"""{{ cookiecutter.project_name }} URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

admin.site.site_header = admin.site.site_title = "{{ cookiecutter.project_name }}"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            (
                [
                    *(
                        [path("", include("{{ cookiecutter.project_slug }}.urls_apibrowser"))]
                        if settings.ENABLE_API_DOC
                        else []
                    ),
                ],
                "api",
            )
        ),
    ),
]

if settings.DEBUG:  # pragma: no cover
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]

try:
    import debug_toolbar
except ModuleNotFoundError:  # pragma: no cover
    pass
else:
    urlpatterns.append(
        path("__debug__/", include(debug_toolbar.urls))
    )  # pragma: no cover
