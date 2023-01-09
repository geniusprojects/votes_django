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

from .models import Poll, CategoryGroup, Category, Choice, Vote
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


class PollViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()
    #filter_backends = (filters.SearchFilter,)
    #search_fields = ('account', 'title')

    def perform_create(self, serializer):
        account = Account.objects.filter(user=self.request.user).first()

        serializer.save(account=account)

    def get_queryset(self):
        return self.queryset


class GetGroupPolls(APIView):
    def get(self, request, group_id):
        p = Poll.objects.filter(category__group=group_id).order_by('-updated').all()
        #serializer = PopularPollSerializer(p, many=True, context={'request': request})
        paginator = CustomPaginator()
        response = paginator.generate_response(p, PopularPollSerializer, request)
        return response


class GetGroupCategories(APIView):
    def get(self, request, group_id):
        c = Category.objects.filter(group_id=group_id).order_by('title').all()
        serializer = CategorySerializer(c, many=True, context={'request': request})
        return Response(serializer.data)


class GetGroupPollsPopular(APIView):

    def get(self, request, group_id):
        p = Poll.objects.filter(category__group=group_id).order_by('-points')[:5]
        serializer = PopularPollSerializer(p, many=True, context={'request': request})
        return Response(serializer.data)


class GetCategoryPolls(APIView):

    def get(self, request, cat_id):
        p = Poll.objects.filter(category_id=cat_id).order_by('-updated').all()
        #serializer = PopularPollSerializer(p, many=True, context={'request': request})
        paginator = CustomPaginator()
        response = paginator.generate_response(p, PopularPollSerializer, request)
        return response
        #return Response(serializer.data)


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

    def perform_create(self, serializer):
        poll = Poll.objects.filter(uid=self.request.data['uid']).first()

        serializer.save(poll=poll)

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


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikesSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        vote = Vote.objects.filter(uid=self.request.data['uid']).first()
        account = Account.objects.filter(user=self.request.user).first()

        like_obj = self.queryset.filter(vote=vote).first()
        if like_obj:
            like_obj.accounts.add(account)
            like_obj.save()
            #accounts = list(like_obj.accounts.all())
        else:
            accounts = [account]
            serializer.save(vote=vote, accounts=accounts)

    def get_queryset(self):
        return self.queryset


class DisLikeViewSet(viewsets.ModelViewSet):
    serializer_class = DisLikesSerializer
    queryset = DisLike.objects.all()

    def perform_create(self, serializer):
        vote = Vote.objects.filter(uid=self.request.data['uid']).first()
        account = Account.objects.filter(user=self.request.user).first()

        dislike_obj = self.queryset.filter(vote=vote).first()
        if dislike_obj:
            dislike_obj.accounts.add(account)
            dislike_obj.save()
            #accounts = list(like_obj.accounts.all())
        else:
            accounts = [account]
            serializer.save(vote=vote, accounts=accounts)

    def get_queryset(self):
        return self.queryset