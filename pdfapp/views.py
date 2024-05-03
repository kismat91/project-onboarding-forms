from django.shortcuts import render, redirect
from .forms import UserDetailsForm, DirectDepositForm, ContractorAgreementForm, CommissionAgreementForm
from fillpdf import fillpdfs
from .drive import DriveUploader


OUTPUT_LOCAL_FOLDER_PATH = 'output_files'

def process_pdf(pdf_template_path, output_path, data_dict):
    # Logic to fill out PDF form with user details
    fillpdfs.write_fillable_pdf(pdf_template_path, output_path, data_dict)

def user_details_form(request):
    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        web_form_fields = dict(form.data)
        web_form_fields.pop('csrfmiddlewaretoken')
        web_form_fields_keys = list(web_form_fields.keys())

        # Concept 1: Get form data from the web form and fill PDF
        if form.is_valid():
            form_fields = list(fillpdfs.get_form_fields('automatePDF/Agent_information_sheet.pdf').keys())
            final_dict = {form_fields[i]: web_form_fields[web_form_fields_keys[i]][0] for i in range(len(form_fields))}
            fillpdfs.write_fillable_pdf('automatePDF/Agent_information_sheet.pdf', f'{OUTPUT_LOCAL_FOLDER_PATH}/Agent_information.pdf', final_dict)
            return redirect('direct_deposit_form')

    else:
        form = UserDetailsForm()

    return render(request, 'pdfapp/user_details_form.html', {'form': form})


def direct_deposit_form(request):
    if request.method == 'POST':
        form = DirectDepositForm(request.POST)
        web_form_fields = dict(form.data)
        web_form_fields.pop('csrfmiddlewaretoken')
        web_form_fields_keys = list(web_form_fields.keys())
        # Attempt to fill PDF using web form data
        if form.is_valid():
            form_fields = list(fillpdfs.get_form_fields('automatePDF/Direct_Deposit_Form.pdf').keys())
            final_dict = {form_fields[i]: web_form_fields[web_form_fields_keys[i]][0] for i in range(len(form_fields))}
            fillpdfs.write_fillable_pdf('automatePDF/Direct_Deposit_Form.pdf', f'{OUTPUT_LOCAL_FOLDER_PATH}/direct_deposit.pdf', final_dict)
            return redirect('contractor_agreement_form')

    else:
        form = DirectDepositForm()

    return render(request, 'pdfapp/direct_deposit_form.html', {'form': form})


def contractor_agreement_form(request):
    if request.method == 'POST':
        form = ContractorAgreementForm(request.POST)
        web_form_fields = dict(form.data)
        web_form_fields.pop('csrfmiddlewaretoken')
        web_form_fields_keys = list(web_form_fields.keys())

        # Attempt to fill PDF using web form data
        if form.is_valid():
            form_fields = list(fillpdfs.get_form_fields('automatePDF/Independent_contractor_agreement.pdf').keys())
            final_dict = {form_fields[i]: web_form_fields[web_form_fields_keys[i]][0] for i in range(len(form_fields))}
            print(final_dict)
            fillpdfs.write_fillable_pdf('automatePDF/Independent_contractor_agreement.pdf', f'{OUTPUT_LOCAL_FOLDER_PATH}/contractor_agreement.pdf', final_dict)
            return redirect('commission_agreement_form')

    else:
        form = ContractorAgreementForm()

    return render(request, 'pdfapp/contractor_agreement_form.html', {'form': form})

def commission_agreement_form(request):
    uploader = DriveUploader()
    if request.method == 'POST':
        form = CommissionAgreementForm(request.POST)
        web_form_fields = dict(form.data)
        web_form_fields.pop('csrfmiddlewaretoken')
        web_form_fields_keys = list(web_form_fields.keys())
        web_form_fields_items = list(web_form_fields.items())
                                
        try:
            web_form_fields_items.insert(web_form_fields_keys.index('exclusive')+1, ('nonExclusive', [None]))
            web_form_fields = dict(web_form_fields_items)
            web_form_fields['exclusive'] = ['Yes_pgge']
            web_form_fields_keys = list(web_form_fields.keys())
            web_form_fields_items = list(web_form_fields.items())
        except:
            web_form_fields_items.insert(1, ('exclusive', [None]))
            web_form_fields_items.insert(2, ('nonExclusive', ['Yes_rjaw']))
            web_form_fields = dict(web_form_fields_items)
            web_form_fields_keys = list(web_form_fields.keys())
            
        try:
            web_form_fields_items.insert(web_form_fields_keys.index('notApplicableExpenses')+1, ('applicableExpenses', [None]))
            web_form_fields = dict(web_form_fields_items)
            web_form_fields['notApplicableExpenses'] = ['Yes_xavj']
            web_form_fields_keys = list(web_form_fields.keys())
            web_form_fields_items = list(web_form_fields.items())
        except:
            web_form_fields_items.insert(16, ('notApplicableExpenses', [None]))
            web_form_fields_items.insert(17, ('applicableExpenses', ['Yes_vkfk']))
            web_form_fields = dict(web_form_fields_items)
            web_form_fields_keys = list(web_form_fields.keys())
            
        try:
            web_form_fields_items.insert(web_form_fields_keys.index('notApplicable')+1, ('applicable', [None]))
            web_form_fields = dict(web_form_fields_items)
            web_form_fields['notApplicable'] = ['Yes_aecf']
            web_form_fields_keys = list(web_form_fields.keys())
            web_form_fields_items = list(web_form_fields.items())
        except:
            web_form_fields_items.insert(23, ('notApplicable', [None]))
            web_form_fields_items.insert(24, ('applicable', ['Yes_kzvw']))
            web_form_fields = dict(web_form_fields_items)
            web_form_fields_keys = list(web_form_fields.keys())

        try:
            web_form_fields_items.insert(web_form_fields_keys.index('notapplicableExclussion')+1, ('applicableExclusion', [None]))
            web_form_fields = dict(web_form_fields_items)
            web_form_fields['notapplicableExclussion'] = ['Yes_jqla']
            web_form_fields_keys = list(web_form_fields.keys())
            web_form_fields_items = list(web_form_fields.items())
        except:
            web_form_fields_items.insert(31, ('notapplicableExclussion', [None]))
            web_form_fields_items.insert(32, ('applicableExclusion', ['Yes_erku']))
            web_form_fields = dict(web_form_fields_items)
            web_form_fields_keys = list(web_form_fields.keys())

        # Attempt to fill PDF using web form data
        if form.is_valid():
            form_fields = list(fillpdfs.get_form_fields('automatePDF/Commission_agreement.pdf').keys())
            final_dict = {form_fields[i]: web_form_fields[web_form_fields_keys[i]][0] for i in range(len(form_fields))}
            fillpdfs.write_fillable_pdf('automatePDF/Commission_agreement.pdf', f'{OUTPUT_LOCAL_FOLDER_PATH}/commission_agreement.pdf', final_dict)
            uploader.upload_files(OUTPUT_LOCAL_FOLDER_PATH)
            return redirect('success')

    else:
        form = CommissionAgreementForm()

    return render(request, 'pdfapp/commission_agreement_form.html', {'form': form})


def success(request):
    return render(request, 'pdfapp/success.html')
