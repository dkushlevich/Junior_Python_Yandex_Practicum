from api.views import SignUpView, TokenView, UserViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', TokenView.as_view())
]
