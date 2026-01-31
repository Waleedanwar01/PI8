from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
from datetime import datetime
from .models import SiteConfig, MainPage, DropdownItem, PaymentPartner, QuoteRequest, QuoteRequestDocument, PolicyChangeRequest, SupportRequest, FileUploadRequest, SalesSupportRequest, FAQCategory, FAQItem, get_fake_hero_image_url, InsuranceProduct, BlogPost
from .forms import UploadFileForm, SupportForm, QuoteRequestForm, PolicyChangeForm, SalesSupportForm, QuickQuoteForm

@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        file = request.FILES.get('file')
        if file:
            # Generate a unique filename
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{timestamp}_{file.name}"
            
            # Save the file
            save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'tinymce')
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            
            with open(os.path.join(save_path, filename), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            # Return the URL
            location = os.path.join(settings.MEDIA_URL, 'uploads', 'tinymce', filename).replace('\\', '/')
            return JsonResponse({'location': location})
    return JsonResponse({'error': 'Upload failed'}, status=400)

class PlaceholderMainPage:
	def __init__(self, slug):
		self.slug = slug
		self.title = slug.replace("-", " ").title()
		self.hero_title = self.title
		self.hero_subtitle = "Coming Soon..."
		self.meta_title = self.title
		self.meta_description = f"Information about {self.title}"
		self.meta_keywords = ""
		self.content = "<p class='text-center text-xl'>This page is under construction. Please check back soon!</p>"
		self.layout_columns = 1
		self.dropdown_items = DropdownItem.objects.none()
		self.pk = 0 # Dummy PK
	
	@property
	def get_hero_image_url(self):
		return get_fake_hero_image_url(self.title, self.slug)
	
	def get_absolute_url(self):
		return f"/p/{self.slug}/"

class PlaceholderDropdownItem:
	def __init__(self, slug):
		self.slug = slug
		self.title = slug.replace("-", " ").title()
		self.hero_title = self.title
		self.hero_subtitle = "Coming Soon..."
		self.meta_title = self.title
		self.meta_description = f"Information about {self.title}"
		self.meta_keywords = ""
		self.content = "<p class='text-center text-xl'>This page is under construction. Please check back soon!</p>"
		self.layout_columns = 1
		self.main_page = PlaceholderMainPage("home") # Dummy parent
		self.pk = 0 # Dummy PK
	
	@property
	def get_hero_image_url(self):
		return get_fake_hero_image_url(self.title, self.slug)
	
	def get_absolute_url(self):
		return f"/d/{self.slug}/"


def home(request):
    services = MainPage.objects.filter(show_on_home=True, is_active=True).order_by('order')
    serving_states = DropdownItem.objects.filter(main_page__slug='states', is_active=True).order_by('title')
    faq_items = FAQItem.objects.filter(is_active=True, show_on_home=True).select_related('category').order_by('category__order', 'order')
    latest_posts = BlogPost.objects.filter(is_active=True).order_by('-created_at')[:3]
    
    if request.method == "POST":
        quick_quote_form = QuickQuoteForm(request.POST)
        if quick_quote_form.is_valid():
            quote_request = quick_quote_form.save()
            
            # Send Email
            config = SiteConfig.get_solo()
            subject = f"New Quick Quote Request from {quote_request.business_name or quote_request.contact_name}"
            body = f"""
            New Quick Quote Request Received from Home Page:
            
            Contact Name: {quote_request.contact_name}
            Business Name: {quote_request.business_name}
            State: {quote_request.operate_state}
            Email: {quote_request.email}
            Phone: {quote_request.phone}
            New Business: {quote_request.is_new_business}
            Contact Preference: {quote_request.contact_preference}
            
            View full details in the Admin Panel: 
            {request.scheme}://{request.get_host()}/admin/core/quoterequest/{quote_request.pk}/change/
            """
            
            to_email = config.email if config.email else "admin@example.com"
            
            email_msg = EmailMessage(
                subject,
                body,
                to=[to_email],
                reply_to=[quote_request.email],
            )
            
            try:
                email_msg.send()
                messages.success(request, "Your quote request has been sent successfully! We will contact you soon.")
                return redirect("home")
            except Exception as e:
                print(f"Email Error: {e}")
                messages.error(request, "There was an error sending your request. Please try again.")
    else:
        quick_quote_form = QuickQuoteForm()

    return render(request, "core/home.html", {
        'services': services, 
        'serving_states': serving_states, 
        'faq_items': faq_items, 
        'latest_posts': latest_posts,
        'quick_quote_form': quick_quote_form
    })


def upload_success(request):
	return render(request, "core/upload_success.html")

def faq_view(request):
    categories = FAQCategory.objects.filter(is_active=True).prefetch_related("items")
    
    # Fake a page object for the template to render hero, etc. if needed
    page = PlaceholderMainPage("faqs")
    page.title = "Frequently Asked Questions"
    page.hero_title = "Frequently Asked Questions"
    page.hero_subtitle = "Find answers to common questions"
    
    return render(request, "core/faq.html", {"categories": categories, "item": page})


def main_page_detail(request, slug: str):
	try:
		page = MainPage.objects.prefetch_related("dropdown_items").get(slug=slug, is_active=True)
	except MainPage.DoesNotExist:
		# If page doesn't exist, create a placeholder so user doesn't see error
		page = PlaceholderMainPage(slug)

	# Special handling for Blog page
	if slug == "blog":
		return blog_list(request, page_obj=page)

	# If a product exists with this slug, render product-style layout on main page URL
	product = InsuranceProduct.objects.filter(slug=slug, is_active=True).first()
	if product:
		categories = product.faq_categories.filter(is_active=True).prefetch_related("items")
		coverages = product.coverages.filter(is_active=True).order_by("order", "name")
		
		# Fetch related blog posts via FAQCategory
		related_articles = BlogPost.objects.filter(
			category__insurance_product=product, 
			is_active=True
		).order_by("-created_at")
		
		reviews = list(getattr(product, "reviews", []).filter(is_active=True).order_by("order", "-created_at")) if hasattr(product, "reviews") else []
		config = SiteConfig.get_solo()
		if request.method == "POST":
			form = QuoteRequestForm(request.POST, request.FILES)
			if form.is_valid():
				quote_request = form.save()
				files = request.FILES.getlist('misc_files')
				for f in files:
					QuoteRequestDocument.objects.create(quote_request=quote_request, file=f)
				subject = f"New Quote Request from {quote_request.business_name}"
				body = f"""
				New Quote Request Received:
				
				Business Name: {quote_request.business_name}
				Contact Name: {quote_request.contact_name}
				Email: {quote_request.email}
				Phone: {quote_request.phone}
				Contact Preference: {quote_request.contact_preference or 'N/A'}
				
				View full details and download files in the Admin Panel: 
				{request.scheme}://{request.get_host()}/admin/core/quoterequest/{quote_request.pk}/change/
				"""
				to_email = config.email if config.email else "admin@example.com"
				email_msg = EmailMessage(
					subject,
					body,
					to=[to_email],
					reply_to=[quote_request.email],
				)
				if 'loss_runs_file' in request.FILES:
					f = request.FILES['loss_runs_file']
					f.seek(0)
					email_msg.attach(f.name, f.read(), f.content_type)
				for misc_doc in quote_request.documents.all():
					f = misc_doc.file
					try:
						f.open('rb')
						email_msg.attach(f.name, f.read())
						f.close()
					except Exception as e:
						print(f"Error attaching file {f.name}: {e}")
				try:
					email_msg.send()
					return redirect("upload_success")
				except Exception as e:
					print(f"Email Error: {e}")
					messages.error(request, "There was an error sending your request. Please try again.")
		else:
			form = QuoteRequestForm()
		# Reuse dropdown_item template with page as item for hero/background
		return render(
			request,
			"core/dropdown_item.html",
			{
				"item": page,
				"siblings": [],
				"quote_form": form,
				"insurance_product": product,
				"faq_categories": categories,
				"coverages": coverages,
				"related_articles": related_articles,
				"customer_reviews": reviews,
			},
		)
	
	# Special handling for Request a Quote page
	if "request-a-quote" in slug:
		# Override placeholder text if needed
		if isinstance(page, PlaceholderMainPage):
			page.hero_subtitle = "Get a free quote today"
			page.content = ""

		config = SiteConfig.get_solo() # Still need it for email
		if request.method == "POST":
			form = QuoteRequestForm(request.POST, request.FILES)
			if form.is_valid():
				quote_request = form.save()
				
				# Handle multiple files
				files = request.FILES.getlist('misc_files')
				for f in files:
					QuoteRequestDocument.objects.create(quote_request=quote_request, file=f)
				
				# Send Email
				subject = f"New Quote Request from {quote_request.business_name}"
				body = f"""
				New Quote Request Received:
				
				Business Name: {quote_request.business_name}
				Contact Name: {quote_request.contact_name}
				Email: {quote_request.email}
				Phone: {quote_request.phone}
				Contact Preference: {quote_request.contact_preference or 'N/A'}
				
				View full details and download files in the Admin Panel: 
				{request.scheme}://{request.get_host()}/admin/core/quoterequest/{quote_request.pk}/change/
				"""
				
				to_email = config.email if config.email else "admin@example.com"
				
				email_msg = EmailMessage(
					subject,
					body,
					to=[to_email],
					reply_to=[quote_request.email],
				)
				
				# Attach loss runs file if exists
				if 'loss_runs_file' in request.FILES:
					f = request.FILES['loss_runs_file']
					f.seek(0)
					email_msg.attach(f.name, f.read(), f.content_type)

				# Attach misc files
				for misc_doc in quote_request.documents.all():
					f = misc_doc.file
					try:
						f.open('rb')
						email_msg.attach(f.name, f.read())
						f.close()
					except Exception as e:
						print(f"Error attaching file {f.name}: {e}")
				
				try:
					email_msg.send()
					return redirect("upload_success")
				except Exception as e:
					print(f"Email Error: {e}")
					messages.error(request, "There was an error sending your request. Please try again.")
		else:
			form = QuoteRequestForm()
			
		return render(
			request,
			"core/request_quote.html",
			{"item": page, "form": form},
		)

	return render(request, "core/main_page.html", {"page": page})


def dropdown_item_detail(request, slug: str):
	try:
		item = DropdownItem.objects.select_related("main_page").get(slug=slug, is_active=True)
		siblings = (
			item.main_page.dropdown_items.filter(is_active=True)
			.exclude(pk=item.pk)
			.order_by("order")
		)
	except DropdownItem.DoesNotExist:
		# If item doesn't exist, create a placeholder
		item = PlaceholderDropdownItem(slug)
		siblings = []

	# Category-first insurance page
	if hasattr(item, "faq_category") and item.faq_category:
		category = item.faq_category
		coverages = category.coverages.filter(is_active=True).order_by("order", "name")

		config = SiteConfig.get_solo()
		if request.method == "POST":
			form = QuoteRequestForm(request.POST, request.FILES)
			if form.is_valid():
				quote_request = form.save()
				files = request.FILES.getlist('misc_files')
				for f in files:
					QuoteRequestDocument.objects.create(quote_request=quote_request, file=f)
				subject = f"New Quote Request from {quote_request.business_name}"
				body = f"""
				New Quote Request Received:
				
				Business Name: {quote_request.business_name}
				Contact Name: {quote_request.contact_name}
				Email: {quote_request.email}
				Phone: {quote_request.phone}
				Contact Preference: {quote_request.contact_preference or 'N/A'}
				
				View full details and download files in the Admin Panel: 
				{request.scheme}://{request.get_host()}/admin/core/quoterequest/{quote_request.pk}/change/
				"""
				to_email = config.email if config.email else "admin@example.com"
				email_msg = EmailMessage(
					subject,
					body,
					to=[to_email],
					reply_to=[quote_request.email],
				)
				if 'loss_runs_file' in request.FILES:
					f = request.FILES['loss_runs_file']
					f.seek(0)
					email_msg.attach(f.name, f.read(), f.content_type)
				for misc_doc in quote_request.documents.all():
					f = misc_doc.file
					try:
						f.open('rb')
						email_msg.attach(f.name, f.read())
						f.close()
					except Exception as e:
						print(f"Error attaching file {f.name}: {e}")
				try:
					email_msg.send()
					return redirect("upload_success")
				except Exception as e:
					print(f"Email Error: {e}")
					messages.error(request, "There was an error sending your request. Please try again.")
		else:
			form = QuoteRequestForm()

		return render(
			request,
			"core/dropdown_item.html",
			{
				"item": item,
				"siblings": siblings,
				"quote_form": form,
				"faq_category": category,
                "faq_categories": [category],
				"coverages": coverages,
			},
		)

	# Insurance product page with fixed form + FAQs
	if hasattr(item, "insurance_product") and item.insurance_product:
		product = item.insurance_product
		categories = product.faq_categories.filter(is_active=True).prefetch_related("items")
		coverages = product.coverages.filter(is_active=True).order_by("order", "name")
		related_articles = list(getattr(product, "related_articles", []).all()) if hasattr(product, "related_articles") else []
		reviews = list(getattr(product, "reviews", []).filter(is_active=True).order_by("order", "-created_at")) if hasattr(product, "reviews") else []

		config = SiteConfig.get_solo()
		if request.method == "POST":
			form = QuoteRequestForm(request.POST, request.FILES)
			if form.is_valid():
				quote_request = form.save()
				files = request.FILES.getlist('misc_files')
				for f in files:
					QuoteRequestDocument.objects.create(quote_request=quote_request, file=f)
				subject = f"New Quote Request from {quote_request.business_name}"
				body = f"""
				New Quote Request Received:
				
				Business Name: {quote_request.business_name}
				Contact Name: {quote_request.contact_name}
				Email: {quote_request.email}
				Phone: {quote_request.phone}
				Contact Preference: {quote_request.contact_preference or 'N/A'}
				
				View full details and download files in the Admin Panel: 
				{request.scheme}://{request.get_host()}/admin/core/quoterequest/{quote_request.pk}/change/
				"""
				to_email = config.email if config.email else "admin@example.com"
				email_msg = EmailMessage(
					subject,
					body,
					to=[to_email],
					reply_to=[quote_request.email],
				)
				if 'loss_runs_file' in request.FILES:
					f = request.FILES['loss_runs_file']
					f.seek(0)
					email_msg.attach(f.name, f.read(), f.content_type)
				for misc_doc in quote_request.documents.all():
					f = misc_doc.file
					try:
						f.open('rb')
						email_msg.attach(f.name, f.read())
						f.close()
					except Exception as e:
						print(f"Error attaching file {f.name}: {e}")
				try:
					email_msg.send()
					return redirect("upload_success")
				except Exception as e:
					print(f"Email Error: {e}")
					messages.error(request, "There was an error sending your request. Please try again.")
		else:
			form = QuoteRequestForm()

		return render(
			request,
			"core/dropdown_item.html",
			{
				"item": item,
				"siblings": siblings,
				"quote_form": form,
				"insurance_product": product,
				"faq_categories": categories,
				"coverages": coverages,
				"related_articles": related_articles,
				"customer_reviews": reviews,
			},
		)

	# Special handling for Upload File page
	if "upload-a-file" in slug:
		# Override placeholder text if needed
		if isinstance(item, PlaceholderDropdownItem):
			item.hero_subtitle = "Secure Document Upload"
			item.content = ""

		config = SiteConfig.get_solo()
		if request.method == "POST":
			form = UploadFileForm(request.POST, request.FILES)
			if form.is_valid():
				name = form.cleaned_data["name"]
				email = form.cleaned_data["email"]
				phone = form.cleaned_data["phone"]
				uploaded_file = request.FILES["file"]

				# Save to Database
				FileUploadRequest.objects.create(
					name=name,
					email=email,
					phone=phone,
					file=uploaded_file
				)

				# Prepare Email
				subject = f"New File Submission from {name}"
				body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nPlease find the attached file."
				
				# Get Admin Email
				to_email = config.email if config.email else "admin@example.com"
				
				email_msg = EmailMessage(
					subject,
					body,
					to=[to_email],
					reply_to=[email],
				)
				email_msg.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
				
				try:
					email_msg.send()
					return redirect("upload_success")
				except Exception as e:
					print(f"Email Error: {e}")
					messages.error(request, "There was an error sending your file. Please try again.")
		else:
			form = UploadFileForm()
		
		return render(
			request,
			"core/dropdown_item.html",
			{"item": item, "siblings": siblings, "form": form},
		)

	# Special handling for Support for Current Clients page
	if "support-for-current-clients" in slug:
		# Override placeholder text if needed
		if isinstance(item, PlaceholderDropdownItem):
			item.hero_subtitle = "We are here to help"
			item.content = ""

		if request.method == "POST":
			config = SiteConfig.get_solo()
			form = SupportForm(request.POST)
			if form.is_valid():
				first_name = form.cleaned_data["first_name"]
				last_name = form.cleaned_data["last_name"]
				email = form.cleaned_data["email"]
				phone = form.cleaned_data["phone"]
				message = form.cleaned_data["message"]

				# Save to Database
				SupportRequest.objects.create(
					first_name=first_name,
					last_name=last_name,
					email=email,
					phone=phone,
					message=message
				)

				# Prepare Email
				subject = f"Support Request from {first_name} {last_name}"
				body = f"Name: {first_name} {last_name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
				
				# Get Admin Email
				to_email = config.email if config.email else "admin@example.com"
				
				email_msg = EmailMessage(
					subject,
					body,
					to=[to_email],
					reply_to=[email],
				)
				
				try:
					email_msg.send()
					return redirect("upload_success") # Reuse success page
				except Exception as e:
					print(f"Email Error: {e}")
					messages.error(request, "There was an error sending your request. Please try again.")
		else:
			form = SupportForm()
		
		return render(
			request,
			"core/dropdown_item.html",
			{"item": item, "siblings": siblings, "support_form": form},
		)

	if "make-a-payment-online" in slug:
		# Override placeholder text if needed
		if isinstance(item, PlaceholderDropdownItem):
			item.hero_subtitle = "Secure Online Payments"
			item.content = ""

		payment_partners = PaymentPartner.objects.filter(is_active=True)
		return render(
			request,
			"core/dropdown_item.html",
			{
				"item": item,
				"siblings": siblings,
				"payment_partners": payment_partners
			},
		)

	if "sales-support" in slug:
		# Override placeholder text if needed
		if isinstance(item, PlaceholderDropdownItem):
			item.hero_subtitle = "Contact our Sales Team"
			item.content = ""

		if request.method == "POST":
			config = SiteConfig.get_solo()
			form = SalesSupportForm(request.POST)
			if form.is_valid():
				# Save to Database
				SalesSupportRequest.objects.create(
					first_name=form.cleaned_data["first_name"],
					last_name=form.cleaned_data["last_name"],
					email=form.cleaned_data["email"],
					phone=form.cleaned_data["phone"],
					operate_state=form.cleaned_data["operate_state"],
					message=form.cleaned_data["message"]
				)

				# Prepare Email
				subject = f"Sales Support Request from {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}"
				body = f"""
				New Sales Support Request:
				
				Name: {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}
				Email: {form.cleaned_data['email']}
				Phone: {form.cleaned_data['phone']}
				State: {form.cleaned_data['operate_state']}
				
				Message:
				{form.cleaned_data['message']}
				"""
				
				# Get Admin Email
				to_email = config.email if config.email else "admin@example.com"
				
				email_msg = EmailMessage(
					subject,
					body,
					to=[to_email],
					reply_to=[form.cleaned_data['email']],
				)
				
				try:
					email_msg.send()
					return redirect("upload_success")
				except Exception as e:
					print(f"Email Error: {e}")
					messages.error(request, "There was an error sending your request. Please try again.")
		else:
			form = SalesSupportForm()
		
		return render(
			request,
			"core/dropdown_item.html",
			{"item": item, "siblings": siblings, "sales_form": form},
		)

	if "policy-changes" in slug:
		# Override placeholder text if needed
		if isinstance(item, PlaceholderDropdownItem):
			item.hero_subtitle = "Update your policy information"
			item.content = ""
		if request.method == "POST":
			config = SiteConfig.get_solo()
			form = PolicyChangeForm(request.POST)
			if form.is_valid():
				# Extract Data
				data = form.cleaned_data
				
				# Save to Database
				PolicyChangeRequest.objects.create(
					your_name=data['your_name'],
					company_name=data['company_name'],
					email=data['email'],
					phone=data.get('phone', ''),
					operate_state=data.get('operate_state', ''),
					
					driver_change_type=data.get('driver_change_type', ''),
					driver_name=data.get('driver_name', ''),
					driver_dob=data.get('driver_dob') if data.get('driver_dob') else None,
					driver_license=data.get('driver_license', ''),
					
					vehicle_change_type=data.get('vehicle_change_type', ''),
					vehicle_year=data.get('vehicle_year', ''),
					vehicle_make_model=data.get('vehicle_make_model', ''),
					vehicle_vin=data.get('vehicle_vin', ''),
					vehicle_coverage=data.get('vehicle_coverage', ''),
					vehicle_value=data.get('vehicle_value', '')
				)

				# Prepare Email Body
				subject = f"Policy Change Request from {data['your_name']}"
				body = f"""
				New Policy Change Request:
				
				--- General Information ---
				Name: {data['your_name']}
				Company: {data['company_name']}
				Email: {data['email']}
				Phone: {data.get('phone', 'N/A')}
				State of Operation: {data.get('operate_state', 'N/A')}
				
				--- Driver Change ---
				Action: {data.get('driver_change_type', 'None')}
				Driver Name: {data.get('driver_name', 'N/A')}
				DOB: {data.get('driver_dob', 'N/A')}
				License: {data.get('driver_license', 'N/A')}
				
				--- Vehicle Change ---
				Action: {data.get('vehicle_change_type', 'None')}
				Year: {data.get('vehicle_year', 'N/A')}
				Make/Model: {data.get('vehicle_make_model', 'N/A')}
				VIN: {data.get('vehicle_vin', 'N/A')}
				Comp/Collision: {data.get('vehicle_coverage', 'N/A')}
				Value: {data.get('vehicle_value', 'N/A')}
				"""
				
				# Get Admin Email
				to_email = config.email if config.email else "admin@example.com"
				
				email_msg = EmailMessage(
					subject,
					body,
					to=[to_email],
					reply_to=[data['email']],
				)
				
				try:
					email_msg.send()
					return redirect("upload_success")
				except Exception as e:
					print(f"Email Error: {e}")
					messages.error(request, "There was an error sending your request. Please try again.")
		else:
			form = PolicyChangeForm()
			
		return render(
			request,
			"core/dropdown_item.html",
			{"item": item, "siblings": siblings, "policy_form": form},
		)

	# Fallback for generic pages (including State pages)
	config = SiteConfig.get_solo()

	# Fetch related content
	faq_categories = []
	if hasattr(item, "faq_category") and item.faq_category:
		faq_categories = [item.faq_category]
	elif hasattr(item, "insurance_product") and item.insurance_product:
		faq_categories = item.insurance_product.faq_categories.all()
	
	reviews = item.reviews.filter(is_active=True).order_by("order", "-created_at")
	
	# Fetch related articles (BlogPosts) based on category
	# If we have FAQ categories, we can find blog posts in those categories
	related_articles = BlogPost.objects.none()
	if faq_categories:
		related_articles = BlogPost.objects.filter(
			category__in=faq_categories, 
			is_active=True
		).order_by("-created_at")[:3]
	
	# Fallback: If no category-specific posts, show recent posts
	if not related_articles.exists():
		related_articles = BlogPost.objects.filter(is_active=True).order_by("-created_at")[:3]

	if request.method == "POST":
		form = QuoteRequestForm(request.POST, request.FILES)
		if form.is_valid():
			quote_request = form.save()
			files = request.FILES.getlist('misc_files')
			for f in files:
				QuoteRequestDocument.objects.create(quote_request=quote_request, file=f)
			subject = f"New Quote Request from {quote_request.business_name}"
			body = f"""
			New Quote Request Received:
			
			Business Name: {quote_request.business_name}
			Contact Name: {quote_request.contact_name}
			Email: {quote_request.email}
			Phone: {quote_request.phone}
			Contact Preference: {quote_request.contact_preference or 'N/A'}
			
			View full details and download files in the Admin Panel: 
			{request.scheme}://{request.get_host()}/admin/core/quoterequest/{quote_request.pk}/change/
			"""
			to_email = config.email if config.email else "admin@example.com"
			email_msg = EmailMessage(
				subject,
				body,
				to=[to_email],
				reply_to=[quote_request.email],
			)
			if 'loss_runs_file' in request.FILES:
				f = request.FILES['loss_runs_file']
				f.seek(0)
				email_msg.attach(f.name, f.read(), f.content_type)
			for misc_doc in quote_request.documents.all():
				f = misc_doc.file
				try:
					f.open('rb')
					email_msg.attach(f.name, f.read())
					f.close()
				except Exception as e:
					print(f"Error attaching file {f.name}: {e}")
			try:
				email_msg.send()
				return redirect("upload_success")
			except Exception as e:
				print(f"Email Error: {e}")
				messages.error(request, "There was an error sending your request. Please try again.")
	else:
		form = QuoteRequestForm()

	return render(
		request,
		"core/dropdown_item.html",
		{
			"item": item, 
			"siblings": siblings, 
			"quote_form": form,
			"faq_categories": faq_categories,
			"customer_reviews": reviews,
			"related_articles": related_articles,
		},
	)


def blog_list(request, page_obj=None):
    posts = BlogPost.objects.filter(is_active=True).order_by("-created_at")
    categories = FAQCategory.objects.filter(is_active=True).order_by("order")
    
    if page_obj:
        page = page_obj
    else:
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
    categories = FAQCategory.objects.filter(is_active=True).order_by("order")
    
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
