from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import ArticleListSerializer, ArticleSerializer, ArticleCommentListSerializer, ArticleCommentSerializer
from .models import Board, Comment

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
# 모든 게시글 정보를 가져오기
def all_articles_or_create(request):
    if request.method == 'GET':
        articles = Board.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    # 게시글 생성
    elif request.method == 'POST':
        print(request.data)
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # 유효성 검사 실패 시
            print('유효성 검사 실패:', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST',])
@permission_classes([IsAuthenticated])
# 카테고리에 맞게 글 리스트를 가져오기
def article_list(request, category_id):
    if request.method == 'GET':
        articles = Board.objects.all().filter(category = category_id)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, article_pk):
    article = Board.objects.get(pk=article_pk)
    # 단일 게시글 조회
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    # 게시글 수정
    elif request.method == 'PUT':
        serializer = ArticleSerializer(instance = article, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    
    # 게시글 삭제
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def Increase_Views(request, article_pk):
    article = Board.objects.get(pk=article_pk)
    # 조회수 증가
    article.views += 1
    article.save()
    return Response(status=status.HTTP_206_PARTIAL_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
# 모든 게시글 정보를 가져오기
def all_comments_or_create(request, article_pk):
    article = Board.objects.get(pk=article_pk)
    if request.method == 'GET':
        comments = article.comment_set.all()
        serializer = ArticleCommentListSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, board=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_likes(request, article_pk):
    article = Board.objects.get(pk=article_pk)
    value = int(request.data['likes'])
    article.likes += value
    article.save()
    return Response(status=status.HTTP_206_PARTIAL_CONTENT)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)