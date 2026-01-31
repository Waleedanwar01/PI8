from django.contrib import admin
from django import forms
from django.shortcuts import redirect
from django.db import models

from .models import SiteConfig, MainPage, DropdownItem, PaymentPartner, QuoteRequest, QuoteRequestDocument, PolicyChangeRequest, SupportRequest, FileUploadRequest, SalesSupportRequest, FAQCategory, FAQItem, InsuranceCoverageType, InsuranceProduct, RelatedArticle, CustomerReview, BlogPost, BlogImage

# Clean default admin: move Requests and Insurance/FAQs to dedicated admin sites
_to_unreg = [
    QuoteRequest,
    PolicyChangeRequest,
    SupportRequest,
    FileUploadRequest,
    SalesSupportRequest,
    InsuranceCoverageType,
    InsuranceProduct,
    FAQCategory,
    FAQItem,
]
for _m in _to_unreg:
    if _m in admin.site._registry:
        admin.site.unregister(_m)

@admin.register(SalesSupportRequest)
class SalesSupportRequestAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)

@admin.register(FileUploadRequest)
class FileUploadRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at", "file_link")
    search_fields = ("name", "email", "phone")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "file_link")

    def file_link(self, obj):
        if obj.file:
            return forms.utils.mark_safe(f'<a href="{obj.file.url}" target="_blank">Download File</a>')
        return "No file"
    file_link.short_description = "Uploaded File"

@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)

@admin.register(PolicyChangeRequest)
class PolicyChangeRequestAdmin(admin.ModelAdmin):
    list_display = ("your_name", "company_name", "email", "created_at")
    search_fields = ("your_name", "company_name", "email", "phone")
    list_filter = ("created_at", "driver_change_type", "vehicle_change_type")
    readonly_fields = ("created_at",)

    fieldsets = (
        ("General Info", {
            "fields": ("your_name", "company_name", "email", "phone", "operate_state")
        }),
        ("Driver Change", {
            "fields": ("driver_change_type", "driver_name", "driver_dob", "driver_license")
        }),
        ("Vehicle Change", {
            "fields": ("vehicle_change_type", "vehicle_year", "vehicle_make_model", "vehicle_vin", "vehicle_coverage", "vehicle_value")
        }),
        ("Meta", {
            "fields": ("created_at",)
        }),
    )

@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
	fieldsets = (
		("Basic", {"fields": ("site_name", "homepage_title")}),
		("Contact", {"fields": ("phone_number", "email")}),
		(
			"Hero",
			{
				"fields": (
					"hero_title",
					"hero_tagline",
					"hero_description",
					"hero_image",
				)
			},
		),
		("Branding", {"fields": ("logo", "favicon")}),
		(
			"States",
			{
				"fields": ("serving_states_list", "coming_soon_states_list"),
				"description": "Enter comma-separated lists of states (e.g. 'CA, NY, TX').",
			}
		),
		(
			"Social links",
			{
				"fields": (
					"facebook_url",
					"instagram_url",
					"twitter_url",
					"linkedin_url",
					"youtube_url",
				)
			},
		),
	)

	list_display = ("site_name", "phone_number", "email", "updated_at")

	def has_add_permission(self, request):
		if SiteConfig.objects.exists():
			return False
		return super().has_add_permission(request)

	def changelist_view(self, request, extra_context=None):
		cfg = SiteConfig.objects.first()
		if cfg:
			return redirect(f"{cfg.pk}/change/")
		return super().changelist_view(request, extra_context=extra_context)


@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "url", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "slug")
    fieldsets = (
        ("Basic", {"fields": ("title", "slug", "url", "order", "is_active")}),
        ("Hero", {"fields": ("hero_title", "hero_subtitle", "hero_image")}),
        ("Content", {"fields": ("content", "content_width", "layout_columns")}),
        ("SEO", {"fields": ("meta_title", "meta_description", "meta_keywords", "og_image")}),
    )
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(attrs={"class": "vLargeTextField tinymce-editor"})
        },
    }
    
    class Media:
        js = [
            "https://cdnjs.cloudflare.com/ajax/libs/tinymce/6.8.3/tinymce.min.js",
            "/static/core/tinymce-init.js",
        ]


@admin.register(DropdownItem)
class DropdownItemAdmin(admin.ModelAdmin):
    list_display = ("title", "main_page", "url", "order", "is_active", "product_link", "faq_link")
    list_editable = ("order", "is_active")
    list_filter = ("main_page", "is_active")
    search_fields = ("title", "url", "description", "main_page__title")
    autocomplete_fields = ("main_page",)
    fieldsets = (
        ("Basic", {"fields": ("main_page", "title", "slug", "url", "description", "order", "is_active")}),
        ("Hero", {"fields": ("hero_title", "hero_subtitle", "hero_image")}),
        ("Card Media", {"fields": ("image", "icon_svg")}),
        ("Content", {"fields": ("content", "content_width", "layout_columns")}),
        ("SEO", {"fields": ("meta_title", "meta_description", "meta_keywords")}),
        ("Related", {"fields": ("product_link", "faq_link")}),
    )
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(attrs={"class": "vLargeTextField tinymce-editor"})
        },
    }
    readonly_fields = ("product_link", "faq_link")
    def product_link(self, obj):
        return _related_change_link(obj, "insurance_product", "Insurance Product")
    product_link.short_description = "Insurance Product"
    def faq_link(self, obj):
        return _related_change_link(obj, "faq_category", "FAQ Category")
    faq_link.short_description = "FAQ Category"
    
    class Media:
        js = [
            "https://cdnjs.cloudflare.com/ajax/libs/tinymce/6.8.3/tinymce.min.js",
            "/static/core/tinymce-init.js",
        ]


@admin.register(PaymentPartner)
class PaymentPartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "payment_url", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "description")


class QuoteRequestDocumentInline(admin.TabularInline):
    model = QuoteRequestDocument
    extra = 0
    readonly_fields = ("file_preview", "uploaded_at")
    fields = ("file", "file_preview", "uploaded_at")

    def file_preview(self, obj):
        if obj.file:
            return forms.utils.mark_safe(f'<a href="{obj.file.url}" target="_blank">Download {obj.file.name}</a>')
        return "No file"
    file_preview.short_description = "Preview"


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("business_name", "contact_name", "email", "phone", "contact_preference", "created_at")
    search_fields = ("business_name", "contact_name", "email", "phone", "city", "state_address")
    list_filter = ("created_at", "is_new_business", "is_currently_insured", "contact_preference")
    readonly_fields = ("created_at", "loss_runs_file_preview")
    inlines = [QuoteRequestDocumentInline]

    fieldsets = (
        ("General Information", {
            "fields": (
                "business_name", "phone", "proposed_start_date",
                "contact_name", "email", "website", "fein"
            )
        }),
        ("Address", {
            "fields": ("street_address", "city", "state_address", "zip_code")
        }),
        ("Business Details", {
            "fields": (
                "is_new_business", "description_of_operation",
                "cities_of_operation", "operate_state"
            )
        }),
        ("Loss History", {
            "fields": ("number_of_losses", "loss_runs_file", "loss_runs_file_preview")
        }),
        ("Insurance History", {
            "fields": (
                "is_currently_insured", "current_carrier",
                "radius_of_operation", "years_in_business"
            )
        }),
        ("Coverage Limits", {
            "fields": (
                "general_liability_needed",
                "general_liability_limits",
                "auto_liability_limits"
            )
        }),
        ("Meta", {
            "fields": ("created_at",)
        }),
    )

    def loss_runs_file_preview(self, obj):
        if obj.loss_runs_file:
             return forms.utils.mark_safe(f'<a href="{obj.loss_runs_file.url}" target="_blank">Download {obj.loss_runs_file.name}</a>')
        return "No file"
    loss_runs_file_preview.short_description = "Loss Runs File Preview"

def _related_change_link(obj, related_attr, label):
    rel = getattr(obj, related_attr, None)
    if rel:
        return forms.utils.mark_safe(f'<a href="/admin/core/{rel._meta.model_name}/{rel.pk}/change/" target="_blank">Edit {label}</a>')
    return forms.utils.mark_safe(f'<span style="color:#999">No {label} linked</span>')


class FAQSubCategoryInline(admin.TabularInline):
    model = FAQItem
    extra = 1

class BlogPostInline(admin.TabularInline):
    model = BlogPost
    extra = 0
    fields = ("title", "is_active", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True

class FAQCategoryInline(admin.TabularInline):
    model = FAQCategory
    extra = 1
    fields = ("name", "slug", "order", "is_active")
    show_change_link = True

@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "insurance_product", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("insurance_product",)
    inlines = [FAQSubCategoryInline, BlogPostInline]

class FAQItemInline(admin.StackedInline):
    model = FAQItem
    extra = 1
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(attrs={"class": "vLargeTextField tinymce-editor"})
        },
    }

    

@admin.register(InsuranceCoverageType)
class InsuranceCoverageTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "description")
    ordering = ("order", "name")

@admin.register(InsuranceProduct)
class InsuranceProductAdmin(admin.ModelAdmin):
    list_display = ("name", "dropdown_item", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "slug")
    autocomplete_fields = ("dropdown_item", "coverages")
    filter_horizontal = ("coverages",)
    ordering = ("order", "name")
    fieldsets = (
        ("Basic", {"fields": ("name", "slug", "dropdown_item", "order", "is_active")}),
        ("Coverages", {"fields": ("coverages",)}),
    )
    inlines = [FAQCategoryInline]
    
# RelatedArticle removed from admin as per request to consolidate logic
# @admin.register(RelatedArticle)
# class RelatedArticleAdmin(admin.ModelAdmin):
#    list_display = ("title", "order", "is_active")
#    list_editable = ("order", "is_active")
#    search_fields = ("title", "url")
#    filter_horizontal = ("products",)
#    ordering = ("order", "-created_at")

@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ("author", "product", "order", "is_active", "created_at")
    list_editable = ("order", "is_active")
    search_fields = ("author", "content")
    list_filter = ("product", "is_active")
    ordering = ("order", "-created_at")

class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1
    fields = ("image", "caption", "order")

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("category", "is_active", "created_at")
    search_fields = ("title", "content", "meta_title")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Basic Info", {"fields": ("title", "slug", "category", "image", "order", "is_active")}),
        ("Content", {"fields": ("content",)}),
        ("SEO", {"fields": ("meta_title", "meta_description", "meta_keywords")}),
        ("Meta", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")
    inlines = [BlogImageInline]
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(attrs={"class": "vLargeTextField tinymce-editor"})
        },
    }
    
    class Media:
        js = [
            "https://cdnjs.cloudflare.com/ajax/libs/tinymce/6.8.3/tinymce.min.js",
            "/static/core/tinymce-init.js",
        ]

@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "show_on_home", "order", "is_active")
    list_editable = ("show_on_home", "order", "is_active")
    list_filter = ("category", "show_on_home", "is_active")
    search_fields = ("question", "answer")
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(attrs={"class": "vLargeTextField tinymce-editor"})
        },
    }
    
    class Media:
        js = [
            "https://cdnjs.cloudflare.com/ajax/libs/tinymce/6.8.3/tinymce.min.js",
            "/static/core/tinymce-init.js",
        ]
