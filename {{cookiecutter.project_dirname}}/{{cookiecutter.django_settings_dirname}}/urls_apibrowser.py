"""API browser URL configuration."""

from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path(
        "browser/",
        include(
            (
                [
                    path(
                        "schema/",
                        staff_member_required(
                            SpectacularAPIView.as_view(
                                urlconf="{{ cookiecutter.project_slug }}.urls"
                            )
                        ),
                        name="schema",
                    ),
                    path(
                        "docs/",
                        staff_member_required(
                            SpectacularSwaggerView.as_view(
                                url_name="api:browser:schema"
                            )
                        ),
                        name="docs",
                    ),
                ],
                "browser",
            ),
        ),
    )
]
