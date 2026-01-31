import os
import django
import random
from django.utils.text import slugify

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes_insurance.settings")
django.setup()

from core.models import BlogPost, FAQCategory, InsuranceProduct

def setup_blogs():
    # 1. Ensure we have a category
    # Try to find Limo Insurance product to link to
    limo_product = InsuranceProduct.objects.filter(name__icontains="Limo").first()
    
    category, created = FAQCategory.objects.get_or_create(name="Insurance Tips")
    
    if limo_product and not category.insurance_product:
        category.insurance_product = limo_product
        category.save()
        print(f"Linked 'Insurance Tips' category to '{limo_product.name}'")
    
    # 2. Define some blog posts content
    posts_data = [
        {
            "title": "Why You Need Taxi Insurance Today",
            "content": """
                <p>Driving a taxi is a demanding job that comes with its own set of risks. Unlike personal vehicles, taxis are on the road for longer hours, often in heavy traffic and diverse weather conditions. This increased exposure makes having the right insurance coverage not just a legal requirement, but a critical business asset.</p>
                <h3>Protecting Your Livelihood</h3>
                <p>Your vehicle is your primary source of income. If an accident occurs, you not only face repair costs but also lost wages while your car is off the road. Comprehensive taxi insurance can cover these repairs and sometimes even provide a replacement vehicle, ensuring you can get back to work as soon as possible.</p>
                <h3>Liability Coverage is Key</h3>
                <p> Accidents happen, even to the most experienced drivers. Liability coverage protects you if you're found at fault in an accident that injures a passenger or damages another vehicle. Without this coverage, you could be personally responsible for thousands of dollars in medical bills and property damage.</p>
                <p>Don't wait until it's too late. Review your policy today and make sure you're fully protected.</p>
            """,
            "image_url": "/media/hero/taxi.jpg"
        },
        {
            "title": "5 Tips for Lowering Your Commercial Insurance Cost",
            "content": """
                <p>Insurance is a necessary expense for any commercial driving business, but that doesn't mean you have to overpay. Here are five practical tips to help you reduce your premiums without sacrificing coverage.</p>
                <ol>
                    <li><strong>Hire Experienced Drivers:</strong> Insurers favor drivers with a clean record and years of experience. Thorough vetting can save you money in the long run.</li>
                    <li><strong>Install Dash Cams:</strong> Dash cams provide irrefutable evidence in the event of an accident, protecting you from fraudulent claims and potentially lowering your rates.</li>
                    <li><strong>Bundle Your Policies:</strong> Many insurers offer discounts if you purchase multiple types of coverage (like auto and general liability) from them.</li>
                    <li><strong>Increase Your Deductible:</strong> If you have enough cash reserves to cover minor repairs, raising your deductible can significantly lower your monthly premiums.</li>
                    <li><strong>Maintain Your Fleet:</strong> Regular maintenance prevents mechanical failures that could lead to accidents. Keep records to show insurers you're proactive.</li>
                </ol>
                <p>Talk to your agent today to see which of these savings you qualify for.</p>
            """,
             "image_url": "/media/hero/taxi.jpg" # Using safe local image
        },
        {
            "title": "Understanding Liability vs Full Coverage",
            "content": """
                <p>When shopping for commercial auto insurance, you'll often hear the terms "Liability Only" and "Full Coverage." Understanding the difference is crucial for making the right decision for your business.</p>
                <h3>Liability Insurance</h3>
                <p>This is typically the minimum coverage required by law. It covers damages and injuries you cause to <em>others</em> in an accident. It does <strong>not</strong> pay to repair your own vehicle.</p>
                <h3>Full Coverage (Physical Damage)</h3>
                <p>"Full coverage" usually refers to adding Collision and Comprehensive coverage to your liability policy. Collision pays for damage to your car from an accident, while Comprehensive covers non-collision events like theft, vandalism, fire, or weather damage.</p>
                <h3>Which Do You Need?</h3>
                <p>If your vehicle is financed, your lender will likely require full coverage. If your car is older and paid off, liability might be sufficient, but remember: if you total the car, you'll have to replace it out of pocket.</p>
            """,
             "image_url": "/media/hero/taxi.jpg"
        }
    ]

    print("Creating/Updating Blog Posts...")
    created_posts = []
    for data in posts_data:
        post, created = BlogPost.objects.get_or_create(
            title=data["title"],
            defaults={
                "content": data["content"],
                "category": category,
                "is_active": True,
                "meta_description": data["content"][:150]
            }
        )
        # Force update content and image just in case
        post.content = data["content"]
        # In a real scenario we'd handle images better, but for now we won't set the image field 
        # because it expects a file object, but we can assume the template handles it or we manually set path if needed.
        # Wait, the template uses `post.image.url`. 
        # Let's see if we can set it to a string relative path? No, ImageField needs a file.
        # But we can update RelatedArticle to point to these posts.
        post.save()
        created_posts.append(post)
        print(f"{'Created' if created else 'Updated'} post: {post.title}")

    print("\nDone! Blog system is populated.")

if __name__ == "__main__":
    setup_blogs()
