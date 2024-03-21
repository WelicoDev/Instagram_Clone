from django.core.exceptions import ObjectDoesNotExist
from django.utils.datetime_safe import datetime
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework import permissions , status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from shared.utility import send_email, send_phone, check_email_or_phone
from .models import User , UserConfirmation , NEW , CODE_VERIFIED , DONE , PHOTO_DONE , VIA_EMAIL , VIA_PHONE
from .serializers import SignUpSerializer, ChangeUserInformation, ChangeUserPhotoSerializer, LoginSerializer, \
    LoginRefreshSerializer , LogoutSerializer , ForgetPasswordSerializer , ResetPasswordSerializer


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer

class VerifyAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self ,request, *args , **kwargs):
        user = self.request.user
        code = self.request.data.get('code')

        self.check_verify(user, code)

        return Response(
            data={
                "success":True,
                "auth_status":user.auth_status,
                "access":user.token()['access'],
                "refresh":user.token()['refresh_token'],
            }
        )
    @staticmethod
    def check_verify(user , code):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), code=code , is_confirmed=False)
        if not verifies.exists():
            data = {
                "message":"Confirmed code invalid."
            }

            raise ValidationError(data)
        else:
            verifies.update(is_confirmed=True)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()

        return True

class GetNewVerification(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self , request , *args , **kwargs):
        user = self.request.user
        self.check_verification(user)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email , code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            # send_phone(user.phone_number , code)
        else:
            data = {
                "message":"Email or phone number invalid."
            }

            raise ValidationError(data)
        return Response(
            {
                "success":True,
                "message":"Your verification code has been resent",
            }
        )
    @staticmethod
    def check_verification(user):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), is_confirmed=False)
        if verifies.exists():
            data = {
                "message":"Your code is still usable. wait a while"
            }

            raise ValidationError(data)

class ChangeUserInformationView(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChangeUserInformation
    http_method_names = ['patch' , 'put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super(ChangeUserInformationView , self).update(request , *args , **kwargs)
        data = {
            "success":True,
            "message":"User updated successfully",
            "auth_status":self.request.user.auth_status,
        }
        return Response(data , status=status.HTTP_200_OK)
    def partial_update(self, request, *args, **kwargs):
        super(ChangeUserInformationView , self).partial_update(request , *args , **kwargs)
        data = {
            "success":True,
            "message":"User updated successfully",
            "auth_status":self.request.user.auth_status,
        }
        return Response(data , status=status.HTTP_200_OK)

class ChangeuserPhotoView(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self,request,*args,**kwargs):
        serializer = ChangeUserPhotoSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            serializer.update(user , serializer.validated_data)
            return Response(
                {
                    "message":"Photo updated successfully"
                }, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors , status=status.HTTP_400_BAD_REQUEST
        )

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class LoginRefreshView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer

class LogoutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated,]

    def post(self , request , *args , **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                "success":True,
                "message":"You are logout out."
            }
            return Response(data , status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ForgetPasswordView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = ForgetPasswordSerializer

    def post(self , request , *args , **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email_or_phone = serializer.validated_data.get('email_or_phone')
        user = serializer.validated_data.get('user')
        if check_email_or_phone(email_or_phone) == "phone":
            code = user.create_verify_code(VIA_PHONE)
            # send_phone(email_or_phone , code)
        elif check_email_or_phone(email_or_phone) == "email":
            code = user.create_verify_code(VIA_EMAIL)
            send_email(email_or_phone , code)
        return Response(
            {
                "success":True,
                "message":"Verification code sent successfully.",
                "access":user.token()['access'],
                "refresh":user.token()['refresh_token'],
                "user_status":user.auth_status
            } , status=status.HTTP_200_OK
        )

class ResetPasswordView(UpdateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['patch' , 'put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = super(ResetPasswordView ,self).update(request , *args , **kwargs)
        try:
            user = User.objects.get(id=response.data.get('id'))
        except ObjectDoesNotExist as e:
            raise NotFound(detail="User not found.")

        return Response(
            {
                "success":True,
                "message":"You are password updated successfully",
                "access":user.token()['access'],
                "refresh":user.token()['refresh_token']
            }
        )

