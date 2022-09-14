import logging
import minbolig_functions
import partner_functions

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='logfile.log', level=logging.DEBUG)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.info('--------------------------------------------------')
    logging.info('----- Running MINBOLIG API AUTOMATION script -----')
    logging.info('--------------------------------------------------')
    print('--------------------------------------------------')
    print('----- Running MINBOLIG API AUTOMATION script -----')
    print('--------------------------------------------------')

    # # Call to register
    # register_response = minbolig_functions.register()
    #
    # # Call to retrieve unique id
    # unique_id_response = minbolig_functions.retrieve_unique_id(register_response.json()['data']['user']['ID'])
    #
    # # Call to verify
    # minbolig_functions.verify(unique_id_response.json()['data'][0]['UNIQUE_ID'])
    #
    # # Call to Login after Register
    # login_register = minbolig_functions.login_through_register()

    # Call to Log in
    login_response = minbolig_functions.login()
    token = login_response.json()['data']['user']['TOKEN']

    # Create Project
    create_project = minbolig_functions.create_project(token)
    project_id = create_project.json()['data']['ID']
    folder_id1 = create_project.json()['data']['FOLDER_ID']

    # Inspiration
    minbolig_functions.inspiration(token, project_id)

    # Upload Billeder
    minbolig_functions.upload_billeder(token, folder_id1)

    # To do Upload Billeder
    minbolig_functions.todo_upload_billeder(token, project_id)

    # Prisberegnere AI Calculator
    minbolig_functions.prisberegnere_calculator(token)

    #Create Budget
    minbolig_functions.create_initial_budget(token, project_id)

    # Add Budget
    minbolig_functions.add_budget(token, project_id)


    # # Send Offer for henttilbud
    # minbolig_functions.henttilbud_anbefalet(token, project_id)

    # Create Folder
    create_folder = minbolig_functions.create_folder(token)
    folder_id = create_folder.json()['data']['ID']
    parent_id = create_folder.json()['data']['PARENT_ID']

    # # Rename Folder
    # minbolig_functions.rename_folder(token, folder_id)

    # Send Messages in email
    minbolig_functions.send_messages(token)

    # Create Meeting in Calendar
    minbolig_functions.create_meeting(token)

    # Favorite
    minbolig_functions.Favorite(token)

    # Add ContractType
    minbolig_functions.minetilbud_contractType(token, project_id)

    # Send Offer to Invitation to Partner
    minbolig_functions.send_offer_invitation_to_partner(token, project_id)

    # Login to Partner
    partner_login =partner_functions.partner_login()
    token_partner = partner_login.json()['data']['token']

    # Partner Get Invitation ID
    get_invitation =partner_functions.get_invitation_id(token_partner, project_id)
    invitation_id = get_invitation.json()['data']['INVITATION_ID']

    # Partner Accept Offer sent by the homeowner
    partner_functions.partner_accept_offer(token_partner, invitation_id)

    # Partner Creates and offer
    partner_functions.partner_create_offer(token_partner, project_id)

    # Minbolig Get Offer Id
    get_offer_id = minbolig_functions.get_offer_id_minbolig(token,project_id)

    for i in get_offer_id.json()['data']:
        offer_id = i['ID']

        # Accept Offer in Minbolig
        minbolig_functions.accept_offer_minbolig(token, project_id, offer_id)


    # Create Contract in Minbolig
    minbolig_contract = minbolig_functions.create_contract_minbolig(token, project_id)
    # contract_id = minbolig_contract.json()['data']['DOCUMENTS']['CONTRACT_ID']
    # print(f'Contract ID :{contract_id}')


    # Create project Meeting in Minbolig
    minbolig_functions.create_project_meeting(token, project_id)

    # Get Timeline Id
    get_timeline_id =minbolig_functions.get_timeline_id(token, project_id)
    timeline_id = get_timeline_id.json()['data']['ID']

    # Create Timeline Task
    minbolig_functions.create_timeline_task(token, timeline_id)

    # Submit Timeline Task
    minbolig_functions.submit_timeline_created(token, timeline_id)

    # Partner approves timeline created by the homewoner
    partner_functions.partner_approve_timeline(token_partner, timeline_id)

    # Accept Contract Minbolig Side
    # minbolig_functions.accept_contract_minbolig(token, contract_id)





