from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import EmailVerification
from .serializers import SignupSerializer, LoginSerializer, UserSerializer

User = get_user_model()

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        # return Response({"error" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        error_messages = serializer.errors.get("non_field_errors")
        if error_messages:
            error_message = error_messages[0] 
        else: 
            for key, messages in serializer.errors.items():
                if messages:
                    error_message = messages
                    break
        
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    


class EmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            email_verif = EmailVerification.objects.get(token=token)
            if email_verif.is_verified:
                return Response({"message": "Email already verified."}) 
            email_verif.is_verified = True
            email_verif.save()

            # Activate user now
            user = email_verif.user
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully!"})
        
        except EmailVerification.DoesNotExist:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)  # Generate JWT Token
            return Response({
                "message": "Login successful!",
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        # return Response({"error" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        error_messages = serializer.errors.get("non_field_errors")
        if error_messages:
            error_message = error_messages[0]  # get the first error string
        else:
            # fallback: convert the whole errors dict to string
            for key, messages in serializer.errors.items():
                if messages:
                    error_message = messages
                    break
        
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)




class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            
            return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)