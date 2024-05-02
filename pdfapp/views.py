from django.shortcuts import render, redirect
from .forms import UserDetailsForm, DirectDepositForm, ContractorAgreementForm, CommissionAgreementForm
from fillpdf import fillpdfs
from drive import DriveUploader


OUTPUT_LOCAL_FOLDER_PATH = 'output_files'

def process_pdf(pdf_template_path, output_path, data_dict):
    # Logic to fill out PDF form with user details
    fillpdfs.write_fillable_pdf(pdf_template_path, output_path, data_dict)

def user_details_form(request):
    print('user_details_form')

    if request.method == 'POST':
        print('user_details_form')
        form = UserDetailsForm(request.POST)
        web_form_fields = dict(form.data)
        web_form_fields.pop('csrfmiddlewaretoken')
        web_form_fields_keys = list(web_form_fields.keys())

        # Concept 1: Get form data from the web form and fill PDF
        if form.is_valid():
            print('user_details_form')
            form_fields = list(fillpdfs.get_form_fields('/Users/kismatkhatri/Downloads/automatePDF/Agent_information_sheet.pdf').keys())
            final_dict = {form_fields[i]: web_form_fields[web_form_fields_keys[i]][0] for i in range(len(form_fields))}
            print(final_dict)
            fillpdfs.write_fillable_pdf('/Users/kismatkhatri/Downloads/automatePDF/Agent_information_sheet.pdf', f'{OUTPUT_LOCAL_FOLDER_PATH}/Agent_information.pdf', final_dict)
            return redirect('direct-deposit')

    else:
        form = UserDetailsForm()

    return render(request, 'pdfapp/user_details_form.html', {'form': form})


def direct_deposit_form(request):
    if request.method == 'POST':
        form = DirectDepositForm(request.POST)
        web_form_fields = dict(form.data)
        web_form_fields.pop('csrfmiddlewaretoken')
        web_form_fields_keys = list(web_form_fields.keys())
        print(web_form_fields)
        print(len(web_form_fields_keys))
        # Attempt to fill PDF using web form data
        if form.is_valid():
            print('direct_deposit_form')
            form_fields = list(fillpdfs.get_form_fields('/Users/kismatkhatri/Downloads/automatePDF/Direct_Deposit_Form.pdf').keys())
            print(form_fields)
            print(len(form_fields))
            final_dict = {form_fields[i]: web_form_fields[web_form_fields_keys[i]][0] for i in range(len(form_fields))}
            print(final_dict)
            fillpdfs.write_fillable_pdf('/Users/kismatkhatri/Downloads/automatePDF/Direct_Deposit_Form.pdf', f'{OUTPUT_LOCAL_FOLDER_PATH}/direct_deposit.pdf', final_dict)
            return redirect('contractor-agreement')

    else:
        form = DirectDepositForm()

    return render(request, 'pdfapp/direct_deposit_form.html', {'form': form})


def contractor_agreement_form(request):
    print('contractor_agreement_form')
    if request.method == 'POST':
        form = ContractorAgreementForm(request.POST)
        web_form_fields = dict(form.data)
        web_form_fields.pop('csrfmiddlewaretoken')
        web_form_fields_keys = list(web_form_fields.keys())

        # Attempt to fill PDF using web form data
        if form.is_valid():
            form_fields = list(fillpdfs.get_form_fields('/Users/kismatkhatri/Downloads/automatePDF/Independent_contractor_agreement.pdf').keys())
            final_dict = {form_fields[i]: web_form_fields[web_form_fields_keys[i]][0] for i in range(len(form_fields))}
            print(final_dict)
            fillpdfs.write_fillable_pdf('/Users/kismatkhatri/Downloads/automatePDF/Independent_contractor_agreement.pdf', f'{OUTPUT_LOCAL_FOLDER_PATH}/contractor_agreement.pdf', final_dict)
            return redirect('commission-agreement')

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
        
        # Handle checkboxes and convert their values accordingly
        checkboxes = ['exclusive', 'nonExclusive', 'notApplicableExpenses', 'applicableExpenses', 'notApplicable', 'applicable', 'notapplicableExclussion', 'applicableExclusion']
        for checkbox in checkboxes:
            if checkbox in web_form_fields and web_form_fields[checkbox][0] == 'on':
                web_form_fields[checkbox] = ['Yes']
            else:
                web_form_fields[checkbox] = [None]
        
        print(web_form_fields)
        print(len(web_form_fields_keys))

        # Attempt to fill PDF using web form data
        if form.is_valid():
            form_fields = list(fillpdfs.get_form_fields('/Users/kismatkhatri/Downloads/automatePDF/Commission_agreement.pdf').keys())
            print(form_fields)
            print(len(form_fields))
            final_dict = {form_fields[i]: web_form_fields[web_form_fields_keys[i]][0] for i in range(len(form_fields))}
            print(final_dict)
            fillpdfs.write_fillable_pdf('/Users/kismatkhatri/Downloads/automatePDF/Commission_agreement.pdf', f'{OUTPUT_LOCAL_FOLDER_PATH}/commission_agreement.pdf', final_dict)
            uploader.upload_files(OUTPUT_LOCAL_FOLDER_PATH)
            return redirect('success')

    else:
        form = CommissionAgreementForm()

    return render(request, 'pdfapp/commission_agreement_form.html', {'form': form})


def success(request):
    return render(request, 'pdfapp/success.html')
