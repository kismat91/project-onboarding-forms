# Create your models here.
from django.db import models

class UserDetails(models.Model):
    fist_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
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

    def __str__(self):
        return self.fist_name
    
class DirectDeposit(models.Model):
    payee_name = models.CharField(max_length=100, null=True)
    payee_address = models.CharField(max_length=100, null=True)
    payee_city = models.CharField(max_length=100, null=True)
    payee_state = models.CharField(max_length=100, null=True)
    payee_phone_number = models.CharField(max_length=100, null=True)
    payee_fax_number = models.CharField(max_length=100, null=True)
    payee_home_number = models.CharField(max_length=100, null=True)
    payee_work_number = models.CharField(max_length=100, null=True)
    payee_ssn = models.CharField(max_length=100, null=True)
    payee_identification_number = models.CharField(max_length=100, null=True)
    bank_name = models.CharField(max_length=100, null=True)
    bank_address_1 = models.CharField(max_length=100, null=True)
    bank_address_2 = models.CharField(max_length=100, blank=True)
    bank_address_3 = models.CharField(max_length=100, blank=True)
    bank_address_4 = models.CharField(max_length=100, blank=True)
    bank_phone_number = models.CharField(max_length=100, null=True)
    fax_number = models.CharField(max_length=100, null=True)
    bank_route_number = models.CharField(max_length=100, null=True)
    account_number = models.CharField(max_length=100, null=True)
    type_of_account = models.CharField(max_length=100, null=True)
    date = models.DateTimeField()

    def __str__(self):
        return self.payee_name

class ContractorAgreement(models.Model):
    contractDay = models.CharField(max_length=2)
    contractMonth = models.CharField(max_length=2)
    contractYear = models.CharField(max_length=4)
    brokerName = models.CharField(max_length=100)
    employeeName = models.CharField(max_length=100)
    age = models.CharField(max_length=3)
    ssn = models.CharField(max_length=10)
    contractorLocation = models.CharField(max_length=100)
    effectiveDayOfAgreement = models.CharField(max_length=2)
    effectiveMonthOfAgreement = models.CharField(max_length=2)
    effectiveYearOfAgreement = models.CharField(max_length=4)
    commissionTimePeriod = models.CharField(max_length=2)
    bCommission = models.CharField(max_length=10)
    cCommission = models.CharField(max_length=10)
    agreementDuration = models.CharField(max_length=2)
    agreementEffectiveDate = models.DateField()
    terminationDays = models.CharField(max_length=3)
    bAddress = models.CharField(max_length=100)
    bAttention = models.CharField(max_length=100)
    bFacsimileNo = models.CharField(max_length=20)
    cAddress = models.CharField(max_length=100)
    cAttention = models.CharField(max_length=100)
    cFacsimileNo = models.CharField(max_length=20)
    forumLocation = models.CharField(max_length=100)
    bName = models.CharField(max_length=100)
    bTitle = models.CharField(max_length=100)
    bdate = models.DateField()
    bWitness = models.CharField(max_length=100)
    cName = models.CharField(max_length=100)
    cTitle = models.CharField(max_length=100)
    cDate = models.DateField()
    cWitness = models.CharField(max_length=100)

    def __str__(self):
        return self.contractDay
    
class CommissionAgreement(models.Model):
    agentName = models.CharField(max_length=100)
    exclusive = models.BooleanField(default=False)
    companyPurpose1 = models.CharField(max_length=100)
    companyPurpose2 = models.CharField(max_length=100)
    companyPurpose3 = models.CharField(max_length=100)
    companyPurpose4 = models.CharField(max_length=100)
    agentDuties1 = models.CharField(max_length=100)
    agentDuties2 = models.CharField(max_length=100)
    agentDuties3 = models.CharField(max_length=100)
    agentDuties4 = models.CharField(max_length=100)
    commissionPercentage = models.CharField(max_length=100)
    additionalDetails1 = models.CharField(max_length=100)
    additionalDetails2 = models.CharField(max_length=100)
    additionalDetails3 = models.CharField(max_length=100)
    additionalDetails4 = models.CharField(max_length=100)
    notApplicableExpenses = models.BooleanField(default=False)
    expensesDetails1 = models.CharField(max_length=100)
    expensesDetails2 = models.CharField(max_length=100)
    expensesDetails3 = models.CharField(max_length=100)
    expensesDetails4 = models.CharField(max_length=100)
    agreementExpiryDate = models.DateField()
    notApplicable = models.BooleanField(default=False)
    incrementDay = models.CharField(max_length=100)
    incrementMonth = models.CharField(max_length=100)
    incrementYear = models.CharField(max_length=100)
    noticeDay = models.CharField(max_length=100)
    printedNameOfAgent = models.CharField(max_length=100)
    agentAddress = models.CharField(max_length=100)
    notapplicableExclussion = models.BooleanField(default=False)
    agreementPages = models.CharField(max_length=100)
    agreementDay = models.CharField(max_length=100)
    agreementMonth = models.CharField(max_length=100)
    agreementYear = models.CharField(max_length=100)
    nameOfCompanyRepresentative = models.CharField(max_length=100)
    nameOfAgent = models.CharField(max_length=100)

    def __str__(self):
        return self.agentName

    

    