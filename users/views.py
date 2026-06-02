from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, UserSerializer
from .models import User


# ----------------------------
# REGISTER
# ----------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # anyone can register


# ----------------------------
# USER PROFILE (logged-in user only)
# ----------------------------
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user  # returns the currently logged-in user


# ----------------------------
# LOGIN — handled by SimpleJWT
# ----------------------------
# TokenObtainPairView → POST /api/users/login/ → returns access + refresh token
# TokenRefreshView   → POST /api/users/token/refresh/ → returns new access token