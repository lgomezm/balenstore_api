from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import CreateUserView


urlpatterns = [
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("signup", CreateUserView.as_view(), name="signup"),
]
