from django.urls import path
from .views import (
    HomeView,
    ArticleDetailView,
    AddPostView,
    UpdatePostView,
    DeletePostView,
    AddCategoryView,
    CategoryView,
    CategoryListView,
    LikeDislikeView,
    AddCommentView,
    AboutUsView,
    ContactUsView,
    PrivacyPolicyView,
    OurTeamView
)

urlpatterns = [
    # path('', views.home, name='home'),
    path('', HomeView.as_view(), name='home'),
    path('article/<int:pk>', ArticleDetailView.as_view(),
         name='article-detail'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name='update_post'),
    path('article/<int:pk>/remove', DeletePostView.as_view(),
         name='delete_post'),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('category-list/', CategoryListView, name='category-list'),
    path('post-feedback/<int:pk>', LikeDislikeView, name='post-feedback'),
    path('article/<int:pk>/comment/', AddCommentView.as_view(),
         name='add_comment'),
    path('about_us/', AboutUsView.as_view(), name='about_us'),
    path('contact_us/', ContactUsView.as_view(), name='contact_us'),
    path('privacy_policy', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('about_us/our_team', OurTeamView.as_view(), name='our_team'),
]
