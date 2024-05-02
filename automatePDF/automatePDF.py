import datetime
from datetime import date
from fillpdf import fillpdfs

form_fields = list(fillpdfs.get_form_fields('Agent_information_sheet.pdf').keys())
form_fields1 = list(fillpdfs.get_form_fields('Direct_Deposit_Form.pdf').keys())
form_fields2 = list(fillpdfs.get_form_fields('Independent_contractor_agreement.pdf').keys())
form_fields3 = list(fillpdfs.get_form_fields('Commission_agreement.pdf').keys())


print(form_fields)
print(form_fields1)
print(form_fields2)
print(form_fields3)


agentFirstName = 'Akash'
agentMiddleName = 'Kumar'
agentLastName = 'Yadav'
agentStreetAddress = 'Ghodbunder Road'
agentAppartment = 'vhyang'
agentCity = 'Thane'
agentState = 'Maharashtra'
agentZipCode = '45801'
agentHomePhone = '9845845688'
agentAlternatePhone = '6788523301'
agentEmail = 'akash@gmail.com'
agentSSN = '789416620'
agentDOB = '02/02/2000'
agentMaritalStatus = 'unmarried'
agentSpouseName = 'Tati Yadav'
agentSpouseEmployer = 'Bakwas Tech Limited'
agentSpouseWorkPhone = '0468752623'
referedBy = 'Kismat Khatri'

payeeName = 'Lucky'
payeeAddress = 'NIT'
payeeCity = 'Rourkela'
payeeState = 'Udesha'
payeePhoneNumber = '9844557528'
payeeFaxNumber = '4544545454'
payeeHomeNumber = '656565664'
payeeWorkNumber = '24498421303'
payeeSSN = '77842632647'
payeeIdentificationNumber = '68771203145'
bankName = 'SBI'
bankAddress = 'KTM'
bankPhoneNumber = '8913131336'
FaxNumber = '549796611'
bankRouteNumber = '5448979131'
accountNumber ='789456123001'
typeOfAccount = 'saving'
date = datetime.datetime.today()

contractDay = '13'
contractMonth = '11'
contractYear = '2024'
brokerName = 'Akash'
employeeName = 'kismat'
age = '24'
ssn = '4656565'
contractorLocation = 'thane'
effectiveDayOfAgreement = '12'
effectiveMonthOfAgreement = '11'
effectiveYearOfAgreement = '2024'
commissionTimePeriod = '10'
bCommission = '1000'
cCommission = '1200'
agreementDuration = '12'
agreementEffectiveDate = '12/10/2025'
terminationDays = '90'
bAddress = 'anandnagar'
bAttention = 'shdjskjksj'
bFacsimileNo = '5656262'
cAddress = 'rampur'
cAttention = 'dsadjsj'
cFacsimileNo = '65656626'
forumLocation = 'andheri'
bName = 'kismat'
bTitle = 'developer'
bdate = date.today()
bWitness = 'rahul'
cName = 'Akash'
cTitle = 'Manager'
cDate = date.today()
cWitness = 'shyam'

agentName = 'Kismat Yadav'
exclusive = 'Yes_pgge'
nonExclusive = 'Yes_rjaw'
companyPurpose1 = 'aaaaa'
companyPurpose2 = 'bbbbb'
companyPurpose3 = 'ccccc'
companyPurpose4 = 'ddddd'
agentDuties1 = 'eeeeee'
agentDuties2 = 'ffffff'
agentDuties3 = 'gggggg'
agentDuties4 = 'hhhhhh'
commissionPercentage = '35'
additionalDetails1 = 'iii'
additionalDetails2 = 'jjj'
additionalDetails3 = 'kkk'
additionalDetails4 = 'lll'
notApplicableExpenses = 'Yes_xavj'
applicableExpenses = 'Yes_vkfk'
expensesDetails1 = 'mmm'
expensesDetails2 = 'nnn'
expensesDetails3 = 'ooo' 
expensesDetails4 = 'ppp'
agreementExpiryDate = '12/10/2024'
notApplicable = 'Yes_aecf'
applicable = 'Yes_kzvw'
incrementDay = '12'
incrementMonth = '10'
incrementYear = '5'
noticeDay = '20'
agentName = 'Lucky'
agentAddress = 'Sinja Jumla'
notapplicableExclussion = 'Yes_jqla'
applicableExclusion = 'Yes_erku'
agreementPages = '5'
agreementDay = '05'
agreemntMonth = '06'
agreementYear = '24'
nameOfCompanyRepresentative = ' Binita Khatri'
nameOfAgent = 'Kismat'

data_dict = {
        form_fields[0]: agentFirstName,
        form_fields[1]: agentMiddleName,
        form_fields[2]: agentLastName,
        form_fields[3]: agentStreetAddress,
        form_fields[4]: agentAppartment,
        form_fields[5]: agentCity,
        form_fields[6]: agentState,
        form_fields[7]: agentZipCode,
        form_fields[8]: agentHomePhone,
        form_fields[9]: agentAlternatePhone, 
        form_fields[10]: agentEmail,
        form_fields[11]: agentSSN,
        form_fields[12]: agentDOB,
        form_fields[13]: agentMaritalStatus,
        form_fields[14]: agentSpouseName,
        form_fields[15]: agentSpouseEmployer,
        form_fields[16]: agentSpouseWorkPhone,
        form_fields[17]: referedBy
}

data_dict1 = {
        form_fields1[0]: payeeName,
        form_fields1[1]: payeeAddress,
        form_fields1[2]: payeeCity,
        form_fields1[3]: payeeState,
        form_fields1[4]: payeeFaxNumber,
        form_fields1[5]: payeeHomeNumber,
        form_fields1[6]: payeeWorkNumber,
        form_fields1[7]: payeeSSN,
        form_fields1[8]: payeeIdentificationNumber,
        form_fields1[9]: bankName,
        form_fields1[10]: bankAddress,
        form_fields1[11]: bankAddress,
        form_fields1[12]: bankAddress,
        form_fields1[13]: bankAddress,
        form_fields1[14]: bankPhoneNumber,
        form_fields1[15]: FaxNumber,
        form_fields1[16]: bankRouteNumber,
        form_fields1[17]: accountNumber,
        form_fields1[18]: typeOfAccount,
        form_fields1[19]: date,
        form_fields1[20]: payeePhoneNumber
}

data_dict2 = {
        form_fields2[0]: contractDay,
        form_fields2[1]: contractMonth,
        form_fields2[2]: contractYear,
        form_fields2[3]: brokerName,
        form_fields2[4]: employeeName,
        form_fields2[5]: age,
        form_fields2[6]: ssn,
        form_fields2[7]: contractorLocation,
        form_fields2[8]: effectiveDayOfAgreement,
        form_fields2[9]: effectiveMonthOfAgreement,
        form_fields2[10]: effectiveYearOfAgreement,
        form_fields2[11]: commissionTimePeriod,
        form_fields2[12]: bCommission,
        form_fields2[13]: cCommission,
        form_fields2[14]: agreementDuration,
        form_fields2[15]: agreementEffectiveDate,
        form_fields2[16]: terminationDays,
        form_fields2[17]: bAddress,
        form_fields2[18]: bAttention,
        form_fields2[19]: bFacsimileNo,
        form_fields2[20]: cAddress,
		form_fields2[21]: cAttention,
        form_fields2[22]: cFacsimileNo,
        form_fields2[23]: forumLocation,
        form_fields2[24]: bName,
        form_fields2[25]: bTitle,
        form_fields2[26]: bdate,
        form_fields2[27]: bWitness,
        form_fields2[28]: cName,
        form_fields2[29]: cTitle,
        form_fields2[30]: cDate,
        form_fields2[31]: cWitness
}

data_dict3 = {
    form_fields3[0]: agentName ,
    form_fields3[1]: exclusive ,
    form_fields3[2]: nonExclusive ,
    form_fields3[3]: companyPurpose1 ,
    form_fields3[4]: companyPurpose2 ,
    form_fields3[5]: companyPurpose3 ,
    form_fields3[6]: companyPurpose4 ,
    form_fields3[7]: agentDuties1 ,
    form_fields3[8]: agentDuties2 ,
    form_fields3[9]: agentDuties3 ,
    form_fields3[10]: agentDuties4 ,
    form_fields3[11]: commissionPercentage ,
    form_fields3[12]: additionalDetails1 ,
    form_fields3[13]: additionalDetails2 ,
    form_fields3[14]: additionalDetails3 ,
    form_fields3[15]: additionalDetails4 ,
    form_fields3[16]: notApplicableExpenses ,
    form_fields3[17]: applicableExpenses ,
    form_fields3[18]: expensesDetails1 ,
    form_fields3[19]: expensesDetails2 ,
    form_fields3[20]: expensesDetails3 ,
    form_fields3[21]: expensesDetails4 ,
    form_fields3[22]: agreementExpiryDate ,
    form_fields3[23]: notApplicable ,
    form_fields3[24]: applicable ,
    form_fields3[25]: incrementDay ,
    form_fields3[26]: incrementMonth ,
    form_fields3[27]: incrementYear ,
    form_fields3[28]: noticeDay ,
    form_fields3[29]: agentName ,
    form_fields3[30]: agentAddress ,
    form_fields3[31]: notapplicableExclussion ,
    form_fields3[32]: applicableExclusion ,
    form_fields3[33]: agreementPages ,
    form_fields3[34]: agreementDay ,
    form_fields3[35]: agreemntMonth ,
    form_fields3[36]: agreementYear ,
    form_fields3[37]: nameOfCompanyRepresentative ,
    form_fields3[38]: nameOfAgent 
}

fillpdfs.write_fillable_pdf('Agent_information_sheet.pdf', 'new.pdf', data_dict)
fillpdfs.write_fillable_pdf('Direct_Deposit_Form.pdf', 'new1.pdf', data_dict1)
fillpdfs.write_fillable_pdf('Independent_contractor_agreement.pdf', 'new2.pdf', data_dict2)
fillpdfs.write_fillable_pdf('Commission_agreement.pdf', 'new3.pdf', data_dict3)
