
def blog_list(request):
    posts = BlogPost.objects.filter(is_active=True).order_by("-created_at")
    categories = BlogCategory.objects.filter(is_active=True).order_by("order")
    
    # Fake a page object for the hero
    page = PlaceholderMainPage("blog")
    page.title = "Our Blog"
    page.hero_title = "Latest News & Insights"
    page.hero_subtitle = "Stay updated with the latest from the taxi insurance world"
    
    return render(request, "core/blog_list.html", {
        "posts": posts, 
        "categories": categories,
        "item": page
    })

def blog_detail(request, slug):
    post = BlogPost.objects.get(slug=slug, is_active=True)
    recent_posts = BlogPost.objects.filter(is_active=True).exclude(pk=post.pk).order_by("-created_at")[:5]
    categories = BlogCategory.objects.filter(is_active=True).order_by("order")
    
    # Reuse dropdown item logic for hero if image exists, otherwise placeholder
    # We can create a fake item object to pass to base template for hero rendering
    class BlogPostItem:
        def __init__(self, post):
            self.title = post.title
            self.hero_title = post.title
            self.hero_subtitle = post.created_at.strftime("%B %d, %Y")
            self.hero_image = post.image
            self.meta_title = post.meta_title or post.title
            self.meta_description = post.meta_description
            self.meta_keywords = post.meta_keywords
            
        @property
        def get_hero_image_url(self):
            if self.hero_image:
                return self.hero_image.url
            return get_fake_hero_image_url(self.title, "")

    item = BlogPostItem(post)
    
    return render(request, "core/blog_detail.html", {
        "post": post,
        "recent_posts": recent_posts,
        "categories": categories,
        "item": item
    })
