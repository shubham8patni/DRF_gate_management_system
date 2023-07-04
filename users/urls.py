from django.urls import path, re_path
from .views import UserCreate, UserProfile, UnverifiedUsers, UserLogin, VerifyResidents, VerifyGuards, Users, UserState, adminProfileView

# drf_yasg code starts here
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Jaseci API",
        default_version='v1',
        description="Welcome to the world of Jaseci",
        terms_of_service="https://www.jaseci.org",
        contact=openapi.Contact(email="jason@jaseci.org"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# ends here


urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),  #<-- Here
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),  #<-- Here
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),  #<-- Here
    path('register/', UserCreate.as_view(), name = "register"),
    path('login/', UserLogin.as_view(), name ='user_login'), #residents,guards
    path('user_profile/<str:phone_number>/', UserProfile.as_view(), name = "user_profile"),
    path('unverified/<str:type>/', UnverifiedUsers.as_view(), name ='unverifiedUsers'), #residents,guards
    path('VerifyResidents/', VerifyResidents.as_view(), name ='VerifyResidents'), #residents,guards
    path('VerifyGuards/', VerifyGuards.as_view(), name ='VerifyGuards'), #residents,guards


    ###################################SORTED###################################
    path('users/', Users.as_view(), name ='users'), #residents,guards
    path('user_state/', UserState.as_view(), name ='userState2'), #residents,guards
    path('user_state/<str:type>', UserState.as_view(), name ='userState'), #residents,guards
    path('admin_view/<str:phone_number>', adminProfileView.as_view(), name ='admin_view'), #residents,guards

    # path('registerfunc/', UserCreatef, name = "registerfunc"),
    
]