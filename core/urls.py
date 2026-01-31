from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('faqs/', views.faq_view, name='faq'),
    path('p/<slug:slug>/', views.main_page_detail, name='main_page_detail'),
    path('d/<slug:slug>/', views.dropdown_item_detail, name='dropdown_item_detail'),
    path('add-edit-driver-or-vehicle-list/', views.dropdown_item_detail, {'slug': 'policy-changes'}, name='add_edit_driver_vehicle'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('upload-success/', views.upload_success, name='upload_success'),
]
