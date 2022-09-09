import json
import minbolig_test_data
import config
import sys
import requests


# Login to Partner account
def partner_login():
    path= "/partner/login/"
    # Send the POST request
    # Return the result of the POST request
    try:
        email = minbolig_test_data.partner_login_test_data['email']
        password = minbolig_test_data.partner_login_test_data['password']
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


# Get Invitation ID by Project
def get_invitation_id(token_partner, project_id):
    path = "/partner/project"

    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'multipart/form-data',
            'Authorization': 'Bearer' + token_partner
        }

        response = requests.get(f'{config.host + path}/{project_id}/invitation',
                                    headers=headers, verify=False)
        print(f'--------------------------------------------------')
        print(f'GET INVITATION BY PROJECT')
        print(f'--------------------------------------------------')
        print(f'Status Code: {response.status_code}')
        print(f'Project ID : {project_id}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)


# Partner Accept offer from homeowner
def partner_accept_offer(token_partner, invitation_id):
    path = "/partner/projectInvitation"

    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'multipart/form-data',
            'Authorization': 'Bearer' + token_partner
        }

        response = requests.post(f'{config.host + path}/{invitation_id}?accepted=1',
                                    headers=headers, verify=False)
        print(f'--------------------------------------------------')
        print(f'PARTNER ACCEPT OFFER')
        print(f'--------------------------------------------------')
        print(f'Status Code: {response.status_code}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)



# Partner create an offer to send to homeowner
def partner_create_offer(token_partner, project_id):
    path = "/partner/offer"

    try:
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + token_partner
        }
        offers = minbolig_test_data.partner_create_offer_test_data['offers']

        response = requests.post(f'{config.host + path}',
                                 json={
                                     "projectId": project_id,
                                     "offers": offers
                                 },
                                headers=headers, verify=False)
        print(f'--------------------------------------------------')
        print(f'PARTNER CREATE OFFER')
        print(f'--------------------------------------------------')
        print(f'Status Code: {response.status_code}')
        print(f'Project Id: {project_id}')
        print(json.dumps(response.json(), indent=4, sort_keys=True))


    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))
        sys.exit(1)