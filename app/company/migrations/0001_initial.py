# Generated by Django 2.2.4 on 2019-08-23 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('uuid', models.CharField(editable=False, max_length=128, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('cb_rank', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('uuid', models.CharField(editable=False, max_length=128, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('cb_api_url', models.CharField(max_length=256)),
                ('cb_rank', models.IntegerField()),
                ('num_employees', models.IntegerField()),
                ('total_funding_usd', models.BigIntegerField()),
                ('homepage_url', models.CharField(max_length=256)),
                ('board_advisors', models.ManyToManyField(related_name='company_boardadvisors', to='company.Person')),
                ('current_team', models.ManyToManyField(related_name='company_currentteam', to='company.Person')),
                ('featured_team', models.ManyToManyField(related_name='company_featuredteam', to='company.Person')),
                ('founders', models.ManyToManyField(related_name='company_founders', to='company.Person')),
                ('investors', models.ManyToManyField(related_name='company_investors', to='company.Person')),
            ],
        ),
    ]
