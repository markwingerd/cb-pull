import json
import urllib.request, urllib.parse

from django.conf import settings
from django.http import Http404


def get_resp(url, params=None):
    """
    Makes a request to a website and returns a dict
    Raises Http404
    """
    # Initialize variables
    if not params:
        params = {}
    params['user_key'] = settings.CRUNCHBASE_API_KEY
    params = urllib.parse.urlencode(params)
    url = '{url}?{params}'.format(url=url, params=params)

    # Make request and format Output
    req = urllib.request.Request(url)
    try:
        f = urllib.request.urlopen(req)
    except urllib.error.HTTPError:
        raise Http404
    resp = f.read().decode('utf-8')
    return json.loads(resp)

def get_company_url(name):
    """
    Searches CrunchBase for a company by name and returns its url
    Raises Exception if there is no sufficent match
    """
    # Search Crunchbase for the company
    url = 'https://api.crunchbase.com/v3.1/organizations'
    try:
        data = get_resp(url, {'name': name})
    except urllib.error.HTTPError:
        raise Http404
    # Ensure a sufficent match was found
    for company in data['data']['items']:
        if company['properties']['name'].lower() == name.lower():
            return company['properties']['api_url']
    # No company found
    raise Http404


def data_normalizer(data):
    """
    Normalizes data from the organizations endpoint. This will company specific
    data and people specific data and handle them seperately.
    Returns dict(company), list-of-dict(people)
    """
    data = data['data']
    company_properties = data['properties']
    relationships = data['relationships']
    company = {
        'uuid': data['uuid'],
        'cb_api_url': company_properties['api_url'],
        'name': company_properties['name'],
        'num_employees': company_properties['num_employees_min'],
        'total_funding_usd': company_properties['total_funding_usd'],
        'homepage_url': company_properties['homepage_url'],
        'cb_rank': company_properties['rank'],
        'founders': [el['uuid'] for el in relationships['founders']['items']],
        'featured_team': [el['uuid'] for el in relationships['featured_team']['items']],
        'current_team': [el['uuid'] for el in relationships['current_team']['items']],
        'board_advisors': [el['uuid'] for el in relationships['board_members_and_advisors']['items']],
        'investors': [el['uuid'] for el in relationships['investors']['items']],
    }

    return company, _people_normalizer(relationships)


def _people_normalizer(relationships):
    """
    Extracts all people from relationships and returns a list of unique
    normalized people.
    Returns list-of-dict(people)
    """
    # Join all people
    people_list = []
    people_list.extend(relationships['founders']['items'])
    people_list.extend(relationships['featured_team']['items'])
    people_list.extend(relationships['current_team']['items'])
    people_list.extend(relationships['board_members_and_advisors']['items'])
    people_list.extend(relationships['investors']['items'])
    # Normalize all people uniquely by uuid
    people_dict = {
        el['uuid']: _person_normalizer(el) for el in people_list
    }

    return people_dict.values()


def _person_normalizer(person_data):
    return {
        'uuid': person_data['uuid'],
        'name': _get_name(person_data),
        'cb_rank': person_data['properties'].get('rank', 0),
    }

def _get_name(data):
    """
    Returns 'firstname lastname' or 'name'
    """
    try:
        return '{} {}'.format(data['properties']['first_name'],
                              data['properties']['last_name'])
    except KeyError:
        return data['properties'].get('name', '')
