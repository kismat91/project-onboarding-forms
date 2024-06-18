from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import ContractorAgreementForm, CommissionAgreementForm, CombinedForm
from fillpdf import fillpdfs
import os
from django.http import HttpResponseNotFound, FileResponse, HttpResponse
from urllib.parse import quote
from sqllite_test.sqlite_conn import DatabaseManager
from sqllite_test.email import EmailSender
import uuid
from zipfile import ZipFile, ZIP_DEFLATED
import mimetypes
import io
import re
from datetime import date
from django.utils.timezone import now

# Set up a global session ID and output folder path
session_id = uuid.uuid4()
output_base_folder_path = '/root/project/output_files/'
db_path = '/root/project/real_estate_onboarding.db'
OUTPUT_LOCAL_FOLDER_PATH = f'{output_base_folder_path}{session_id}'
print(f'Output Local Folder Path: {OUTPUT_LOCAL_FOLDER_PATH}')
def process_pdf(pdf_template_path, output_path, data_dict):
    fillpdfs.write_fillable_pdf(pdf_template_path, output_path, data_dict)

def sanitize_session_id(session_id):
    return session_id
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', session_id)

def get_value(user_details, key, default=''):
    value = user_details.get(key, [default])
    if isinstance(value, list):
        value = value[0]
    if isinstance(value, date):
        return value.strftime('%Y-%m-%d')
    return value

def user_details(request):
    print(session_id)
    db = DatabaseManager(db_path)
    email_sender = EmailSender()
    if request.method == 'POST':
        form = CombinedForm(request.POST)
        if form.is_valid():
            web_form_fields = dict(form.cleaned_data)
            agent_info_template_path = 'automatePDF/Agent_information_sheet.pdf'
            agent_info_output_path = 'Agent_information_filled.pdf'
            direct_deposit_template_path = 'automatePDF/Direct_Deposit_Form.pdf'
            direct_deposit_output_path = 'Direct_Deposit_filled.pdf'

            user_details_pdf_fields = {
                'FirstName': web_form_fields['first_name'],
                'MiddleInitial': web_form_fields['middle_name'][:1] if web_form_fields['middle_name'] else 'N/A',
                'LastName': web_form_fields['last_name'],
                'Address': f"{web_form_fields['street_address']}",
                'apartment_num': f"{web_form_fields.get('apartment_number', '')}",
                'City': web_form_fields['city'],
                'State': web_form_fields['state'],
                'ZipCode': web_form_fields['zip_code'],
                'HomePhone': web_form_fields['home_phone'],
                'AlternatePhone': web_form_fields.get('alternate_phone', ''),
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
            final_dict = {keys_pdf[i]: user_details_pdf_fields.get(user_details_pdf_fields_keys[i], '') for i in range(len(keys_pdf))}

            if not os.path.exists(OUTPUT_LOCAL_FOLDER_PATH):
                os.makedirs(OUTPUT_LOCAL_FOLDER_PATH)
            print(f'Output Local Folder Path: {OUTPUT_LOCAL_FOLDER_PATH}')
            fillpdfs.write_fillable_pdf(agent_info_template_path, f'{OUTPUT_LOCAL_FOLDER_PATH}/Agent_information.pdf', final_dict)

            direct_deposit_pdf_fields = {
                'PayeeName': f"{web_form_fields['first_name']} {web_form_fields['middle_name']} {web_form_fields['last_name']}",
                'PayeeAddress': f"{web_form_fields['street_address']} , {web_form_fields['city']}",
                'PayeeState': f"{web_form_fields['state']}",
                'PayeeZipcode': f"{web_form_fields['zip_code']}",
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
            keys_pdf = list(fillpdfs.get_form_fields(direct_deposit_template_path).keys())
            final_dict = {keys_pdf[i]: direct_deposit_pdf_fields.get(direct_deposit_pdf_fields_keys[i], '') for i in range(len(keys_pdf))}

            fillpdfs.write_fillable_pdf(direct_deposit_template_path, f'{OUTPUT_LOCAL_FOLDER_PATH}/direct_deposit.pdf', final_dict)

            db.add_record(web_form_fields['first_name'], web_form_fields['last_name'], web_form_fields['middle_name'], web_form_fields['email'], web_form_fields['home_phone'], web_form_fields['alternate_phone'], web_form_fields['street_address'], web_form_fields['apartment_number'], web_form_fields['city'], web_form_fields['state'], web_form_fields['zip_code'], web_form_fields['birth_date'].strftime('%Y-%m-%d'), web_form_fields['ssn_or_gov_id'], OUTPUT_LOCAL_FOLDER_PATH)

            email_sender.connect()
            recipient = 'info@onest.realestate'
            email_sender.send_email(recipient, f'Form Submitted by {web_form_fields["first_name"]}', f"""Form was submitted. You can check at {request.build_absolute_uri('/log_in/')}""")
            email_sender.close_connection()

            return redirect('success')
    else:
        form = CombinedForm()

    return render(request, 'pdfapp/combined_form.html', {'form': form})

def contractor_agreement_form(request):
    db = DatabaseManager(db_path)
    global OUTPUT_LOCAL_FOLDER_PATH, session_id
    session_id = request.GET.get('session_id')
    print(f'Session ID: {session_id}')

    if session_id:
        session_id = sanitize_session_id(session_id)
    else:
        return redirect('log_in')

    OUTPUT_LOCAL_FOLDER_PATH = f'{output_base_folder_path}{session_id}'
    print(f'Output Local Folder Path: {OUTPUT_LOCAL_FOLDER_PATH}')

    try:
        print(OUTPUT_LOCAL_FOLDER_PATH)
        user_details = db.fetch_record(OUTPUT_LOCAL_FOLDER_PATH).to_dict()
    except Exception as e:
        print(f'Error fetching record: {e}')
        user_details = {}

    print(f'User Details: {user_details}')

    if request.method == 'POST':
        form = ContractorAgreementForm(request.POST)
        print(f'Form Data: {form.data}')

        if form.is_valid():
            print('Form is valid')
            web_form_fields = dict(form.cleaned_data)
            print(f'Cleaned Form Data: {web_form_fields}')

            # No need to adjust bCommission and cCommission here since they're already set in the form

            web_form_fields_items = list(web_form_fields.items())

            f_name = get_value(user_details, 'f_name')[0]
            m_name = get_value(user_details, 'm_name')[0]
            l_name = get_value(user_details, 'l_name')[0]
            s_address = get_value(user_details, 's_address')[0]
            ssn = get_value(user_details, 'ssn')[0]
            if m_name:
                web_form_fields_items.insert(4, ('employeeName', f"{f_name} {m_name} {l_name}".strip()))
            else:
                web_form_fields_items.insert(4, ('employeeName', f"{f_name} {l_name}".strip()))

            web_form_fields_items.insert(6, ('ssn', ssn))
            web_form_fields_items.insert(7, ('contractorLocation', s_address))
            web_form_fields_items.insert(20, ('cAddress', s_address))

            if m_name:
                web_form_fields_items.insert(28, ('cName', f"{f_name} {m_name} {l_name}".strip()))
            else:
                web_form_fields_items.insert(28, ('cName', f"{f_name} {l_name}".strip()))

            web_form_fields = dict(web_form_fields_items)
            web_form_fields_keys = list(web_form_fields.keys())

            form_fields = list(fillpdfs.get_form_fields('automatePDF/Independent_contractor_agreement.pdf').keys())

            final_dict = {}
            for i in range(len(form_fields)):
                final_dict[form_fields[i]] = web_form_fields.get(web_form_fields_keys[i], '')

            if not os.path.exists(OUTPUT_LOCAL_FOLDER_PATH):
                os.makedirs(OUTPUT_LOCAL_FOLDER_PATH)

            fillpdfs.write_fillable_pdf('automatePDF/Independent_contractor_agreement.pdf', f'{OUTPUT_LOCAL_FOLDER_PATH}/contractor_agreement.pdf', final_dict)
            return redirect(f'/commission_agreement_form/?session_id={session_id}&contractor_agreement_path={OUTPUT_LOCAL_FOLDER_PATH}/contractor_agreement.pdf')
        else:
            print('Form is invalid')
            print(form.errors)
    else:
        form = ContractorAgreementForm(initial={
            'brokerName': 'Anjana Budhathoki',
            'bName': 'Anjana Budhathoki',
            'bTitle': 'Principal Broker',
            'forumLocation': 'Fairfax, Virginia',
            'bAddress': '8280 Willow Oaks Corp Dr. Suite 600 Fairfax, VA 22031',
            'bAttention': 'Anjana Budhathoki',
            'bFacsimileNo': 'NA',
            'agreementDuration': '1 year',
            'terminationDays': '30 days',
            'commissionTimePeriod': '5 days',
            'bCommission': '20%',
            'cCommission': '80%',
            'agreementEffectiveDate': now().date(),
        })

    return render(request, 'pdfapp/contractor_agreement_form.html', {'form': form, 'session_id': session_id})


def commission_agreement_form(request):
    global OUTPUT_LOCAL_FOLDER_PATH, session_id
    session_id = request.GET.get('session_id')
    contractor_agreement_path = request.GET.get('contractor_agreement_path')

    if session_id:
        session_id = sanitize_session_id(session_id)
    else:
        return redirect('log_in')

    OUTPUT_LOCAL_FOLDER_PATH = f'{output_base_folder_path}{session_id}'

    db = DatabaseManager(db_path)

    try:
        user_details = db.fetch_record(OUTPUT_LOCAL_FOLDER_PATH).to_dict()
    except Exception as e:
        print(f'Error fetching record: {e}')
        user_details = {}

    if request.method == 'POST':
        form = CommissionAgreementForm(request.POST)
        # print(f'Form Data: {form.data}')

        if form.is_valid():
            print('Form is valid')
            web_form_fields = dict(form.cleaned_data)
            # print(f'Cleaned Form Data: {web_form_fields}')

            web_form_fields_items = list(web_form_fields.items())

            f_name = get_value(user_details, 'f_name')[0]
            m_name = get_value(user_details, 'm_name')[0]
            l_name = get_value(user_details, 'l_name')[0]
            s_address = get_value(user_details, 's_address')[0]
            ssn = get_value(user_details, 'ssn')[0]

            if m_name:
                web_form_fields_items.insert(0, ('agentName', f"{f_name} {m_name} {l_name}".strip()))
                web_form_fields_items.insert(26, ('printedNameOfAgent', f"{f_name} {m_name} {l_name}".strip()))
                web_form_fields_items.append(('nameOfAgent', f"{f_name} {m_name} {l_name}".strip()))
            else:
                web_form_fields_items.insert(0, ('agentName', f"{f_name} {l_name}".strip()))
                web_form_fields_items.insert(26, ('printedNameOfAgent', f"{f_name} {l_name}".strip()))
                web_form_fields_items.append(('nameOfAgent', f"{f_name} {l_name}".strip()))

            web_form_fields_items.insert(27, ('agentAddress', s_address))
            web_form_fields = dict(web_form_fields_items)
            web_form_fields_keys = list(web_form_fields.keys())
            # print(f'Web Form Fields: {web_form_fields}')
            web_form_fields_items = list(web_form_fields.items())

            try:
                web_form_fields_items.insert(web_form_fields_keys.index('exclusive') + 1, ('nonExclusive', None))
                web_form_fields = dict(web_form_fields_items)
                web_form_fields['exclusive'] = None
                web_form_fields['exclusive'] = 'Yes_pgge'
                web_form_fields_keys = list(web_form_fields.keys())
                web_form_fields_items = list(web_form_fields.items())
            except ValueError:
                web_form_fields_items.insert(1, ('exclusive', None))
                web_form_fields_items.insert(2, ('nonExclusive', 'Yes_rjaw'))
                web_form_fields = dict(web_form_fields_items)
                web_form_fields_keys = list(web_form_fields.keys())

            try:
                web_form_fields_items.insert(web_form_fields_keys.index('notApplicableExpenses') + 1, ('applicableExpenses', None))
                web_form_fields = dict(web_form_fields_items)
                web_form_fields['notApplicableExpenses'] = 'Yes_xavj'
                web_form_fields_keys = list(web_form_fields.keys())
                web_form_fields_items = list(web_form_fields.items())
            except ValueError:
                web_form_fields_items.insert(16, ('notApplicableExpenses', None))
                web_form_fields_items.insert(17, ('applicableExpenses', 'Yes_vkfk'))
                web_form_fields = dict(web_form_fields_items)
                web_form_fields_keys = list(web_form_fields.keys())

            try:
                web_form_fields_items.insert(web_form_fields_keys.index('notApplicable') + 1, ('applicable', None))
                web_form_fields = dict(web_form_fields_items)
                web_form_fields['notApplicable'] = 'Yes_aecf'
                web_form_fields_keys = list(web_form_fields.keys())
                web_form_fields_items = list(web_form_fields.items())
            except ValueError:
                web_form_fields_items.insert(23, ('notApplicable', None))
                web_form_fields_items.insert(24, ('applicable', 'Yes_kzvw'))
                web_form_fields = dict(web_form_fields_items)
                web_form_fields_keys = list(web_form_fields.keys())

            try:
                web_form_fields_items.insert(web_form_fields_keys.index('notapplicableExclussion') + 1, ('applicableExclusion', None))
                web_form_fields = dict(web_form_fields_items)
                web_form_fields['notapplicableExclussion'] = 'Yes_jqla'
                web_form_fields_keys = list(web_form_fields.keys())
                web_form_fields_items = list(web_form_fields.items())
            except ValueError:
                web_form_fields_items.insert(31, ('notapplicableExclussion', None))
                web_form_fields_items.insert(32, ('applicableExclusion', 'Yes_erku'))
                web_form_fields = dict(web_form_fields_items)
                web_form_fields_keys = list(web_form_fields.keys())

            print(f'Web Form Fields after insertion: {web_form_fields}')
            print(len(web_form_fields))
            # Attempt to fill PDF using web form data
            form_fields = list(fillpdfs.get_form_fields('automatePDF/Commission_agreement.pdf').keys())
            final_dict = {}
            print(len(form_fields))
            for i in range(len(form_fields)):
                value = web_form_fields.get(web_form_fields_keys[i], '')
                final_dict[form_fields[i]] = value
                
            print(f'Final Dict: {final_dict}')

            commission_agreement_path = f'{OUTPUT_LOCAL_FOLDER_PATH}/commission_agreement.pdf'
            fillpdfs.write_fillable_pdf('automatePDF/Commission_agreement.pdf', commission_agreement_path, final_dict)
            return redirect(f'/success2/?session_id={session_id}&contractor_agreement_path={contractor_agreement_path}&commission_agreement_path={commission_agreement_path}')
        else:
            print('Form is invalid')
            print(form.errors)
    else:
        form = CommissionAgreementForm()

    return render(request, 'pdfapp/commission_agreement_form.html', {'form': form, 'session_id': session_id})

def download_file(request):
    file_path = request.GET.get('file_path')
    file_name = request.GET.get('file_name')

    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            mem_zip = io.BytesIO()
            with ZipFile(mem_zip, 'w') as zipf:
                for root, dirs, files in os.walk(file_path):
                    for file in files:
                        zipf.write(os.path.join(root, file), arcname=file)
            mem_zip.seek(0)
            response = FileResponse(mem_zip, as_attachment=True, content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{file_name}.zip"'
            return response
        else:
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{file_name}.pdf"'
            return response
    else:
        return HttpResponseNotFound('The requested file or directory was not found on our server.')

def records_form(request):
    if not request.user.is_authenticated:
        return redirect('log_in')

    db = DatabaseManager(db_path)
    df = db.fetch_all_records()

    def make_download_button(file_path, file_name):
        safe_path = quote(file_path)
        return f'<a href="/download_file/?file_path={safe_path}&file_name={file_name}" class="btn btn-primary">Download</a>'

    def make_next_form_button(file_path):
        print(f'File Path: {file_path}')
        safe_path = quote(file_path.replace(output_base_folder_path, ''))
        return f'<a href="/contractor_agreement_form/?session_id={safe_path}" class="btn btn-primary">Next Forms</a>'

    if not df.empty:
        df['Download'] = df.apply(lambda x: make_download_button(x['file_path'], x['First Name']), axis=1)
        df['Next'] = df.apply(lambda x: make_next_form_button(x['file_path']), axis=1)
    else:
        df['Download'] = 'No records found'
        df['Next'] = 'No records found'

    df.drop('file_path', axis=1, inplace=True)
    html_table = df.to_html(index=False, escape=False)

    return render(request, 'pdfapp/list_forms.html', {'html_table': html_table})

def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.data.get('username')
            password = form.data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return HttpResponse("Invalid username or password.")
        else:
            return HttpResponse("Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'pdfapp/log_in_page.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('log_in')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('records_form')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    return render(request, 'pdfapp/home.html')

def success(request):
    return render(request, 'pdfapp/success.html', {'host_link': request.build_absolute_uri('/records_form/')})

def success2(request):
    session_id = request.GET.get('session_id')
    contractor_agreement_path = request.GET.get('contractor_agreement_path')
    commission_agreement_path = request.GET.get('commission_agreement_path')

    sanitized_session_id = sanitize_session_id(session_id)
    output_folder_path = f'{output_base_folder_path}{sanitized_session_id}'

    files = [
        contractor_agreement_path,
        commission_agreement_path
    ]

    if not os.path.exists(output_folder_path):
        return HttpResponseNotFound('The requested files were not found on our server.')

    mem_zip = io.BytesIO()
    with ZipFile(mem_zip, 'w') as zipf:
        for file in files:
            if os.path.exists(file):
                zipf.write(file, os.path.basename(file))

    mem_zip.seek(0)

    response = FileResponse(mem_zip, as_attachment=True, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="filled_forms_{sanitized_session_id}.zip"'

    return response
