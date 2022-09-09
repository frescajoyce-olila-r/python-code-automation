import requests
import minbolig_test_data
import sys
import config
import json
import urllib3
from pathlib import Path

# This is to remove InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Register Minbolig
def register():
    path = "/minbolig/register"
    data = minbolig_test_data.registration_test_data
    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
        }
        response = requests.post(config.host + path,
                             data=json.dumps(data), headers=headers, verify=False)

        print(f'Status Code: {response.status_code}')
        # print(json.dumps(response.json(), indent=4, sort_keys=True))
        print(f'Successfully Registered in Minbolig Production')

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)

# Retrieve Unique ID
def retrieve_unique_id(user_id):
    path = "/database/tableByColumn"
    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
        }
        response = requests.get(config.host + path,
                                 params={
                                    'table': 'c_minbolig_email_verification',
                                    'column': 'USER_ID',
                                    'value': user_id
                                 }, headers=headers, verify=False)

        print(f'Status Code: {response.status_code}')
        # print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)

# Verify Email
def verify(unique_id):
    path = "/minbolig/verifyEmail/"
    try:
        url = f'{config.host}{path}{unique_id}'
        print(f'URL: {url}')
        response = requests.get(url, verify=False)

        print(f'Status Code: {response.status_code}')

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)

#Login Account
def login_through_register():
    path= "/minbolig/login/"


    # Send the POST request
    # Return the result of the POST request
    try:
        email = minbolig_test_data.registration_test_data['email']
        password = minbolig_test_data.registration_test_data['password']
        response = requests.post(config.host + path,
                               data={'email': email, 'password': password},
                               verify=False)
        print(f'Status Code: {response.status_code}')
        # print(json.dumps(response.json(), indent=4, sort_keys=True))

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)


def login():
    path= "/minbolig/login/"

    # Send the POST request
    # Return the result of the POST request
    try:
        email = minbolig_test_data.login_test_data['email']
        password = minbolig_test_data.login_test_data['password']
        response = requests.post(config.host + path,
                                 data={'email': email, 'password': password},
                                 verify=False)

        print(f'LOGIN IN MINBOLIG')
        print(f'--------------------------------------------------')
        print(f'Status Code: {response.status_code}')
        print(f'Log in Successful')
        print(f'Username: {email}')
        print(f'Password: {password}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)

def send_messages(token):
    path='/minbolig/message'

    # Send the POST request
    # Return the result of the POST request
    try:

        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + token
        }
        partnerId = minbolig_test_data.send_message_test_data['partnerId']
        title = minbolig_test_data.send_message_test_data['title']
        message = minbolig_test_data.send_message_test_data['message']
        response = requests.post(config.host + path,
                                 params={
                                     'partnerId': partnerId,
                                     'title': title,
                                     'message': message
                                 },
                                 headers=headers, verify=False)

        print(f'--------------------------------------------------')
        print(f'SEND MESSAGE IN MINBOLIG')
        print(f'--------------------------------------------------')
        print(f'Status Code: {response.status_code}')
        print(f'Successfully send Message')
        print(f'partnerId: {partnerId}')
        print(f'Title: {title}')
        print(f'Message: {message}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)

# Create Meeting
def create_meeting(token):
    path= '/minbolig/calendar/'

    # Send the POST request
    # Return the result of the POST request
    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + token
        }
        for dic in minbolig_test_data.create_calendar_test_data:
            title = dic['title']
            description = dic['description']
            date = dic['date']
            startTime = dic['startTime']
            endTime = dic['endTime']
            type = dic['type']
            partnerId = dic['partnerId']

            response = requests.post(config.host + path,
                                params={
                                     'title' : title,
                                     'description': description,
                                     'date': date,
                                     'startTime': startTime,
                                     'endTime': endTime,
                                     'type': type,
                                     'partnerId': partnerId

                                 },
                                 headers=headers, verify=False)

            print(f'--------------------------------------------------')
            print(f'CREATE CALENDAR')
            print(f'--------------------------------------------------')
            print(f'Status Code: {response.status_code}')
            print(f'Title: {title}')
            print(f'Description: {description}')
            print(f'Date: {date}')
            print(f'Start Time: {startTime}')
            print(f'End Time: {endTime}')
            print(f'Type: {type}')
            print(f'Partner Id : {partnerId}')
            print(json.dumps(response.json(), indent=4, sort_keys=True))


    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)

def create_folder(token):
    path = "/minbolig/folder"
    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + token
        }
        folderName = minbolig_test_data.create_folder_test_data['folderName']
        parentId = minbolig_test_data.create_folder_test_data['parentId']

        response = requests.post(config.host + path,
                                 params={
                                     'folderName' : folderName,
                                     'parentId': parentId,
                                 },
                                 headers=headers, verify=False)

        print(f'--------------------------------------------------')
        print(f'CREATE FOLDER')
        print(f'--------------------------------------------------')
        print(f'Status Code: {response.status_code}')
        print(f'Folder Name: {folderName}')
        print(f'Parent ID: {parentId}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)


def rename_folder(token,folder_id):
    path = "/minbolig/folder"

    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + token
        }
        newName = minbolig_test_data.rename_folder_test_data['newName']

        response = requests.put(f'{config.host + path}/{folder_id}',
                                params={'newName': newName},
                                headers=headers, verify=False)

        print(f'--------------------------------------------------')
        print(f'RENAME  FOLDER')
        print(f'--------------------------------------------------')
        print(f'Status Code: {response.status_code}')
        print(f'Folder ID: {folder_id}')
        print(f'Folder Name: {newName}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)


def create_project(token):
    path = "/minbolig/projects"

    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + token
        }
        industryIds = minbolig_test_data.create_project_test_data['industryIds']
        addressId = minbolig_test_data.create_project_test_data['addressId']
        name = minbolig_test_data.create_project_test_data['name']
        description = minbolig_test_data.create_project_test_data['description']
        contractType = minbolig_test_data.create_project_test_data['contractType']
        subcategory =minbolig_test_data.create_project_test_data['subcategory']
        taskType= minbolig_test_data.create_project_test_data['taskType']
        tags = minbolig_test_data.create_project_test_data['tags']


        response = requests.post(config.host + path,
                            params={
                                'industryIds': industryIds,
                                'addressId' : addressId,
                                'name' : name,
                                'description' : description,
                                'contractType' : contractType,
                                'subcategory' : subcategory,
                                'taskType' : taskType,
                                'tags': tags
                            },
                            headers=headers, verify=False)

        print(f'--------------------------------------------------')
        print(f'CREATE PROJECT')
        print(f'--------------------------------------------------')
        print(f'Status Code: {response.status_code}')
        print('Successfully Created Project')
        print(f'Project Name: {name}')
        print(f'Description: {description}')
        print(f'Industry ID: {industryIds}')
        print(f'Address ID: {addressId}')
        print(f'Contract Type: {contractType}')
        print(f'Subcategory: {subcategory}')
        print(f'Task Type: {taskType}')
        print(f'Tags: {tags}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)

def create_initial_budget(token, project_id):
    path="/minbolig/project/"

    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + token
        }
        amount = minbolig_test_data.create_initial_budget_test_data['amount']

        response = requests.post(f'{config.host + path}{project_id}/initialBudget',
                                 params={
                                     'amount': amount
                                 },
                                 headers=headers, verify=False)

        print(f'--------------------------------------------------')
        print(f'CREATE INITIAL BUDGET')
        print(f'--------------------------------------------------')
        print(f'Status Code: {response.status_code}')
        print(f'Successfully created Initial Budget')
        print(f'Project ID: {project_id}')
        print(f'Amount: {amount}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)

def add_budget(token,project_id):
    path = "/minbolig/project/"

    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + token
        }
        title = minbolig_test_data.add_budget_test_data['title']
        category = minbolig_test_data.add_budget_test_data['category']
        amount = minbolig_test_data.add_budget_test_data['amount']
        isLocked = minbolig_test_data.add_budget_test_data['isLocked']

        response = requests.post(f'{config.host + path}{project_id}/budget',
                                 params={
                                 "title": title,
                                 "category": category,
                                 "amount": amount,
                                 "isLocked": isLocked
                                 },
                                 headers=headers, verify=False)
        print(f'--------------------------------------------------')
        print(f'ADD BUDGET')
        print(f'--------------------------------------------------')
        print(f'Status Code: {response.status_code}')
        print(f'Successfully Added Budget')
        print(f'Title: {title}')
        print(f'Category: {category}')
        print(f'Amount: {amount}')
        print(f'Locked: {isLocked}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)

def prisberegnere_calculator(token):
    path = "/bitrix/getCalculationPrice"

    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + token
        }
        industry = minbolig_test_data.prisberegnere_calculator_test_data['industry']
        zipcode = minbolig_test_data.prisberegnere_calculator_test_data['zipcode']
        husnr = minbolig_test_data.prisberegnere_calculator_test_data['husnr']
        addressid = minbolig_test_data.prisberegnere_calculator_test_data['addressid']
        kommunekode = minbolig_test_data.prisberegnere_calculator_test_data['kommunekode']
        vejkode = minbolig_test_data.prisberegnere_calculator_test_data['vejkode']
        vejnavn = minbolig_test_data.prisberegnere_calculator_test_data['vejnavn']

        response = requests.get(config.host + path,
                                 params={
                                     "industry": industry,
                                     "zipcode": zipcode,
                                     "husnr": husnr,
                                     "addressid": addressid,
                                     "kommunekode": kommunekode,
                                     "vejkode": vejkode,
                                     "vejnavn": vejnavn
                                 },
                                 headers=headers, verify=False)
        print(f'--------------------------------------------------')
        print(f'PRIS BEREGNERE CALCULATOR')
        print(f'--------------------------------------------------')
        print(f'Status Code: {response.status_code}')
        print(f'Industry: {industry}')
        print(f'Zipcode: {zipcode}')
        print(f'Husnr: {husnr}')
        print(f'Address ID: {addressid}')
        print(f'kommunekode: {kommunekode}')
        print(f'vejkode: {vejkode}')
        print(f'vejnavn: {vejnavn}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)

# Favorite (url)
def Favorite(token):
    path = "/minbolig/favorite/"

    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + token
        }
        for dic in minbolig_test_data.favorites:
            title = dic['title']
            url = dic['url']
            type = dic['type']
            objectId = dic['objectId']
            picType = dic['picType']
            picUrl = dic['picUrl']

            response = requests.post(config.host + path,
                             params={
                                 'title': title,
                                 'url': url,
                                 'type': type,
                                 'objectId': objectId,
                                 'picType': picType,
                                 'picUrl': picUrl
                             },
                             headers=headers, verify=False)
            print(f'--------------------------------------------------')
            print(f'FAVORITE')
            print(f'--------------------------------------------------')
            print(f'Status Code: {response.status_code}')
            print(f'Successfully Added Favorite')
            print(f'title: {title}')
            print(f'url: {url}')
            print(f'type: {type}')
            print(f'objectId: {objectId}')
            print(f'picType: {picType}')
            print(json.dumps(response.json(), indent=4, sort_keys=True))
# print(json.dumps(response.json(), indent=4, sort_keys=True))

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)

# Upload Billeder
def upload_billeder(token, folder_id1):
    path = "/minbolig/files?"

    try:
        headers = {
            'Authorization': 'Bearer' + token
        }
        images_folder = Path.cwd() / 'Images'
        file0 = images_folder / 'Image1.jpg'
        file1 = images_folder / 'Image2.jpg'

        response = requests.post(f'{config.host + path}',
                                 params={
                                     'parentId': folder_id1
                                 },
                                 files={
                                     'files[0]': file0.open(mode='rb'),
                                     'files[1]': file1.open(mode='rb')
                                 },
                                 headers=headers, verify=False)
        print(f'--------------------------------------------------')
        print(f'UPLOAD BILLEDER')
        print(f'--------------------------------------------------')
        print(f'Successfully Uploaded Image/File')
        print(f'Status Code: {response.status_code}')
        print(f'parentId: {folder_id1}')
        print(f'File 1: {file1}')
        print(f'File 0: {file0}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)

# To do Upload Billeder
def todo_upload_billeder(token, project_id):
    path = "/minbolig/project"

    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'multipart/form-data',
            'Authorization': 'Bearer' + token
        }
        code = minbolig_test_data.todo_upload_billeder['code']
        done = minbolig_test_data.todo_upload_billeder['done']
        skipped = minbolig_test_data.todo_upload_billeder['skipped']

        response = requests.post(f'{config.host + path}/{project_id}/todo',
                                 params={
                                      'code' : code,
                                      'done' : done,
                                      'skipped' : skipped
                                },
                                 headers=headers, verify=False)
        print(f'--------------------------------------------------')
        print(f'TO DO UPLOAD BILLEDER verification')
        print(f'--------------------------------------------------')
        print(f'Successfully Uploaded File')
        print(f'Status Code: {response.status_code}')
        print(f'Status Done: {done}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)

# Contract Type
def minetilbud_contractType(token, project_id):
    path = '/minbolig/project/'

    try:
        headers = {
            # 'accept': '*/*',
            # 'Content-Type': 'multipart/form-data',
            'Authorization': 'Bearer' + token
        }
        isFinal = minbolig_test_data.minetilbud_contractType['isFinal']
        contractType = minbolig_test_data.minetilbud_contractType['contractType']

        response = requests.put(f'{config.host + path}{project_id}',
                                params={
                                     'isFinal' : isFinal,
                                     'contractType' : contractType
                                },
                                 headers=headers, verify=False)
        print(f'--------------------------------------------------')
        print(f'CONTRACT TYPE')
        print(f'--------------------------------------------------')
        print(f'Successfully Added Contract Type')
        print(f'Status Code: {response.status_code}')
        print(f'isFinal: {isFinal}')
        print(f'contractType: {contractType}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)

# Create Offer
def henttilbud_anbefalet(token,project_id):
    path = '/minbolig/project/'

    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + token
        }
        name = minbolig_test_data.hentilbud_anbefalet['name']
        description = minbolig_test_data.hentilbud_anbefalet['description']
        contractType = minbolig_test_data.hentilbud_anbefalet['contractType']
        subcategory = minbolig_test_data.hentilbud_anbefalet['subcategory']
        taskType = minbolig_test_data.hentilbud_anbefalet['taskType']

        response = requests.put(f'{config.host + path}{project_id}',
                                params={
                                     'name' : name,
                                     'description' : description,
                                     'contractType': contractType,
                                     'subcategory': subcategory,
                                     'taskType': taskType
                                },
                                 headers=headers, verify=False)
        print(f'--------------------------------------------------')
        print(f'SEND OFFER')
        print(f'--------------------------------------------------')
        print(f'Successfully Send Offer')
        print(f'Status Code: {response.status_code}')
        print(f'name: {name}')
        print(f'description: {description}')
        print(f'contractType: {contractType}')
        print(f'subcategory: {subcategory}')
        print(f'taskType: {taskType}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)



# Send Offer Invitation to Partner
def send_offer_invitation_to_partner(token, project_id):
    path = "/minbolig/project"

    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'multipart/form-data',
            'Authorization': 'Bearer' + token
        }
        company_name = minbolig_test_data.offer_send_invitation['companyName']
        contactPerson = minbolig_test_data.offer_send_invitation['contactPerson']
        email = minbolig_test_data.offer_send_invitation['email']
        phone = minbolig_test_data.offer_send_invitation['phone']
        title = minbolig_test_data.offer_send_invitation['title']
        description = minbolig_test_data.offer_send_invitation['description']
        budget = minbolig_test_data.offer_send_invitation['budget']
        selectedImages = minbolig_test_data.offer_send_invitation['selectedImages']

        response = requests.post(f'{config.host + path}/{project_id}/partnerInvitation',
                                 params={
                                      'companyName' : company_name,
                                      'contactPerson' : contactPerson,
                                      'email' : email,
                                      'phone': phone,
                                      'title': title,
                                      'description': description,
                                      'budget': budget,
                                      'selectedImages': selectedImages,
                                 },
                                 headers=headers, verify=False)
        print(f'--------------------------------------------------')
        print(f'SEND OFFER INVITATION TO PARTNER')
        print(f'--------------------------------------------------')
        print(f'Status Code: {response.status_code}')
        print(f'Company Name: {company_name}')
        print(f'Contact Person: {contactPerson}')
        print(f'Email: {email}')
        print(f'Phone: {phone}')
        print(f'Title: {title}')
        print(f'Budget: {budget}')
        print(f'Selected Images: {selectedImages}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)

# Get Offer Id in Minbolig
def get_offer_id_minbolig(token, project_id):
    path = "/minbolig/project"

    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'multipart/form-data',
            'Authorization': 'Bearer' + token
        }


        response = requests.get(f'{config.host + path}/{project_id}/offers',
                                   headers=headers, verify=False)
        print(f'--------------------------------------------------')
        print(f'GET OFFER ID IN MINBOLIG')
        print(f'--------------------------------------------------')
        print(f'Status Code: {response.status_code}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)


# Accept Offer Minbolig Side
def accept_offer_minbolig(token, project_id, offer_id):
    path = "/minbolig/project"

    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'multipart/form-data',
            'Authorization': 'Bearer' + token
        }

        response = requests.post(f'{config.host + path}/{project_id}/offer/{offer_id}',
                                headers=headers, verify=False)
        print(f'--------------------------------------------------')
        print(f'ACCEPT OFFER IN MINBOLIG')
        print(f'--------------------------------------------------')
        print(f'Status Code: {response.status_code}')
        print(f'Project Id:{project_id}')
        print(f'Offer Id: {offer_id}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)

# Create Contract in minbolig
def create_contract_minbolig(token, project_id):
    path = "/minbolig/contract"

    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + token
        }
        template_id = minbolig_test_data.create_contract_test_data['templateId']
        contract_templateId = minbolig_test_data.create_contract_test_data['contractTemplateId']
        company_id = minbolig_test_data.create_contract_test_data['companyId']
        steps = minbolig_test_data.create_contract_test_data['steps']
        comments = minbolig_test_data.create_contract_test_data['comments']
        title = minbolig_test_data.create_contract_test_data['title']
        name = minbolig_test_data.create_contract_test_data['name']
        lastname = minbolig_test_data.create_contract_test_data['lastname']
        address = minbolig_test_data.create_contract_test_data['address']
        zipcode = minbolig_test_data.create_contract_test_data['zipcode']
        email = minbolig_test_data.create_contract_test_data['email']
        mobile = minbolig_test_data.create_contract_test_data['mobile']
        city = minbolig_test_data.create_contract_test_data['city']
        payment_stages = minbolig_test_data.payment_stages_test_data['paymentStages']


        response = requests.post(f'{config.host + path}',
                                 params={
                                     'projectId': project_id,
                                     'templateId': template_id,
                                     'contractTemplateId': contract_templateId,
                                     'companyId': company_id,
                                     'steps': steps,
                                     'comments': comments,
                                     'title': title,
                                     'name': name ,
                                     'lastname': lastname,
                                     'address': address,
                                     'zipcode': zipcode,
                                     'email': email,
                                     'mobile': mobile,
                                     'city': city
                                 },
                                 json={
                                     "paymentStages": payment_stages,

                                 },
                                headers=headers, verify=False)
        print(f'--------------------------------------------------')
        print(f'CREATE CONTRACT IN MINBOLIG')
        print(f'--------------------------------------------------')
        print(f'Status Code: {response.status_code}')
        print(f'Project Id: {project_id}')
        print(f'Template Id: {template_id}')
        print(f'Contract Template Id: {contract_templateId}')
        print(f'Company Id: {company_id}')
        print(f'Steps: {steps}')
        print(f'Comments: {comments}')
        print(f'Title: {title}')
        print(f'Name: {name}')
        print(f'Lastname: {lastname}')
        print(f'Address: {address}')
        print(f'Zipcode: {zipcode}')
        print(f'Email: {email}')
        print(f'Mobile: {mobile}')
        print(f'City: {city}')
        print(f'Payment Stages: {payment_stages}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)


