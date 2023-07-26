from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import viewsets, filters, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from votes_django import settings
from rest_framework.exceptions import NotFound as NotFoundError

from team.models import Team

from .models import Product, CategoryGroup, Category
from .serializers import *


class CustomPaginator(PageNumberPagination):
    page_size = 20 # Number of objects to return in one page

    def generate_response(self, query_set, serializer_obj, request):
        try:
            page_data = self.paginate_queryset(query_set, request)
        except NotFoundError:
            return Response({"error": "No results found for the requested page"}, status=status.HTTP_400_BAD_REQUEST)

        serialized_page = serializer_obj(page_data, many=True, context={'request': request})
        return self.get_paginated_response(serialized_page.data)


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = CategoryGroup.objects.all()

    def get_queryset(self):
        return self.queryset


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        return self.queryset


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        account = Account.objects.filter(user=self.request.user).first()

        serializer.save(account=account)

    def get_queryset(self):
        return self.queryset


@api_view(['GET'])
def get_groups(request):
    groups = CategoryGroup.objects.all()
    serializer = GroupProductsSerializer(groups, many=True, context={'request': request})

    return Response(serializer.data)


class GetGroupCategories(APIView):
    def get(self, request, group_id):
        c = Category.objects.filter(group_id=group_id).order_by('title').all()
        serializer = CategorySerializer(c, many=True, context={'request': request})
        return Response(serializer.data)


class GetGroupProducts(APIView):
    def get(self, request, group_id):
        p = Product.objects.filter(category__group=group_id).order_by('-updated').all()
        paginator = CustomPaginator()
        response = paginator.generate_response(p, PopularProductSerializer, request)
        return response


class GetGroupProductsPopular(APIView):
    def get(self, request, group_id):
        p = Product.objects.filter(category__group=group_id).order_by('-points')[:5]
        serializer = PopularProductSerializer(p, many=True, context={'request': request})
        return Response(serializer.data)


class GetCategoryProducts(APIView):

    def get(self, request, cat_id):
        p = Product.objects.filter(category_id=cat_id).order_by('-updated').all()
        paginator = CustomPaginator()
        response = paginator.generate_response(p, PopularProductSerializer, request)
        return response


class GetCategoryProductsPopular(APIView):

    def get(self, request, cat_id):
        p = Product.objects.filter(category_id=cat_id).order_by('-points')[:5]
        serializer = PopularProductSerializer(p, many=True, context={'request': request})
        return Response(serializer.data)