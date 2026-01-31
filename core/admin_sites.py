from django.contrib import admin
from django import forms
from django.db import models
from .models import (
    QuoteRequest, QuoteRequestDocument, PolicyChangeRequest,
    SupportRequest, FileUploadRequest, SalesSupportRequest,
    InsuranceCoverageType, InsuranceProduct,
    FAQCategory, FAQItem
)
from .models import DropdownItem

# Dedicated admin sites
class RequestsAdminSite(admin.AdminSite):
    site_header = "Requests Admin"
    site_title = "Requests Admin"
    index_title = "Manage Requests"

class InsuranceAdminSite(admin.AdminSite):
    site_header = "Insurance & FAQs Admin"
    site_title = "Insurance Admin"
    index_title = "Manage Insurance and FAQs"

requests_admin_site = RequestsAdminSite(name="requests_admin")
insurance_admin_site = InsuranceAdminSite(name="insurance_admin")

# ---------------- Requests registrations ----------------
class QuoteRequestDocumentInline(admin.TabularInline):
    model = QuoteRequestDocument
    extra = 0
    readonly_fields = ("uploaded_at",)
    fields = ("file", "uploaded_at")

@admin.register(QuoteRequest, site=requests_admin_site)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("business_name", "contact_name", "email", "phone", "contact_preference", "created_at")
    search_fields = ("business_name", "contact_name", "email", "phone", "city", "state_address")
    list_filter = ("created_at", "is_new_business", "is_currently_insured", "contact_preference")
    readonly_fields = ("created_at",)
    inlines = [QuoteRequestDocumentInline]

@admin.register(PolicyChangeRequest, site=requests_admin_site)
class PolicyChangeRequestAdmin(admin.ModelAdmin):
    list_display = ("your_name", "company_name", "email", "created_at")
    search_fields = ("your_name", "company_name", "email", "phone")
    list_filter = ("created_at", "driver_change_type", "vehicle_change_type")
    readonly_fields = ("created_at",)

@admin.register(SupportRequest, site=requests_admin_site)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)

@admin.register(FileUploadRequest, site=requests_admin_site)
class FileUploadRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)

@admin.register(SalesSupportRequest, site=requests_admin_site)
class SalesSupportRequestAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)

# ---------------- Insurance & FAQs registrations ----------------
@admin.register(InsuranceCoverageType, site=insurance_admin_site)
class InsuranceCoverageTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "description")
    ordering = ("order", "name")

class FAQCategoryInline(admin.TabularInline):
    model = FAQCategory
    extra = 1
    fields = ("name", "slug", "order", "is_active")
    show_change_link = True

@admin.register(InsuranceProduct, site=insurance_admin_site)
class InsuranceProductAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "slug", "title", "description")
    filter_horizontal = ("coverages",)
    ordering = ("order", "name")
    fieldsets = (
        ("Basic", {"fields": ("name", "slug", "title", "description", "order", "is_active")}),
        ("Meta Data", {"fields": ("meta_title", "meta_description", "meta_keywords")}),
        ("Linking", {"fields": ("dropdown_item",)}),
        ("Coverages", {"fields": ("coverages",)}),
    )
    inlines = [FAQCategoryInline]

class FAQItemInline(admin.StackedInline):
    model = FAQItem
    extra = 1
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(attrs={"class": "vLargeTextField"})
        },
    }

@admin.register(FAQCategory, site=insurance_admin_site)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "dropdown_item", "order", "is_active")
    list_editable = ("order", "is_active")
    filter_horizontal = ("coverages",)
    fieldsets = (
        ("Basic", {"fields": ("name", "slug", "dropdown_item", "order", "is_active")}),
        ("Coverages", {"fields": ("coverages",)}),
    )
    inlines = [FAQItemInline]

class FAQItemInline(admin.StackedInline):
    model = FAQItem
    extra = 1
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(attrs={"class": "vLargeTextField"})
        },
    }

@admin.register(FAQItem, site=insurance_admin_site)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("category",)
    search_fields = ("question", "answer")
