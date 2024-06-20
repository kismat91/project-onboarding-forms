from django import forms
from .models import UserDetails, ContractorAgreement, CommissionAgreement

class CombinedForm(forms.ModelForm):
    # Additional fields from DirectDeposit
    bank_name = forms.CharField(max_length=100, required=False)
    bank_address = forms.CharField(max_length=200, required=False)
    bank_city = forms.CharField(max_length=100, required=False)
    bank_state = forms.CharField(max_length=100, required=False)
    bank_zipcode = forms.CharField(max_length=100, required=False)
    fax_number = forms.CharField(max_length=20, required=False)
    bank_phone_number = forms.CharField(max_length=20, required=False)
    account_number = forms.CharField(max_length=100, required=False)
    bank_route_number = forms.CharField(max_length=100, required=False)
    type_of_account = forms.CharField(max_length=100, required=False)
    date = forms.DateField(widget=forms.DateInput(format='%m-%d-%Y'), required=False)

    class Meta:
        model = UserDetails
        fields = [
            'first_name', 'last_name', 'middle_name', 'street_address', 'apartment_number',
            'city', 'state', 'zip_code', 'home_phone', 'alternate_phone', 'email',
            'ssn_or_gov_id', 'birth_date', 'marital_status', 'spouse_name', 
            'spouse_employer', 'spouse_work_phone', 'referred_by',
            'bank_name', 'bank_address', 'bank_city', 'bank_state', 'bank_zipcode',
            'fax_number', 'bank_phone_number', 'account_number', 'bank_route_number',
            'type_of_account', 'date'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}), 
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ContractorAgreementForm(forms.ModelForm):
    COMMISSION_CHOICES_B = [
        ('20%', '20% (Self Generated - 80-20%)'),
        ('10%', '10% (Self Generated - 90-10%)'),
        ('$1000', '$1000 FLAT (Office Generated - 50-50%)')
    ]

    COMMISSION_CHOICES_C = [
        ('80%', '80% (Self Generated - 80-20%)'),
        ('90%', '90% (Self Generated - 90-10%)'),
        ('$1000', '$1000 FLAT (Office Generated - 50-50%)')
    ]

    bCommission = forms.ChoiceField(choices=COMMISSION_CHOICES_B, initial='20%')
    cCommission = forms.ChoiceField(choices=COMMISSION_CHOICES_C, initial='80%')

    class Meta:
        model = ContractorAgreement
        fields = '__all__'
        widgets = {
            'bdate': forms.DateInput(attrs={'type': 'date'}),
            'cDate': forms.DateInput(attrs={'type': 'date'}),
            'agreementEffectiveDate': forms.DateInput(attrs={'type': 'date'}),
        }
        

class CommissionAgreementForm(forms.ModelForm):
    class Meta:
        model = CommissionAgreement
        fields = '__all__'
        widgets = {
            'effective_date': forms.DateInput(attrs={'type': 'date'}),
            'employer_sign_date': forms.DateInput(attrs={'type': 'date'}),
            'employee_sign_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'effective_date': 'Effective Date',
            
            
            'employee_title': 'Employee Title',
            
            'employer_sign_date': 'Employer Sign Date',
            'employee_sign_date': 'Employee Sign Date',
        }

