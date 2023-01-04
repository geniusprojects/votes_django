from rest_framework import serializers

from .models import CategoryGroup, Category, Poll, Choice, Vote, Account

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


class PollSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    images = GallerySerializer(many=True, source='get_images')
    main_image = GallerySerializer(source='get_main_images')
    #votes = VoteSerializer(many=True, source='get_count_votes')
    votes_count = serializers.IntegerField(source='get_count_votes')#(many=True, source='get_count_votes')

    class Meta:
        model = Poll
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
            'images',
            'main_image',
            'votes_count',
        )


class ChoiceSerializer(serializers.ModelSerializer):
    poll = PollSerializer(read_only=True)

    class Meta:
        model = Choice
        fields = (
            'id',
            'uid',
            'poll',
            'choice_text',
            'votes',
            'color',
        )


class VoteSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    choice = ChoiceSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = (
            'id',
            'uid',
            'account',
            'comment',
            'updated',
            'choice',
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'description',
        )


class CategoryPollsSerializer(serializers.ModelSerializer):
    polls = PollSerializer(many=True, read_only=True, source="less_polls")

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'description',
            'polls',
        )


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryGroup
        fields = (
            'id',
            'title',
            'description',
        )


class GroupPollsSerializer(serializers.ModelSerializer):
    categories = CategoryPollsSerializer(many=True, read_only=True)

    class Meta:
        model = CategoryGroup
        fields = (
            'id',
            'title',
            'description',
            'categories',
        )


class LatestPollSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    images = GallerySerializer(many=True, source='get_images')
    main_image = GallerySerializer(source='get_main_images')
    votes_count = serializers.IntegerField(source='get_count_votes')
    category = CategorySerializer()

    class Meta:
        model = Poll
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
            'images',
            'main_image',
            'votes_count',
        )


class PopularPollSerializer(serializers.ModelSerializer):
    main_image = GallerySerializer(source='get_main_images')
    votes_count = serializers.IntegerField(source='get_count_votes')
    category = CategorySerializer()

    class Meta:
        model = Poll
        fields = (
            'id',
            'uid',
            'title',
            'description',
            'created',
            'category',
            'points',
            'main_image',
            'votes_count',
        )