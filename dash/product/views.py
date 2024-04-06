from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .producer import publish

from .serializers import ProductSerializer
from .models import Product, User

import random


class ProductViewSet(viewsets.ViewSet):

    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retreive(self, request, id=None):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found for id"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, id=None):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found for id"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, id=None):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            publish('product_deleted', id)
            return Response(
                {"success": "Product deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

        product.delete()
        publish('product_deleted', id)
        return Response(
            {"success": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


class UserApiView(APIView):
    def get(self, _):
        users = User.objects.all()
        if not users:
            return Response({
                'error': "user not found"
            }, status=status.HTTP_404_NOT_FOUND)
        user = random.choice(users)

        return Response({
            'id': user.id
        }, status=status.HTTP_200_OK)
