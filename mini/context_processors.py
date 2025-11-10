from .models import SiteSetting, Category, Tag

def site_settings(request):
    settings = SiteSetting.objects.first()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    return {
        'site_settings': settings,
        'categories': categories,
        'tags': tags,
    }