from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import viewsets, filters, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from team.models import Team

from .models import Poll, CategoryGroup, Category, Choice, Vote
from .serializers import *


class PollPagination(PageNumberPagination):
    page_size = 2


class PollViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()
    pagination_class = PollPagination
    #filter_backends = (filters.SearchFilter,)
    #search_fields = ('account', 'title')

    def get_queryset(self):
        return self.queryset


class GetGroupPolls(APIView):
    pagination_class = PollPagination

    def get(self, request, group_id):
        p = Poll.objects.filter(category__group=group_id).order_by('-updated').all()
        serializer = PopularPollSerializer(p, many=True, context={'request': request})
        return Response(serializer.data)


class GetGroupPollsPopular(APIView):

    def get(self, request, group_id):
        p = Poll.objects.filter(category__group=group_id).order_by('-points')[:5]
        serializer = PopularPollSerializer(p, many=True, context={'request': request})
        return Response(serializer.data)


class GetCategoryPolls(APIView):
    pagination_class = PollPagination

    def get(self, request, cat_id):
        p = Poll.objects.filter(category_id=cat_id).order_by('-updated').all()
        serializer = PopularPollSerializer(p, many=True, context={'request': request})
        return Response(serializer.data)


class GetCategoryPollsPopular(APIView):

    def get(self, request, cat_id):
        p = Poll.objects.filter(category_id=cat_id).order_by('-points')[:5]
        serializer = PopularPollSerializer(p, many=True, context={'request': request})
        return Response(serializer.data)


@api_view(['GET'])
def get_latest_polls(request):
    polls = Poll.objects.all().order_by('-created')[:6]
    serializer = LatestPollSerializer(polls, many=True, context={'request': request})

    return Response(serializer.data)


@api_view(['GET'])
def get_popular_polls(request):
    polls = Poll.objects.all().order_by('points')[:5]
    serializer = PopularPollSerializer(polls, many=True, context={'request': request})

    return Response(serializer.data)


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


@api_view(['GET'])
def get_groups(request):
    groups = CategoryGroup.objects.all()
    serializer = GroupPollsSerializer(groups, many=True, context={'request': request})

    return Response(serializer.data)


class ChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()
    #filter_backends = (filters.SearchFilter,)
    #search_fields = ('account', 'title')

    def get_queryset(self):
        return self.queryset


class GetPollChoices(APIView):

    def get(self, request, poll_id):
        p = Choice.objects.filter(poll_id=poll_id).all()
        serializer = ChoiceSerializer(p, many=True, context={'request': request})
        return Response(serializer.data)


class GetPollVotes(APIView):

    def get(self, request, poll_id):
        choices = Choice.objects.filter(poll_id=poll_id).values('uid')
        votes = Vote.objects.filter(choice__uid__in=choices).order_by('-updated').all()
        serializer = VoteSerializer(votes, many=True, context={'request': request})
        return Response(serializer.data)


class GetPollMyVote(APIView):

    def get(self, request, poll_id):
        choices = Choice.objects.filter(poll_id=poll_id).values('uid')
        if self.request.user.is_authenticated:
            account = Account.objects.filter(user=self.request.user).first()
            vote = Vote.objects.filter(choice__uid__in=choices, account=account).first()
            serializer = VoteSerializer(vote, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({})


class VoteViewSet(viewsets.ModelViewSet):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()

    def perform_create(self, serializer):
        choice = Choice.objects.filter(uid=self.request.data['uid']).first()
        choice.votes += 1
        choice.save()
        account = Account.objects.filter(user=self.request.user).first()

        serializer.save(choice=choice, account=account)

    def get_queryset(self):
        return self.queryset