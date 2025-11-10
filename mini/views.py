from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Count, Q
from django.views.generic import ListView
from .models import Post, Author, Category, Tag, Comment, Portfolio, Service, Testimonial, Partner, Education, Experience, SiteSetting, AboutPage, ContactPage, Subscriber
from .forms import CommentForm, ContactForm  # You'll create this form
# from mini.views import home, about, post_detail, posts_by_author, posts_by_category, posts_by_tag

def home(request):
    editors_picks = Post.objects.filter(is_editors_pick=True)[:4]
    popular_tags = Tag.objects.all()[:12]
    recent_posts_list = Post.objects.order_by('-created_date')
    paginator = Paginator(recent_posts_list, 5)  # Show 5 posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    popular_posts = Post.objects.order_by('-views')[:5]
    last_comments = Comment.objects.order_by('-created')[:3]
    instagram_gallery = [
        'assets/imgs/page/homepage1/gallery1.png',
        'assets/imgs/page/homepage1/gallery2.png',
        'assets/imgs/page/homepage1/gallery3.png',
    ]
    hot_topics = Category.objects.filter(is_hot_topic=True)
    context = {
        'editors_picks': editors_picks,
        'popular_tags': popular_tags,
        'page_obj': page_obj,  # Pass the paginated object
        'popular_posts': popular_posts,
        'last_comments': last_comments,
        'instagram_gallery': instagram_gallery,
        'hot_topics': hot_topics,
    }
    return render(request, 'mini/index.html', context)

def about(request):
    about_page = AboutPage.objects.first()
    educations = Education.objects.all().order_by('-end_year')
    experiences = Experience.objects.all().order_by('-end_year')
    return render(request, 'mini/about.html', {
        'about_page': about_page,
        'educations': educations,
        'experiences': experiences,
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()

    categories = Category.objects.annotate(num_posts=Count('posts'))
    popular_posts = Post.objects.filter(status='published').order_by('-views', '-published_date')[:5]
    tags = Tag.objects.all()
    last_comments = post.comments.filter(active=True).order_by('-created')[:5]  # Get last 5 comments for this post

    return render(request, 'mini/post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'categories': categories,
        'popular_posts': popular_posts,
        'tags': tags,
        'last_comments': last_comments,
    })

def posts_by_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    posts = Post.objects.filter(author=author, status='published')
    return render(request, 'mini/posts_by_author.html', {'author': author, 'posts': posts})

def posts_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts_list = Post.objects.filter(category=category, status='published').order_by('-published_date')
    paginator = Paginator(posts_list, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    categories = Category.objects.all()
    popular_posts = Post.objects.filter(status='published').order_by('-views', '-published_date')[:5]  # or use your own logic for "popular"
    return render(request, 'mini/posts_by_category.html', {
        'category': category,
        'posts': posts,
        'categories': categories,
        'popular_posts': popular_posts,
    })

def posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag, status='published').order_by('-published_date')
    categories = Category.objects.annotate(num_posts=Count('posts'))
    popular_posts = Post.objects.filter(status='published').order_by('-views', '-published_date')[:5]
    tags = Tag.objects.all()
    recent_comments = Comment.objects.filter(active=True).order_by('-created')[:3]
    recent_posts = Post.objects.filter(status='published').order_by('-published_date')[:5]
    return render(request, 'mini/posts_by_tag.html', {
        'tag': tag,
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'recent_posts': recent_posts,
    })

def contact(request):
    contact_page = ContactPage.objects.first()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'mini/contact.html', {
        'form': form,
        'contact_page': contact_page
    })

def portfolio(request):
    projects = Portfolio.objects.all().order_by('-created')
    # Get unique categories from existing portfolios
    portfolio_categories = Portfolio.objects.exclude(category='').values_list('category', flat=True).distinct().order_by('category')
    services = Service.objects.all()
    testimonials = Testimonial.objects.all()
    partners = Partner.objects.all()
    return render(request, 'mini/portfolio.html', {
        'projects': projects,
        'portfolio_categories': portfolio_categories,
        'services': services,
        'testimonials': testimonials,
        'partners': partners,
    })

def portfolio_detail(request, slug):
    project = get_object_or_404(Portfolio, slug=slug)
    tech_stack_list = [tech.strip() for tech in project.tech_stack.split(',') if tech.strip()] if project.tech_stack else []
    return render(request, 'mini/portfolio_detail.html', {
        'project': project,
        'tech_stack_list': tech_stack_list
    })


def category(request):
    categories = Category.objects.all()
    return render(request, 'mini/category.html', {'categories': categories})

class BlogListView(ListView):
    model = Post
    template_name = 'mini/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

def search(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-created_date')
    
    popular_tags = Tag.objects.all()[:10]
    
    return render(request, 'mini/search_results.html', {
        'query': query,
        'results': results,
        'popular_tags': popular_tags,
        'total_results': results.count() if results else 0
    })

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        
        # Generate unique filename
        ext = file.name.split('.')[-1]
        filename = f"post_images/{file.name}"
        
        # Save file
        path = default_storage.save(filename, ContentFile(file.read()))
        file_url = default_storage.url(path)
        
        return JsonResponse(file_url, safe=False)
    
    return JsonResponse({'error': 'No file uploaded'}, status=400)

@csrf_exempt
def search_posts(request):
    """Search posts for inserting related links in editor"""
    query = request.GET.get('q', '')
    posts = []
    
    if query and len(query) >= 2:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).values('id', 'title', 'slug')[:10]
        
        posts = [
            {
                'id': post['id'],
                'title': post['title'],
                'url': f"/post/{post['slug']}/"
            }
            for post in results
        ]
    
    return JsonResponse({'posts': posts})

@csrf_exempt
def subscribe(request):
    """Handle email subscription"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            return JsonResponse({'success': False, 'message': 'Please enter an email address.'})
        
        # Check if already subscribed
        if Subscriber.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'This email is already subscribed!'})
        
        # Create new subscriber
        try:
            Subscriber.objects.create(email=email)
            return JsonResponse({'success': True, 'message': 'Successfully subscribed! Thank you.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})