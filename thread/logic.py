from thread.utils import CompaniesHouseSearch

def get_company_info(company_number, service=None):
    """
    Retrieves information about a company from Companies House.
    Args:
        company_no (str): Registered company number.
    Returns:
        Information Companies House holds on the company.
    """
    if service is None:
        service = CompaniesHouseSearch()
    company_profile = service.profile(company_no)
    return company_profile.json()


def get_associated_companies_info_by_company(company_number, depth=1):
    """
    Finds information about all companies associated through officers with the starting company.

    Args:
        company_no (str):  The company number we want to search associated companies with.
        depth (int): The depth of search in the graph of companies.

    Returns:
        A list of information about all associated companies up to the given depth.
    """
    service = CompaniesHouseSearch(access_token='')
    associated_companies = {0: [company_number],
                            1: []}
    officers = get_officers_by_company(associated_companies[0], service)
    companies = []
    for officer in officers:
        companies += get_companies_by_officer(officer, service)
    associated_companies[1] = set(companies)

    return associated_companies

def get_officers_by_company(company_numbers, service):
    """Return a list of officers associated to a given set of companies.

    Args:
        company_numbers (list): a list of company numbers to query against
        service (obj): instance of the companies house api interface
    Returns:
        associated_officers (list): id's of assoicaited officers
    """
    associated_officers = list()
    for company_number in company_numbers:
        officers = service.officers(company_number).json()
        officer_ids = [get_officer_id_from_item(i) for i in officers['items']]
        associated_officers += officer_ids
    return associated_officers


def get_officer_id_from_item(item):
    """Returns the officer id from an appointment item.
    Args:
        appointment (dict): appointment item
    Returns:
        officer_id (str): unique officer id assigned by companies house
    """
    return item['links']['officer']['appointments'].split('/')[2]


def get_companies_by_officer(officer_id, service):
    """Return a list of company numbers that are related to a given officer.

    Args:
        officer_id (str): the unique id officer
        service (obj): instance of the companies house api interface
    Returns:
        company_numbers (list): list of related companies
    """
    company_numbers = []
    related_companies = service.appointments(officer_id).json()
    for i in related_companies['items']:
        company_numbers += [i['appointed_to']['company_number']]
    return company_numbers