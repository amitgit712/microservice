from django.urls import path

from .views import ProductViewSet, UserApiView

urlpatterns = [
    path('products/', ProductViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('products/<id>/', ProductViewSet.as_view({
        'get': 'retreive',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('user/', UserApiView.as_view(), name='user'),
]
