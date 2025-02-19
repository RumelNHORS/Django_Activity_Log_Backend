from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ActivityLogViewSet, RegisterUserView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'activity-logs', ActivityLogViewSet)


urlpatterns = [
    path('', include(router.urls)),

    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('logout/', LogoutView.as_view(), name='logout'),
    
]
