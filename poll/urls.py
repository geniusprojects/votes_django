from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('groups', GroupViewSet, basename='groups')
router.register('categories', CategoryViewSet, basename='categories')
router.register('polls', PollViewSet, basename='polls')
router.register('choices', ChoiceViewSet, basename='choices')
router.register('votes', VoteViewSet, basename='votes')

urlpatterns = [
    path('polls/latest/', get_latest_polls, name='get_latest_polls'),
    path('polls/popular/', get_popular_polls, name='get_popular_polls'),

    path('groups/menu/', get_groups, name='get_groups'),
    path('groups/<int:group_id>/polls/', GetGroupPolls.as_view(), name='get_group_polls'),
    path('groups/<int:group_id>/polls/popular/', GetGroupPollsPopular.as_view(), name='get_group__polls_popular'),

    path('categories/<int:cat_id>/polls/', GetCategoryPolls.as_view(), name='get_category_polls'),
    path('categories/<int:cat_id>/polls/popular/', GetCategoryPollsPopular.as_view(), name='get_category__polls_popular'),

    path('polls/<uuid:poll_id>/choices/', GetPollChoices.as_view(), name='get_poll_choices'),
    path('polls/<uuid:poll_id>/votes/', GetPollVotes.as_view(), name='get_poll_votes'),
    path('polls/<uuid:poll_id>/my-vote/', GetPollMyVote.as_view(), name='get_poll_my_vote'),
    path('', include(router.urls)),
]