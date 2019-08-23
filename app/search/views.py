from django.http import HttpResponse
from django.shortcuts import redirect

from company.models import Company, Person
from search.libs import crunchbase

def index(request):
    # Get company and people information from CrunchBase
    name = request.GET.get('name')
    company_url = crunchbase.get_company_url(name)
    company_data = crunchbase.get_resp(company_url)
    company_norm, people_norm = crunchbase.data_normalizer(company_data)
    # Add all necessary data to the DB
    company = Company(
        uuid=company_norm['uuid'],
        name=company_norm['name'],
        cb_api_url=company_norm['cb_api_url'],
        cb_rank=company_norm['cb_rank'],
        num_employees=company_norm['num_employees'],
        total_funding_usd=company_norm['total_funding_usd'],
        homepage_url=company_norm['homepage_url'],
    )
    company.save()
    people = {}
    for person_norm in people_norm:
        person = Person(**person_norm)
        person.save()
        people[person_norm['uuid']] = person
    # Create all relationships between the company and people
    for uuid in company_norm['founders']:
        company.founders.add(people[uuid])
    for uuid in company_norm['featured_team']:
        company.featured_team.add(people[uuid])
    for uuid in company_norm['current_team']:
        company.current_team.add(people[uuid])
    for uuid in company_norm['board_advisors']:
        company.board_advisors.add(people[uuid])
    for uuid in company_norm['investors']:
        company.investors.add(people[uuid])
    company.save()

    return redirect('/company/{}'.format(company_norm['uuid']))
