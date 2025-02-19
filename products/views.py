from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, ActivityLog
from .serializers import ProductSerializer, ActivityLogSerializer, UserSerializer
from django.utils.timezone import now
from django.contrib.auth.models import User
from rest_framework import generics
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import set_current_user



class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        set_current_user(self.request.user) 
        serializer.save(user=self.request.user)
        print('#################################')
        print('Created user:', self.request.user)
        print('#################################')

    def perform_update(self, serializer):
        set_current_user(self.request.user)
        serializer.save() 
        print('*******************************')
        print('Updated user:', self.request.user)
        print('*******************************')

    def perform_destroy(self, instance):
        instance.delete()



class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = ActivityLog.objects.all().order_by('-timestamp')
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


