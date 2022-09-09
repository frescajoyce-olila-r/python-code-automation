import json

# Minbolig Registration calling json file
with open("test_data\\registration.json") as f:
    registration_test_data = json.load(f)

# Minbolig Login calling json file
with open("test_data\\login.json") as f:
    login_test_data = json.load(f)

# Minbolig Send Message calling json file
with open("test_data\\send_message.json") as f:
    send_message_test_data = json.load(f)

# Minbolig Create Calendar calling json file
with open("test_data\\calendar.json") as f:
    create_calendar_test_data = json.load(f)

# Minbolig Create Folder calling json file
with open("test_data\\create_folder.json.") as f:
    create_folder_test_data = json.load(f)

# Minbolig Rename Folder calling json file
with open("test_data\\rename_folder.json") as f:
    rename_folder_test_data =json.load(f)

# Minbolig Create Project Calling json file
with open("test_data\\create_project.json") as f:
    create_project_test_data = json.load(f)

# Minbolig Create Initial Budget json file
with open("test_data\\create_initial_budget.json") as f:
    create_initial_budget_test_data = json.load(f)

# Minbolig Add Budget json file
with open("test_data\\add_budget.json") as f:
    add_budget_test_data = json.load(f)

# Minbolig Prisberegnere json file
with open("test_data\\prisberegnere_calculator.json") as f:
    prisberegnere_calculator_test_data = json.load(f)

# Minbolig Favorite json file
with open("test_data\\favorite.json") as f:
    favorites = json.load(f)

# Minbolig Inspiration calling json file
with open("test_data\\inspiration.json") as f:
    inspiration = json.load(f)

# Minbolig Upload Billeder Calling json file
with open("test_data\\upload_billeder.json") as f:
    upload_billeder = json.load(f)

# Minbolig MineTilbud ContractType
with open("test_data\\minetilbud_contractType.json") as f:
    minetilbud_contractType = json.load(f)

# Minbolig Upload billeder json file
with open("test_data\\todo_upload_billeder.json") as f:
    todo_upload_billeder = json.load(f)

# Minbolig Send offer to Partner json file
with open("test_data\\offer_send_invitation_to_partner.json") as f:
    offer_send_invitation = json.load(f)

# Minbolig Henttilbud Anbefalet json file
with open("test_data\\henttilbud_anbefalet.json") as f:
    hentilbud_anbefalet = json.load(f)

# Partner Login json file
with open("test_data\\partner_login.json") as f:
    partner_login_test_data = json.load(f)

# Partner Create Offer json file
with open("test_data\\partner_create_offer.json") as f:
    partner_create_offer_test_data = json.load(f)

# Create Contract json file
with open("test_data\\create_contract.json") as f:
    create_contract_test_data = json.load(f)

# Payment stages for contract json file
with open("test_data\\payment_stages_contract.json") as f:
    payment_stages_test_data = json.load(f)
