from api import views
from django.urls import path


urlpatterns = [
    path('category/', views.CategoryList.as_view()),
    path('category/<int:pk>/', views.CategoryDetail.as_view()),
    path('product/', views.ProductList.as_view()),
    path('product/<int:pk>/', views.ProductDetail.as_view()),
    path('sale/', views.CreateSale.as_view()),
]





# from django.conf.urls import url, include
# from django.contrib.auth.models import User
# from rest_framework import routers, serializers, viewsets

# # Serializers define the API representation.
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'is_staff']

# # ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# # Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     url(r'^', include(router.urls)),
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]