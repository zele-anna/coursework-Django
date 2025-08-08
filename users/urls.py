from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.services import email_verification
from users.views import RegisterView, UserListView, UserDetailView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="mailings:home"), name="logout"),
    path("email_confirm/<str:token>/", email_verification, name="email_confirm"),
    path("user_list/", UserListView.as_view(), name="user_list"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("user/<int:pk>/block/", UserUpdateView.as_view(), name="user_block"),

]
