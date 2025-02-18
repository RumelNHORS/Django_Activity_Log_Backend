from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, ActivityLog
from .serializers import ProductSerializer, ActivityLogSerializer, UserSerializer
from django.utils.timezone import now
from django.contrib.auth.models import User
from rest_framework import generics
from django.core.exceptions import PermissionDenied




class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()  # 🔥 Add this line
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only return products created by the authenticated user."""
        return Product.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Assign the authenticated user as the product owner."""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Ensure the user can only update their own products."""
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this product.")
        serializer.save()

    def perform_destroy(self, instance):
        """Ensure the user can only delete their own products."""
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this product.")
        instance.delete()



class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = ActivityLog.objects.all().order_by('-timestamp')
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]

