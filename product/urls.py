from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('groups', GroupViewSet, basename='groups')
router.register('categories', CategoryViewSet, basename='categories')
router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    path('groups/menu/', get_groups, name='get_groups'),
    path('groups/<int:group_id>/categories/', GetGroupCategories.as_view(), name='get_group_categories'),
    path('groups/<int:group_id>/products/', GetGroupProducts.as_view(), name='get_group_polls'),
    path('groups/<int:group_id>/products/popular/', GetGroupProductsPopular.as_view(), name='get_group__polls_popular'),

    path('categories/<int:cat_id>/products/', GetCategoryProducts.as_view(), name='get_category_polls'),
    path('categories/<int:cat_id>/products/popular/', GetCategoryProductsPopular.as_view(), name='get_category__polls_popular'),

    path('', include(router.urls)),
]