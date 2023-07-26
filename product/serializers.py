from rest_framework import serializers

from .models import CategoryGroup, Category, Account, Product

from team.serializers import UserSerializer
from gallery.serializers import GallerySerializer


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Account
        fields = (
            'uid',
            'user',
            'first_name',
            'last_name',
            'phone',
            'email',
            'avatar',
        )


class ProductSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'uid',
            'account',
            'title',
            'description',
            'created',
            'updated',
            'category',
            'points',
            'parent',
            'price',
            'is_featured',
            'num_available',
            'num_visits',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'description',
        )


class CategoryProductsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True, source="less_products")

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'description',
            'products',
        )


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryGroup
        fields = (
            'id',
            'title',
            'description',
        )


class GroupProductsSerializer(serializers.ModelSerializer):
    categories = CategoryProductsSerializer(many=True, read_only=True)

    class Meta:
        model = CategoryGroup
        fields = (
            'id',
            'title',
            'description',
            'categories',
        )


class PopularProductSerializer(serializers.ModelSerializer):
    main_image = GallerySerializer(source='get_main_images')
    points_count = serializers.IntegerField(source='get_count_points')
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = (
            'id',
            'uid',
            'title',
            'description',
            'created',
            'category',
            'points',
            'main_image',
            'points_count',
        )