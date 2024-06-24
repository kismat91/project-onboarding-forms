from django import forms
from .models import UserDetails, ContractorAgreement, CommissionAgreement
import datetime

class CombinedForm(forms.ModelForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('This field is required.')
        if not '@' in email:
            raise forms.ValidationError('Enter a valid email address.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        for field in self.Meta.required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, 'This field is required.')
        return cleaned_data

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
    date = forms.DateField(widget=forms.DateInput(format='%m-%d-%Y'))

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
        required_fields = [
            'first_name', 'last_name', 'street_address', 'city', 'state', 'zip_code', 
            'home_phone', 'email', 'ssn_or_gov_id', 'birth_date', 'marital_status'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}), 
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ContractorAgreementForm(forms.ModelForm):
    DAY_CHOICES = [(str(i), str(i)) for i in range(1, 32)]
    MONTH_CHOICES = [(str(i), str(i)) for i in range(1, 13)]
    YEAR_CHOICES = [(str(i), str(i)) for i in range(datetime.datetime.now().year, datetime.datetime.now().year + 5)]
    YEAR_CHOICES_LAST_TWO = [(str(i)[2:], str(i)[2:]) for i in range(datetime.datetime.now().year, datetime.datetime.now().year + 5)]

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

    contractDay = forms.ChoiceField(choices=DAY_CHOICES, initial='1')
    contractMonth = forms.ChoiceField(choices=MONTH_CHOICES, initial='1')
    contractYear = forms.ChoiceField(choices=YEAR_CHOICES, initial=str(datetime.datetime.now().year))
    effectiveDayOfAgreement = forms.ChoiceField(choices=DAY_CHOICES, initial='1')
    effectiveMonthOfAgreement = forms.ChoiceField(choices=MONTH_CHOICES, initial='1')
    effectiveYearOfAgreement = forms.ChoiceField(choices=YEAR_CHOICES_LAST_TWO, initial=str(datetime.datetime.now().year)[2:])

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
