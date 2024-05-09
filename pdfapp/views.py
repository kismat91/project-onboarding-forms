from django.shortcuts import render, redirect, reverse
from .forms import ContractorAgreementForm, CommissionAgreementForm, CombinedForm
from fillpdf import fillpdfs
import os
from django.http import HttpResponseNotFound, FileResponse
import pandas as pd
from urllib.parse import quote
from sqllite_test.sqlite_conn import DatabaseManager
from sqllite_test.email import EmailSender
import uuid
from zipfile import ZipFile, ZIP_DEFLATED
import mimetypes
import io

session_id = uuid.uuid4()

OUTPUT_LOCAL_FOLDER_PATH = 'output_files/{session_id}'.format(session_id=session_id)

def process_pdf(pdf_template_path, output_path, data_dict):
    # Logic to fill out PDF form with user details
    fillpdfs.write_fillable_pdf(pdf_template_path, output_path, data_dict)

def user_details(request):
    print(session_id)
    db = DatabaseManager("/root/project/real_estate_onboarding.db")
    email_sender = EmailSender()
    if request.method == 'POST':
        form = CombinedForm(request.POST)
        if form.is_valid():
            web_form_fields = dict(form.cleaned_data)
            # Specific paths for the PDF templates and outputs
            agent_info_template_path = 'automatePDF/Agent_information_sheet.pdf'
            agent_info_output_path = 'Agent_information_filled.pdf'
            direct_deposit_template_path = 'automatePDF/Direct_Deposit_Form.pdf'
            direct_deposit_output_path = 'Direct_Deposit_filled.pdf'

            # Generate UserDetails PDF
            user_details_pdf_fields = {
                'FirstName': web_form_fields['first_name'],
                'MiddleInitial': web_form_fields['middle_name'][:1] if web_form_fields['middle_name'] else '',  # Handle middle name being optional
                'LastName': web_form_fields['last_name'],
                'Address': f"{web_form_fields['street_address']}",
                'apartment_num': f"{web_form_fields.get('apartment_number', '')}",
                'City': web_form_fields['city'],
                'State': web_form_fields['state'],
                'ZipCode': web_form_fields['zip_code'],
                'HomePhone': web_form_fields['home_phone'],
                'AlternatePhone': web_form_fields.get('alternate_phone', ''),  # Handle optional fields
                'Email': web_form_fields['email'],
                'SSN': web_form_fields['ssn_or_gov_id'],
                'BirthDate': web_form_fields['birth_date'].strftime('%Y-%m-%d'),
                'MaritalStatus': web_form_fields['marital_status'],
                'SpouseName': web_form_fields.get('spouse_name', ''),
                'SpouseEmployer': web_form_fields.get('spouse_employer', ''),
                'SpouseWorkPhone': web_form_fields.get('spouse_work_phone', ''),
                'ReferredBy': web_form_fields.get('referred_by', ''),
            }
            user_details_pdf_fields_keys = list(user_details_pdf_fields.keys())
            keys_pdf = list(fillpdfs.get_form_fields(agent_info_template_path).keys())
            final_dict = {keys_pdf[i]:user_details_pdf_fields[user_details_pdf_fields_keys[i]] for i in range(len(keys_pdf))}
            if not os.path.exists(OUTPUT_LOCAL_FOLDER_PATH):
                os.makedirs(OUTPUT_LOCAL_FOLDER_PATH)
            fillpdfs.write_fillable_pdf(
                agent_info_template_path, 
                f'{OUTPUT_LOCAL_FOLDER_PATH}/Agent_information.pdf', 
                final_dict
            )

            # Generate Direct Deposit PDF
            direct_deposit_pdf_fields = {
                'PayeeName': f"{web_form_fields['first_name']} {web_form_fields['middle_name']} {web_form_fields['last_name']}",
                'PayeeAddress': f"{web_form_fields['street_address']} , {web_form_fields['city']}",
                'PayeeState':f"{web_form_fields['state']}",
                'PayeeZipcode':f"{web_form_fields['zip_code']}",
                'PayeeFaxNumber': "NA",
                'PayeeHomeNumber': web_form_fields.get('home_phone'),
                'PayeeWorkNumber': "NA",
                'PayeeSSN': web_form_fields.get('ssn_or_gov_id'),
                'PayeeIdentificationNumber': "NA",
                'BankName': web_form_fields.get('bank_name', ''),
                'BankAddress': web_form_fields.get('bank_address', ''),
                'BankCity': web_form_fields.get('bank_city', ''),
                'BankState': web_form_fields.get('bank_state', ''),
                'BankZipcode': web_form_fields.get('bank_zipcode', ''),
                'BankPhoneNumber': web_form_fields.get('bank_phone_number', ''),
                'FaxNumber': web_form_fields.get('fax_number', ''),
                'BankRouteNumber': web_form_fields.get('bank_route_number', ''),
                'AccountNumber': web_form_fields.get('account_number', ''),
                'TypeOfAccount': web_form_fields.get('type_of_account', ''),
                'TransactionDate': web_form_fields['date'].strftime('%Y-%m-%d'),
                'PayeePhoneNumber': f"{web_form_fields['home_phone']}",
            }

            direct_deposit_pdf_fields_keys = list(direct_deposit_pdf_fields.keys())
            keys_pdf = list(fillpdfs.get_form_fields( direct_deposit_template_path).keys())
            final_dict = {keys_pdf[i]:direct_deposit_pdf_fields[direct_deposit_pdf_fields_keys[i]] for i in range(len(keys_pdf))}
            fillpdfs.write_fillable_pdf(
                direct_deposit_template_path, 
                f'{OUTPUT_LOCAL_FOLDER_PATH}/direct_deposit.pdf', 
                final_dict
            )
            db.add_record(web_form_fields['first_name'], web_form_fields['email'], web_form_fields['home_phone'], web_form_fields['street_address'], web_form_fields['ssn_or_gov_id'], OUTPUT_LOCAL_FOLDER_PATH)
            email_sender.connect()
            recipient = 'kismatkhatri91@gmail.com'
            email_sender.send_email(recipient, f'Form Submitted by {web_form_fields["first_name"]}', """For was submitted you can check at http://127.0.0.1:8000/log_in/""")
            email_sender.close_connection()

            return redirect('success')
    else:
        form = CombinedForm()
    
    return render(request, 'pdfapp/combined_form.html', {'form': form})

def contractor_agreement_form(request):
    global OUTPUT_LOCAL_FOLDER_PATH, session_id
    session_id = request.GET.get('session_id')
    print('aaa')
    print(session_id)
    print(request.GET.dict())
    OUTPUT_LOCAL_FOLDER_PATH = 'output_files/{session_id}'.format(session_id=session_id)
    print(OUTPUT_LOCAL_FOLDER_PATH)
    if not session_id:
        return redirect('log_in')
    if request.method == 'POST':
        form = ContractorAgreementForm(request.POST)
        web_form_fields = dict(form.data)
        web_form_fields.pop('csrfmiddlewaretoken')
        web_form_fields_keys = list(web_form_fields.keys())

        # Attempt to fill PDF using web form data
        if form.is_valid():
            print(OUTPUT_LOCAL_FOLDER_PATH)

            form_fields = list(fillpdfs.get_form_fields('automatePDF/Independent_contractor_agreement.pdf').keys())
            final_dict = {form_fields[i]: web_form_fields[web_form_fields_keys[i]][0] for i in range(len(form_fields))}
            print(final_dict)
            if not os.path.exists(OUTPUT_LOCAL_FOLDER_PATH):
                os.makedirs(OUTPUT_LOCAL_FOLDER_PATH)
            fillpdfs.write_fillable_pdf('automatePDF/Independent_contractor_agreement.pdf', f'{OUTPUT_LOCAL_FOLDER_PATH}/contractor_agreement.pdf', final_dict)
            return redirect('/commission_agreement_form/?session_id={session_id}'.format(session_id=session_id))

    else:
        form = ContractorAgreementForm()

    return render(request, 'pdfapp/contractor_agreement_form.html', {'form': form, 'session_id': session_id})

def commission_agreement_form(request):
    global OUTPUT_LOCAL_FOLDER_PATH, session_id
    session_id = request.GET.get('session_id')
    OUTPUT_LOCAL_FOLDER_PATH = 'output_files/{session_id}'.format(session_id=session_id)
    print('aaa')
    print(session_id)
    if not session_id:
        return redirect('log_in')
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
            return redirect('success')

    else:
        form = CommissionAgreementForm()

    return render(request, 'pdfapp/commission_agreement_form.html', {'form': form, 'session_id': session_id})

def download_file(request):
    # Path to your file
    file_path = request.GET.get('file_path')
    file_name = request.GET.get('file_name')

    # Check if the path exists
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            # Create a zip file in memory
            mem_zip = io.BytesIO()
            with ZipFile(mem_zip, 'w') as zipf:
                # Walk through the directory and add files to the zip
                for root, dirs, files in os.walk(file_path):
                    for file in files:
                        zipf.write(os.path.join(root, file), arcname=file)
            # Set pointer to the beginning of the stream
            mem_zip.seek(0)
            # Set the response with the in-memory zip file
            response = FileResponse(mem_zip, as_attachment=True, content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{file_name}.zip"'
            return response
        else:
            # Single file download
            # Infer the content type from the file extension or use a default
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{file_name}.pdf"'
            return response
    else:
        # If the file or directory is not found
        return HttpResponseNotFound('The requested file or directory was not found on our server.')


def records_form(request):
    is_log_in = request.COOKIES.get('isLogIn', 'No Cookie Found')
    if is_log_in!='True':
        return redirect('log_in')   
    db = DatabaseManager("/root/project/real_estate_onboarding.db")

    df = db.fetch_all_records()

    def make_download_button(file_path, file_name):
        # Ensure the file path is URL-encoded to handle special characters
        safe_path = quote(file_path)
        return f'<a href="/download_file/?file_path={safe_path}&file_name={file_name}" class="btn btn-primary">Download</a>'
    
    def make_next_form_button(file_path):
        # Ensure the file path is URL-encoded to handle special characters
        safe_path = quote(file_path.replace('output_files/', ''))
        return f'<a href="/contractor_agreement_form/?session_id={safe_path}" class="btn btn-primary">Next Forms</a>'
    if not df.empty:
        df['Download'] = df.apply(lambda x: make_download_button(x['file_path'], x['name']), axis=1)
        df['Next'] = df.apply(lambda x: make_next_form_button(x['file_path']), axis=1)
    else:
        df['Download'] = 'No records found'
    df.drop('file_path', axis=1, inplace=True)
    # Convert DataFrame to HTML
    html_table = df.to_html(index=False, escape=False)
    # Convert DataFrame to HTML, without index and escaping text
    html_table = df.to_html(index=False, escape=False)
    return render(request, 'pdfapp/list_forms.html', {'html_table': html_table})


def log_in(request):
    return render(request, 'pdfapp/log_in_page.html')


def success(request):
    return render(request, 'pdfapp/success.html')
