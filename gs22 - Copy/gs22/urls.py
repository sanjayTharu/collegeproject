
from django.contrib import admin
from django.urls import path,include
from api import views
from rest_framework.routers import DefaultRouter
from api.views import ChangepasswordView
# from django.views.generic import TemplateView
# from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
# from api.views import ForgetPasswordView

router=DefaultRouter()

router.register('movie',views.MovieVIewSet,basename='movie')
router.register('theatre',views.TheatreViewSet,basename='threatre')
router.register('show',views.ShowViewSet,basename='show')
router.register('seat',views.SeatViewSet,basename='seat')
router.register('ticket',views.TIcketViewSet,basename='ticket')
router.register('payment',views.PaymentViewSet,basename='payment')
router.register('customer',views.CustomerViewSet,basename='customer')
# router.register('change-password',ChangepasswordView,basename='changepass')
# router.register('forgetpassword',views.ForgotPasswordView,basename='forgetpassword')
# router.register('resetpassword',views.ResetPasswordView,basename='resetpassword')
# router.register('forgetpass',views.ForgetPasswordView,basename='forgetpass')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    # path('forgetpass/<str:token>/',ForgetPasswordView.as_view(),name='forgetpass'),
    path('api/change-password/', ChangepasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # # path('', TemplateView.as_view(template_name="home.html"), name='home'),
    # path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('verifytoken', TokenVerifyView.as_view(), name='token_verify'),
    
]
