from rest_framework import serializers
from .models import Board, Comment
from django.contrib.auth import get_user_model

User = get_user_model()
# serializer에서 다른 모델을 참조하는 방법
# # 자유 게시판 serializer
# class ArticleListSerializer(serializers.ModelSerializer):
#     username = serializers.StringRelatedField(source="user.username", read_only=True)
#     class Meta:
#         model = Article
#         fields = ('id', 'title', 'content', 'username')

# 자유게시판 댓글
class ArticleCommentListSerializer(serializers.ModelSerializer):
    class Userserializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username', 'id',)
    user = Userserializer()
    class Meta:
        model = Comment
        fields = '__all__'

class ArticleCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'board')

# 게시글 serializer
class ArticleListSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username', 'id',)
    user = UserSerializer()
    class Meta:
        model = Board
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username', 'id',)
            
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Board
        fields = '__all__'