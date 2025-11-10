from django.contrib import admin
from django import forms
from .models import Category, Author, Post, Comment, Tag, ContactMessage, SiteSetting, AboutPage, ContactPage, Portfolio, PortfolioCategory, Service, Testimonial, Partner, Education, Experience, Subscriber

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_hot_topic')
    list_editable = ('is_hot_topic',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 20,
        'style': 'width: 100%;'
    }))
    
    class Meta:
        model = Post
        fields = '__all__'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'author', 'category', 'status', 'is_editors_pick', 'created_date', 'published_date', 'draft_date')
    list_filter = ('status', 'category', 'author', 'is_editors_pick', 'created_date', 'published_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_date'
    ordering = ('-created_date',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'post')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created')
    search_fields = ('name', 'email', 'subject')
    date_hierarchy = 'created'

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'address')

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not AboutPage.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False

@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not ContactPage.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False

class PortfolioAdminForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 20,
        'style': 'width: 100%; font-family: monospace;'
    }))
    
    class Meta:
        model = Portfolio
        fields = '__all__'

@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    form = PortfolioAdminForm
    list_display = ('title', 'category', 'tech_stack', 'created')
    search_fields = ('title', 'description', 'tech_stack')
    list_filter = ('category',)
    
    class Media:
        css = {
            'all': ('https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.css',)
        }
        js = ('https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.js',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_year', 'end_year')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_year', 'end_year')

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    date_hierarchy = 'subscribed_at'
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    def activate_subscribers(self, request, queryset):
        queryset.update(is_active=True)
    activate_subscribers.short_description = "Activate selected subscribers"
    
    def deactivate_subscribers(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_subscribers.short_description = "Deactivate selected subscribers"
