from django.urls import path, include

# from .api import RegisterUserApi, UserApi
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register(r'users', UserApi, basename='user')

urlpatterns = [
    # path("register/", RegisterUserApi.as_view()),
    path("", include(router.urls)),
]
