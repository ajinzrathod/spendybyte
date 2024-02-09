from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


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

# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwNzYwMDkyNywiaWF0IjoxNzA3NTE0NTI3LCJqdGkiOiI0OWY2ODdlMmFmNTg0MzRiOTcxZTBhYWI1OTIzOTJhMyIsInVzZXJfaWQiOjN9.jDLDbBfOGezmrqhTslq4cenNFlHwAHUlfEOKDa8Cs1E",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA3NTE0ODI3LCJpYXQiOjE3MDc1MTQ1MjcsImp0aSI6IjFmNjM2OWMwZjc4NTQyZTRhNTdjZGUzMWJhYWQwNzcyIiwidXNlcl9pZCI6M30.CPtwUT6a4tjXvkk0f3BqApm6AfP-4-B1K0HHUBmlFnQ"
# }
