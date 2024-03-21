from django.urls import path
from .views import (CreateUserView , VerifyAPIView , GetNewVerification , ChangeUserInformationView , ChangeuserPhotoView,LoginView ,\
                    LoginRefreshView , LogoutView , ForgetPasswordView , ResetPasswordView)

urlpatterns = [
    path('login/' , LoginView.as_view() , name="login"),
    path('login/refresh/' , LoginRefreshView.as_view() , name='login_refresh'),
    path('logout/' , LogoutView.as_view() , name='logout'),
    path('signup/' , CreateUserView.as_view() , name='signup'),
    path('verify/' , VerifyAPIView.as_view() , name='verify'),
    path('verify/again/' , GetNewVerification.as_view() , name='verify_again'),
    path('change/user/', ChangeUserInformationView.as_view() , name='change_user'),
    path('change/user/photo/' , ChangeuserPhotoView.as_view() , name='change_photo'),
    path('forget/password/' , ForgetPasswordView.as_view() , name='forget_password'),
    path('reset/password/' , ResetPasswordView.as_view() , name='reset_password'),
]