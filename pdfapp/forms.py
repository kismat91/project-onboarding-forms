from django import forms
from .models import UserDetails, DirectDeposit, ContractorAgreement, CommissionAgreement

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(format='%d:%m:%Y'),
        }

class DirectDepositForm(forms.ModelForm):
    class Meta:
        model = DirectDeposit
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(format='%d:%m:%Y'),
        }

class ContractorAgreementForm(forms.ModelForm):
    class Meta:
        model = ContractorAgreement
        fields = '__all__'
        widgets = {
            'bdate': forms.DateInput(format='%d:%m:%Y'),
            'cDate': forms.DateInput(format='%d:%m:%Y'),
        }

class CommissionAgreementForm(forms.ModelForm):
    class Meta:
        model = CommissionAgreement
        fields = '__all__'
        widgets = {
            'agreementExpiryDate': forms.DateInput(format='%d:%m:%Y'),
        }
