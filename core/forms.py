from django import forms
from .models import QuoteRequest

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class QuoteRequestForm(forms.ModelForm):
    misc_files = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True, 'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-none file:border-0 file:text-sm file:font-semibold file:bg-[#e5e7eb] file:text-gray-700 hover:file:bg-gray-200'}),
        required=False,
        label="Misc Document Upload"
    )

    class Meta:
        model = QuoteRequest
        exclude = ['created_at']
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border', 'placeholder': 'Business Name'}),
            'phone': forms.TextInput(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border', 'placeholder': 'Phone'}),
            'proposed_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border'}),
            'contact_name': forms.TextInput(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border', 'placeholder': 'Email'}),
            'website': forms.URLInput(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border', 'placeholder': 'http://'}),
            'fein': forms.TextInput(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border'}),
            'street_address': forms.TextInput(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border'}),
            'city': forms.TextInput(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border'}),
            'state_address': forms.TextInput(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border'}),
            'zip_code': forms.TextInput(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border'}),
            'is_new_business': forms.RadioSelect(choices=[("Yes", "Yes"), ("No", "No")]),
            'description_of_operation': forms.Textarea(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border h-32'}),
            'cities_of_operation': forms.Textarea(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border h-32'}),
            'operate_state': forms.TextInput(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border', 'placeholder': 'State'}),
            'number_of_losses': forms.NumberInput(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border'}),
            'loss_runs_file': forms.ClearableFileInput(attrs={'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-none file:border-0 file:text-sm file:font-semibold file:bg-[#e5e7eb] file:text-gray-700 hover:file:bg-gray-200'}),
            'is_currently_insured': forms.Select(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border'}),
            'current_carrier': forms.TextInput(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border'}),
            'radius_of_operation': forms.TextInput(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border'}),
            'years_in_business': forms.NumberInput(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border'}),
            'general_liability_needed': forms.Select(attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border'}),
            'general_liability_limits': forms.Select(choices=[
                ("", "Select Liability Limits"),
                ("N/A", "N/A"),
                ("$1 Million", "$1 Million"),
                ("$2 Million", "$2 Million"),
                ("$2,000,000", "$2,000,000"),
                ("$1,500,000", "$1,500,000"),
                ("$1,050,000", "$1,050,000"),
                ("$1,000,000", "$1,000,000"),
                ("$500,000", "$500,000"),
                ("$300,000", "$300,000"),
                ("$100,000 / $300,000 / $50,000", "$100,000 / $300,000 / $50,000"),
                ("$100,000 / $300,000 / $25,000", "$100,000 / $300,000 / $25,000")
            ], attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border'}),
            'auto_liability_limits': forms.Select(choices=[
                ("", "Select Liability Limits"),
                ("100,000", "100,000"),
                ("300,000", "300,000"),
                ("500,000", "500,000"),
                ("750,000", "750,000"),
                ("1,000,000", "1,000,000"),
                ("1,500,000", "1,500,000"),
                ("5,000,000", "5,000,000")
            ], attrs={'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-2 border'}),
            'contact_preference': forms.RadioSelect(choices=[
                ("Email", "via Email"),
                ("Phone", "via Phone")
            ]),
        }
        labels = {
            'contact_name': 'Name*',
            'business_name': 'Business Name*',
            'operate_state': 'What state do you operate in?*',
            'email': 'Email*',
            'phone': 'Phone*',
            'is_new_business': 'Is this a new business?*',
            'contact_preference': 'How should we contact you to complete your application?*'
        }

class QuickQuoteForm(forms.ModelForm):
    contact_name = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={'class': 'w-full bg-[#FBB03B] border border-white/80 text-white text-sm px-4 py-2 focus:outline-none focus:border-white focus:ring-0 placeholder-white/90', 'placeholder': 'Your Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'w-full bg-[#FBB03B] border border-white/80 text-white text-sm px-4 py-2 focus:outline-none focus:border-white focus:ring-0 placeholder-white/90', 'placeholder': 'Email'})
    )
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'w-full bg-[#FBB03B] border border-white/80 text-white text-sm px-4 py-2 focus:outline-none focus:border-white focus:ring-0 placeholder-white/90', 'placeholder': 'Phone'})
    )

    class Meta:
        model = QuoteRequest
        fields = ['contact_name', 'business_name', 'operate_state', 'email', 'phone', 'is_new_business', 'contact_preference']
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'w-full bg-[#FBB03B] border border-white/80 text-white text-sm px-4 py-2 focus:outline-none focus:border-white focus:ring-0 placeholder-white/90', 'placeholder': 'Business Name'}),
            'operate_state': forms.TextInput(attrs={'class': 'w-full bg-[#FBB03B] border border-white/80 text-white text-sm px-4 py-2 focus:outline-none focus:border-white focus:ring-0 placeholder-white/90', 'placeholder': 'What state do you operate in?'}),
            'is_new_business': forms.RadioSelect(choices=[("Yes", "Yes"), ("No", "No")], attrs={'class': 'form-radio text-[#8B183F]'}),
            'contact_preference': forms.RadioSelect(choices=[("Email", "via Email"), ("Phone", "via Phone")], attrs={'class': 'form-radio text-[#8B183F]'}),
        }

class UploadFileForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border',
        'placeholder': ''
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border',
        'placeholder': ''
    }))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border',
        'placeholder': ''
    }))
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-none file:border-0 file:text-sm file:font-semibold file:bg-[#8B183F] file:text-white hover:file:bg-[#6b1230]',
    }))

class SupportForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border',
        'placeholder': 'First'
    }))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border',
        'placeholder': 'Last'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border',
        'placeholder': ''
    }))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border',
        'placeholder': ''
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border h-32',
        'placeholder': ''
    }))

class PolicyChangeForm(forms.Form):
    # General Info
    your_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border'
    }))
    company_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border'
    }))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border'
    }))
    operate_state = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border'
    }))

    # Driver Change
    driver_change_type = forms.ChoiceField(
        choices=[('Add', 'Add Driver'), ('Delete', 'Delete Driver')],
        widget=forms.RadioSelect,
        required=False
    )
    driver_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border'
    }))
    driver_dob = forms.DateField(required=False, widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border'
    }))
    driver_license = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border'
    }))

    # Vehicle Change
    vehicle_change_type = forms.ChoiceField(
        choices=[('Add', 'Add Vehicle'), ('Delete', 'Delete Vehicle')],
        widget=forms.RadioSelect,
        required=False
    )
    vehicle_year = forms.CharField(max_length=4, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border'
    }))
    vehicle_make_model = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border'
    }))
    vehicle_vin = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border'
    }))
    vehicle_coverage = forms.ChoiceField(
        choices=[('Yes', 'Yes'), ('No', 'No')],
        widget=forms.RadioSelect,
        required=False
    )
    vehicle_value = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border'
    }))

class SalesSupportForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border',
        'placeholder': 'First'
    }))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border',
        'placeholder': 'Last'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border',
        'placeholder': ''
    }))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border',
        'placeholder': ''
    }))
    operate_state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border',
        'placeholder': ''
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w-full border-gray-300 shadow-sm focus:border-[#8B183F] focus:ring-[#8B183F] sm:text-sm p-3 border h-32',
        'placeholder': ''
    }))
