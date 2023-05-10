
from django.contrib import admin
from django.urls import path,include
from api import views
from rest_framework.routers import DefaultRouter
from api.views import CustomerViewSet,ForgotPasswordViewSet,ResetPasswordViewSet
from django.conf import settings
from django.conf.urls.static import static
# from django.views.generic import TemplateView
# from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
# from api.views import ForgetPasswordView

router=DefaultRouter()

router.register(r'movie',views.MovieVIewSet,basename='movie')
router.register(r'theatre',views.TheatreViewSet,basename='threatre')
router.register(r'show',views.ShowViewSet,basename='show')
router.register(r'seat',views.SeatViewSet,basename='seat')
router.register(r'ticket',views.TicketViewSet,basename='ticket')
router.register(r'payment',views.PaymentViewSet,basename='payment')
router.register(r'customers',CustomerViewSet,basename='customer')
# router.register('change-password',ChangepasswordView,basename='changepass')
# router.register('forgetpassword',views.ForgotPasswordView,basename='forgetpassword')
# router.register('resetpassword',views.ResetPasswordView,basename='resetpassword')
# router.register('forgetpass',views.ForgetPasswordView,basename='forgetpass')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router.urls)),
    path('api/login/',CustomerViewSet.as_view({'post':'create'}),name='customer-login'),
    path('api/register/',CustomerViewSet.as_view({'post':'create'}),name='customer-register'),
    path('api/change-password/',CustomerViewSet.as_view({'put':'update'}),name='customer-change-password'),
    path('api/forgot-password/',ForgotPasswordViewSet.as_view(),name='forgot-password'),
    path('api/reset-password/',ResetPasswordViewSet.as_view(),name='reset-password'),
    # path('forgetpass/<str:token>/',ForgetPasswordView.as_view(),name='forgetpass'),
    # path('api/change-password/', ChangepasswordView.as_view(), name='change-password'),
    # path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # # path('', TemplateView.as_view(template_name="home.html"), name='home'),
    # path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('verifytoken', TokenVerifyView.as_view(), name='token_verify'),
    
] 
# + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
