from django.urls import path
from . import views

urlpatterns = [
    # 게시글
    path('articles/', views.all_articles_or_create), # 게시판 조회 및 생성
    path('articles/<int:category_pk>/', views.article_list), # 게시판 종류별로 가져오기
    path('articles/detail/<int:article_pk>/', views.article_detail), # 게시판의 상세 페이지
    path('article_increase_views/<int:article_pk>/', views.Increase_Views), # 조회수 증가
    path('articles/<int:article_pk>/comments/', views.all_comments_or_create), # 댓글 생성 및 조회
    path('articles/likes/<int:article_pk>/', views.article_likes),
    path('articles/comments/<int:comment_pk>/', views.comment_detail), # 댓글 삭제
]
