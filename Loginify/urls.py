from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("users/", views.get_all_users, name="get_all_users"),
    path("users/<str:email>/", views.get_user_by_email, name="get_user"),
    path("users/update/<str:email>/", views.update_user, name="update_user"),
    path("users/delete/<str:email>/", views.delete_user, name="delete_user"),
]