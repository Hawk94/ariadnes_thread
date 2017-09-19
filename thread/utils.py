import os
import requests

class CompaniesHouseSearch:

    def __init__(self, access_token=None):
        access_token = (
            access_token or
            os.environ.get('COMPANIES_HOUSE_KEY'))
        self._BASE_URI = "https://api.companieshouse.gov.uk/"
        self.session = requests.Session()
        self.session.auth = (access_token, '')
        self.session.params.update(access_token=access_token)

    def search_officers(self, term, disqualified=False, **kwargs):
        """Search for officers by name.
        Args:
          term (str): Officer name to search on.
          disqualified (Optional[bool]): True to search for disqualified
            officers
          kwargs (dict): additional keywords passed into
            requests.session.get params keyword.
        """
        search_type = ('officers' if not disqualified else
                       'disqualified-officers')
        params = kwargs
        params['q'] = term
        baseuri = self._BASE_URI + 'search/{}'.format(search_type)
        res = self.session.get(baseuri, params=params)
        return res

    def appointments(self, num, **kwargs):
        """Search for officer appointments by officer number.
        Args:
          num (str): Officer number to search on.
          kwargs (dict): additional keywords passed into
          requests.session.get params keyword.
        """
        baseuri = self._BASE_URI + 'officers/{}/appointments'.format(num)
        res = self.session.get(baseuri, params=kwargs)
        return res

    def profile(self, num):
        """Search for company profile by company number.
        Args:
          num (str): Company number to search on.
        """
        baseuri = self._BASE_URI + "company/{}".format(num)
        res = self.session.get(baseuri)
        return res

    def insolvency(self, num):
        """Search for insolvency records by company number.
        Args:
          num (str): Company number to search on.
        """
        baseuri = self._BASE_URI + "company/{}/insolvency".format(num)
        res = self.session.get(baseuri)
        return res

    def filing_history(self, num, transaction=None, **kwargs):
        """Search for a company's filling history by company number.
        Args:
          num (str): Company number to search on.
          transaction (Optional[str]): Filing record number.
          kwargs (dict): additional keywords passed into
            requests.session.get params keyword.
        """
        baseuri = self._BASE_URI + "company/{}/filing-history".format(num)
        if transaction is not None:
            baseuri += "/{}".format(transaction)
        res = self.session.get(baseuri, params=kwargs)
        return res

    def charges(self, num, charge_id=None, **kwargs):
        """Search for charges against a company by company number.
        Args:
          num (str): Company number to search on.
          transaction (Optional[str]): Filing record number.
          kwargs (dict): additional keywords passed into
          requests.session.get params keyword.
        """
        baseuri = self._BASE_URI + "company/{}/charges".format(num)
        if charge_id is not None:
            baseuri += "/{}".format(charge_id)
            res = self.session.get(baseuri, params=kwargs)
        else:
            res = self.session.get(baseuri, params=kwargs)
        return res

    def officers(self, num, **kwargs):
        """Search for a company's registered officers by company number.
        Args:
          num (str): Company number to search on.
          kwargs (dict): additional keywords passed into
            requests.session.get *params* keyword.
        """
        baseuri = self._BASE_URI + "company/{}/officers".format(num)
        res = self.session.get(baseuri, params=kwargs)
        return res