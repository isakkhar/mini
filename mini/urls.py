from django.urls import path
from . import views
from mini.views import home, about, post_detail, posts_by_author, posts_by_category, posts_by_tag, contact, portfolio, portfolio_detail, category, search, upload_image, search_posts, subscribe

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('author/<int:author_id>/', posts_by_author, name='posts_by_author'),
    path('category/<slug:category_slug>/', posts_by_category, name='posts_by_category'),
    path('tag/<slug:tag_slug>/', posts_by_tag, name='posts_by_tag'),
    path('contact/', contact, name='contact'),
    path('portfolio/', portfolio, name='portfolio'),
    path('portfolio/<slug:slug>/', portfolio_detail, name='portfolio_detail'),
    path('category/', category, name='category'),
    path('blog/', views.BlogListView.as_view(), name='blog-list'),
    path('search/', search, name='search'),
    path('upload-image/', upload_image, name='upload_image'),
    path('search-posts/', search_posts, name='search_posts'),
    path('subscribe/', subscribe, name='subscribe'),

]