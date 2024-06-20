# Create your models here.
from django.db import models
class UserDetails(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    street_address = models.CharField(max_length=200)
    apartment_number = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    home_phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    ssn_or_gov_id = models.CharField(max_length=20)
    birth_date = models.DateField()
    marital_status = models.CharField(max_length=50)
    spouse_name = models.CharField(max_length=100, blank=True, null=True)
    spouse_employer = models.CharField(max_length=200, blank=True, null=True)
    spouse_work_phone = models.CharField(max_length=20, blank=True, null=True)
    referred_by = models.CharField(max_length=100)
    
    bank_name = models.CharField(max_length=100)
    bank_address = models.CharField(max_length=200)
    bank_city = models.CharField(max_length=100, blank=True, null=True)
    bank_state = models.CharField(max_length=100, blank=True, null=True)
    bank_zipcode = models.CharField(max_length=100, blank=True, null=True)
    bank_phone_number = models.CharField(max_length=20)
    fax_number = models.CharField(max_length=20, blank=True, null=True)
    bank_route_number = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    type_of_account = models.CharField(max_length=100)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.first_name} {self.last_name}"
    
class ContractorAgreement(models.Model):
    contractDay = models.CharField(max_length=2)
    contractMonth = models.CharField(max_length=2)
    contractYear = models.CharField(max_length=4)
   
    # employeeName = models.CharField(max_length=100)3
    age = models.CharField(max_length=3)
    # ssn = models.CharField(max_length=10)5
    # contractorLocation = models.CharField(max_length=100)6
    effectiveDayOfAgreement = models.CharField(max_length=2)
    effectiveMonthOfAgreement = models.CharField(max_length=2)
    effectiveYearOfAgreement = models.CharField(max_length=4)
    
    bCommission = models.CharField(max_length=10)
    cCommission = models.CharField(max_length=10)
    
    agreementEffectiveDate = models.DateField()
    
    #cName = models.CharField(max_length=100)13
    
    # cAddress = models.CharField(max_length=100)14
    cAttention = models.CharField(max_length=100)
    
    
    
    bdate = models.DateField()
    bWitness = models.CharField(max_length=100)
    # cName = models.CharField(max_length=100)18
    cTitle = models.CharField(max_length=100)
    cDate = models.DateField()
    cWitness = models.CharField(max_length=100)

    def __str__(self):
        return self.contractDay
    
class CommissionAgreement(models.Model):
    effective_date = models.DateField()
    #agent_name = models.CharField(max_length=100)1
    #employee_name = models.CharField(max_length=100)2
    employee_title = models.CharField(max_length=100)
    #employee_address = models.CharField(max_length=255)4
    employer_sign_date = models.DateField()
    #employee_name2 = models.CharField(max_length=100)6
    #employee_title2 = models.CharField(max_length=100)7
    employee_sign_date = models.DateField()

    def __str__(self):
        return self.agentName

    

    