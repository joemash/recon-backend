from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from src.account.urls import (
    password_router,
    user_router,
)
from src.recon.urls import recon_router
from src.account.views.token import CustomTokenRefreshView

v1_urls = [
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("user/", include(user_router.urls)),
    path("reconciliation/", include(recon_router.urls)),
    path("password/", include(password_router.urls)),
]


urlpatterns = [
    path("api/v1/", include((v1_urls, "v1"), namespace="v1")),
    path("admin/", admin.site.urls),
    # API docs UI:
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
