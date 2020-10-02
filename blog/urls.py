from django.urls import path
from . import views

urlpatterns = [
    path('liked/', views.like_post, name='blog-liked'),
    #posts views
    path('', views.PostListView.as_view(), name='blog-homepage'),
    path('user/<str:username>', views.UserPostListView.as_view(), name='user-posts'),
    path('myblogs/', views.LoggedinUserPostListView.as_view(), name='blog-myblogs'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new', views.PostCreateView.as_view(), name='post-create'),
    path('post/update/<int:pk>', views.PostUpdateView.as_view(), name='post-update'),
    path('post/delete/<int:pk>', views.PostDeleteView.as_view(), name='post-delete')
]
