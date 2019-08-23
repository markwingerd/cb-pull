from django.db import models


class Person(models.Model):
    uuid = models.CharField(primary_key=True, max_length=128, editable=False)
    name = models.CharField(max_length=128)
    cb_rank = models.IntegerField()


class Company(models.Model):
    uuid = models.CharField(primary_key=True, max_length=128, editable=False)
    name = models.CharField(max_length=128)
    cb_api_url = models.CharField(max_length=256)
    cb_rank = models.IntegerField()
    num_employees = models.IntegerField()
    total_funding_usd = models.BigIntegerField()
    homepage_url = models.CharField(max_length=256)
    founders = models.ManyToManyField(Person, related_name='company_founders')
    featured_team = models.ManyToManyField(Person, related_name='company_featuredteam')
    current_team = models.ManyToManyField(Person, related_name='company_currentteam')
    board_advisors = models.ManyToManyField(Person, related_name='company_boardadvisors')
    investors = models.ManyToManyField(Person, related_name='company_investors')
