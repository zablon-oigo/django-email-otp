from django.urls import path
from .views import verify_email,login_user,register_user,logout_user,index,resend_otp

urlpatterns=[
    path("",index,name="home"),
    path("login/", login_user, name="login"),
    path("register/", register_user, name="register"),
    path("logout/", logout_user, name="logout"),
    path("verify-email/<username>",verify_email, name="verify-email"),
    path("resend-otp",resend_otp, name="resend-otp"),
]