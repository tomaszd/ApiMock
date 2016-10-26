"""apimockproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin


from django.conf.urls import url, include
from django.contrib.auth.models import User, Group
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
from apimock.models import MockedApi


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('name',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff', 'groups')

# ViewSets define the view behavior.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
# APImock


class MockedAPISerializer(serializers.HyperlinkedModelSerializer):
    # groups = GroupSerializer(many=True)

    class Meta:
        model = MockedApi
        fields = ('url_to_api', 'http_method', 'mocked_return_value',
                  'error_403', 'error_400', 'easily_updatable',
                  'behavior_after_post')


class MockedApiViewSet(viewsets.ModelViewSet):
    queryset = MockedApi.objects.all()
    serializer_class = MockedAPISerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'mocked_apis', MockedApiViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^apimock/', include('apimock.urls'))
]
