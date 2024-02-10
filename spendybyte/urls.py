from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf.urls.static import static
from django.conf import settings

from spendybyte.media_access import media_access


admin.site.site_header = settings.PROJECT_NAME
admin.site.index_title = settings.PROJECT_NAME
admin.site.site_title = settings.PROJECT_NAME

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("api/v1/account/", include("account.urls")),
]


# when in local server, show all images irrespective of authentication
# TODO: we can use NGINX server in local system to check if this actually
# works or not, as X-Accel-Redirect is part of NGINX
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
else:
    urlpatterns += [
        re_path(
            r"^media/(?P<filepath>.*)/$",
            media_access,
            name="serve_protected_image",
        ),
    ]
