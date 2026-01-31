from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import random

def get_fake_hero_image_url(title, slug, pk=None):
    """
    Returns a relevant Unsplash image URL based on the item's title or slug.
    If no match is found, returns a random generic transportation/business image.
    """
    # Keywords mapping to Unsplash Image IDs
    keywords = {
        'taxi': '1556122071-e404ea947d56',      # Taxi cab
        'cab': '1556122071-e404ea947d56',       # Taxi cab
        'limo': '1562916183-42e616c68b72',      # Luxury car/Limo feel
        'limousine': '1562916183-42e616c68b72', # Luxury car/Limo feel
        'luxury': '1562916183-42e616c68b72',    # Luxury car
        'black car': '1562916183-42e616c68b72', # Black car service
        'truck': '1601584115197-04ecc0da31d7',  # Semi truck
        'semi': '1601584115197-04ecc0da31d7',   # Semi truck
        'bus': '1570125909232-eb263c188f7e',    # Bus
        'shuttle': '1570125909232-eb263c188f7e',# Bus/Shuttle
        'non-emergency': '1516733725897-1aa73b87c8e8', # Ambulance/Medical transport feel
        'medical': '1516733725897-1aa73b87c8e8',       # Medical
        'uber': '1449965408869-eaa3f722e40d',   # Car driving / Rideshare
        'lyft': '1449965408869-eaa3f722e40d',   # Car driving
        'rideshare': '1449965408869-eaa3f722e40d',
        'contact': '1534536281715-e28d76689b4d',# Phone/Contact
        'support': '1534536281715-e28d76689b4d',# Phone/Support
        'about': '1522071820081-009f0129c71c',  # Office/Team
        'quote': '1450101499163-c8848c66ca85',  # Signing/Paperwork
        'payment': '1554224155-8d04cb21cd6c',   # Calculator/Money
        'pay': '1554224155-8d04cb21cd6c',
        'file': '1586281380349-632531db7ed4',   # Documents
        'upload': '1586281380349-632531db7ed4', # Documents
    }

    defaults = [
        '1549317661-bd32c8ce0db2', # Driving / Steering wheel
        '1469854523086-cc02fe5d8800', # Open Road
        '1449965408869-eaa3f722e40d', # Driver view
        '1486312338219-ce68d2c6f44d', # Working on laptop
    ]

    text = ""
    if title:
        text += title.lower()
    if slug:
        text += " " + slug.lower()
    
    for key, img_id in keywords.items():
        if key in text:
            return f"https://images.unsplash.com/photo-{img_id}?auto=format&fit=crop&w=1920&q=80"
    
    if pk:
        img_id = defaults[pk % len(defaults)]
    else:
        img_id = random.choice(defaults)
        
    return f"https://images.unsplash.com/photo-{img_id}?auto=format&fit=crop&w=1920&q=80"


class SiteConfig(models.Model):
    site_name = models.CharField(max_length=150, blank=True)
    homepage_title = models.CharField(max_length=200, blank=True)

    phone_number = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    hero_title = models.CharField(max_length=200, blank=True)
    hero_tagline = models.CharField(max_length=255, blank=True)
    hero_description = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to="hero/", blank=True, null=True)

    logo = models.ImageField(upload_to="branding/logo/", blank=True, null=True)
    favicon = models.ImageField(upload_to="branding/favicon/", blank=True, null=True)

    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    serving_states_list = models.TextField(
        blank=True,
        help_text="Comma-separated list of states currently serving (e.g. Alaska, Arizona, California)"
    )
    coming_soon_states_list = models.TextField(
        blank=True,
        help_text="Comma-separated list of states coming soon (e.g. Alabama, Arkansas)"
    )

    home_about_title = models.CharField(
        max_length=200, 
        blank=True, 
        default="About Oswald Taxi and Transportation Services",
        help_text="Title for the About section on the homepage"
    )
    home_about_content = models.TextField(
        blank=True, 
        default="We are a leading provider of taxi and transportation insurance...",
        help_text="Content for the About section on the homepage"
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site_name or "Site Configuration"

    def save(self, *args, **kwargs):
        if not self.pk and SiteConfig.objects.exists():
            return
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def get_serving_states(self):
        if not self.serving_states_list:
            return []
        return [s.strip() for s in self.serving_states_list.split(',') if s.strip()]

    @property
    def get_coming_soon_states(self):
        if not self.coming_soon_states_list:
            return []
        return [s.strip() for s in self.coming_soon_states_list.split(',') if s.strip()]


class MainPage(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    url = models.CharField(max_length=200, blank=True)
    
    # Hero
    hero_title = models.CharField(max_length=200, blank=True)
    hero_subtitle = models.CharField(max_length=255, blank=True)
    hero_image = models.ImageField(upload_to="hero/", blank=True, null=True)

    # Content
    content = models.TextField(blank=True)
    content_width = models.CharField(
        max_length=20, 
        choices=[("container", "Container"), ("full", "Full Width")], 
        default="container"
    )
    layout_columns = models.PositiveIntegerField(default=1, choices=[(1, "1 Column"), (2, "2 Columns")])

    # SEO
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)
    og_image = models.ImageField(upload_to="seo/", blank=True, null=True)

    show_on_home = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.url:
            return self.url
        return reverse("main_page_detail", args=[self.slug])

    @property
    def get_hero_image_url(self):
        if self.hero_image:
            return self.hero_image.url
        return get_fake_hero_image_url(self.title, self.slug, self.pk)


class DropdownItem(models.Model):
    main_page = models.ForeignKey(MainPage, related_name="dropdown_items", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    url = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=255, blank=True, help_text="Short description for menu/cards")

    # Card Media
    image = models.ImageField(upload_to="dropdown/images/", blank=True, null=True)
    icon_svg = models.TextField(blank=True, help_text="SVG code for icon")

    # Hero
    hero_title = models.CharField(max_length=200, blank=True)
    hero_subtitle = models.CharField(max_length=255, blank=True)
    hero_image = models.ImageField(upload_to="hero/", blank=True, null=True)

    # Content
    content = models.TextField(blank=True)
    content_width = models.CharField(
        max_length=20, 
        choices=[("container", "Container"), ("full", "Full Width")], 
        default="container"
    )
    layout_columns = models.PositiveIntegerField(default=1, choices=[(1, "1 Column"), (2, "2 Columns")])

    # SEO
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.main_page.title} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.url:
            return self.url
        if not self.slug:
            return "#"
        return reverse("dropdown_item_detail", args=[self.slug])

    @property
    def get_hero_image_url(self):
        if self.hero_image:
            return self.hero_image.url
        return get_fake_hero_image_url(self.title, self.slug, self.pk)


class PaymentPartner(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="payments/logos/", blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)
    payment_url = models.URLField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Payment Partner"
        verbose_name_plural = "Payment Partners"

    def __str__(self):
        return self.name


class QuoteRequest(models.Model):
    # General Information
    business_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50)
    proposed_start_date = models.DateField(null=True, blank=True)
    contact_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    website = models.URLField(blank=True)
    fein = models.CharField(max_length=50, blank=True, verbose_name="FEIN")
    contact_preference = models.CharField(
        max_length=20,
        choices=[("Email", "via Email"), ("Phone", "via Phone"), ("Online", "Online")],
        blank=True,
        verbose_name="Preferred contact method"
    )

    # Address
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state_address = models.CharField(max_length=100, blank=True, verbose_name="State / Province / Region")
    zip_code = models.CharField(max_length=20, blank=True, verbose_name="ZIP / Postal Code")

    # Business Details
    is_new_business = models.CharField(
        max_length=10, 
        choices=[("Yes", "Yes"), ("No", "No")],
        default="No",
        blank=True
    )
    description_of_operation = models.TextField(blank=True)
    cities_of_operation = models.TextField(blank=True, verbose_name="Cities where vehicles regularly operate")
    operate_state = models.CharField(max_length=100, blank=True, verbose_name="What state do you operate in?")

    # Loss History
    number_of_losses = models.PositiveIntegerField(default=0, blank=True)
    loss_runs_file = models.FileField(upload_to="quotes/loss_runs/", blank=True, null=True)

    # Insurance History
    is_currently_insured = models.CharField(
        max_length=20,
        choices=[("Yes", "Yes"), ("No", "No"), ("Unknown", "Unknown")],
        blank=True,
        verbose_name="Are you currently insured?"
    )
    current_carrier = models.CharField(max_length=200, blank=True)
    radius_of_operation = models.CharField(max_length=100, blank=True)
    years_in_business = models.PositiveIntegerField(null=True, blank=True)

    # Coverage Limits
    general_liability_needed = models.CharField(
        max_length=10,
        choices=[("Yes", "Yes"), ("No", "No")],
        blank=True
    )
    general_liability_limits = models.CharField(max_length=100, blank=True)
    auto_liability_limits = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quote Request from {self.business_name or self.contact_name} ({self.created_at.strftime('%Y-%m-%d')})"


class QuoteRequestDocument(models.Model):
    quote_request = models.ForeignKey(QuoteRequest, related_name="documents", on_delete=models.CASCADE)
    file = models.FileField(upload_to="quotes/misc_docs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doc for {self.quote_request}"


class PolicyChangeRequest(models.Model):
    # General Info
    your_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    operate_state = models.CharField(max_length=100, blank=True, verbose_name="What state do you operate in?")

    # Driver Change
    driver_change_type = models.CharField(max_length=20, blank=True, verbose_name="Driver Change Action")
    driver_name = models.CharField(max_length=100, blank=True)
    driver_dob = models.DateField(null=True, blank=True, verbose_name="Driver DOB")
    driver_license = models.CharField(max_length=100, blank=True)

    # Vehicle Change
    vehicle_change_type = models.CharField(max_length=20, blank=True, verbose_name="Vehicle Change Action")
    vehicle_year = models.CharField(max_length=20, blank=True)
    vehicle_make_model = models.CharField(max_length=100, blank=True)
    vehicle_vin = models.CharField(max_length=100, blank=True, verbose_name="VIN Number")
    vehicle_coverage = models.CharField(max_length=20, blank=True, verbose_name="Comp or Collision coverage?")
    vehicle_value = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Policy Change Request from {self.your_name} ({self.created_at.strftime('%Y-%m-%d')})"

    class Meta:
        ordering = ["-created_at"]


class SalesSupportRequest(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    operate_state = models.CharField(max_length=100, blank=True, verbose_name="What state do you operate in?")
    message = models.TextField(verbose_name="How can we help?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sales Support Request from {self.first_name} {self.last_name} ({self.created_at.strftime('%Y-%m-%d')})"

    class Meta:
        ordering = ["-created_at"]


class FileUploadRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    file = models.FileField(upload_to="uploads/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File Upload from {self.name} ({self.created_at.strftime('%Y-%m-%d')})"

    class Meta:
        ordering = ["-created_at"]


class SupportRequest(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Support Request from {self.first_name} {self.last_name} ({self.created_at.strftime('%Y-%m-%d')})"

    class Meta:
        ordering = ["-created_at"]


class FAQCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    dropdown_item = models.OneToOneField(
        DropdownItem,
        related_name="faq_category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    insurance_product = models.ForeignKey(
        "InsuranceProduct",
        related_name="faq_categories",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    coverages = models.ManyToManyField("InsuranceCoverageType", related_name="faq_categories", blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["order"]
        unique_together = ("insurance_product", "slug")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class FAQItem(models.Model):
    category = models.ForeignKey(FAQCategory, related_name="items", on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    show_on_home = models.BooleanField(default=False, help_text="Show this FAQ item on the home page")

    class Meta:
        verbose_name = "FAQ Item"
        verbose_name_plural = "FAQ Items"
        ordering = ["order"]

    def __str__(self):
        return self.question


class InsuranceCoverageType(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Insurance Coverage Type"
        verbose_name_plural = "Insurance Coverage Types"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class InsuranceProduct(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)
    dropdown_item = models.OneToOneField(
        DropdownItem,
        related_name="insurance_product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Link this product to a site page."
    )
    coverages = models.ManyToManyField(InsuranceCoverageType, related_name="products", blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Insurance Product"
        verbose_name_plural = "Insurance Products"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def get_hero_image_url(self):
        if self.dropdown_item and self.dropdown_item.hero_image:
            return self.dropdown_item.hero_image.url
        return get_fake_hero_image_url(self.name, self.slug, self.pk)


class RelatedArticle(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    image_url = models.URLField(blank=True)
    products = models.ManyToManyField(InsuranceProduct, related_name="related_articles", blank=True)
    dropdown_items = models.ManyToManyField(DropdownItem, related_name="related_articles", blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Related Article"
        verbose_name_plural = "Related Articles"
    
    def __str__(self):
        return self.title


class CustomerReview(models.Model):
    product = models.ForeignKey(InsuranceProduct, related_name="reviews", on_delete=models.SET_NULL, null=True, blank=True)
    dropdown_item = models.ForeignKey(DropdownItem, related_name="reviews", on_delete=models.SET_NULL, null=True, blank=True)
    author = models.CharField(max_length=150)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Customer Review"
        verbose_name_plural = "Customer Reviews"
    
    def __str__(self):
        return f"{self.author} Review"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(FAQCategory, related_name="posts", on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to="blog/", blank=True, null=True)
    
    # SEO
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog_detail", args=[self.slug])

    @property
    def get_image_url(self):
        if self.image:
            return self.image.url
        return get_fake_hero_image_url(self.title, self.slug, self.pk)


class BlogImage(models.Model):
    post = models.ForeignKey(BlogPost, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="blog/gallery/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.post.title}"
