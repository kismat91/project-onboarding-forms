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
    date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'), required=False)

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
            'birth_date': forms.DateInput(format='%Y-%m-%d'), 
            'date': forms.DateInput(format='%Y-%m-%d'),
        }

class ContractorAgreementForm(forms.ModelForm):
    class Meta:
        model = ContractorAgreement
        fields = '__all__'
        widgets = {
            'bdate': forms.DateInput(format='%d:%m:%Y'),
            'cDate': forms.DateInput(format='%d:%m:%Y'),
        }
        initial = {
            'brokerName': 'Anjana Budhathoki',
            'bName': 'Anjana Budhathoki',
            'bTitle': 'Principal Broker',
            'forumLocation': 'Fairfax, Virginia',
            'bAddress': '8280 Willow Oaks Corp Dr. Suite 600 Fairfax, VA 22031',
            'bAttention': 'Anjana Budhathoki',
            'bFacsimileNo': 'NA',
            'agreementDuration': 'one year',
            'terminationDays': '30 days',
            'commissionTimePeriod': '5 days',
        }

class CommissionAgreementForm(forms.ModelForm):
    class Meta:
        model = CommissionAgreement
        fields = '__all__'
        widgets = {
            'agreementExpiryDate': forms.DateInput(format='%d:%m:%Y'),
        }
