from django.urls import path
from . import views
from .views import(BuyerAnalysisAPIView, BuyerAnalysisDetailsAPIView, LoginView, SignupView)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api', BuyerAnalysisAPIView.as_view()),
    path('api/<int:buyer_id>', BuyerAnalysisDetailsAPIView.as_view()),
    path('api/schema/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
]
