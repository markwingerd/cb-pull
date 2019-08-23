# cb-pull
Pulls company information from crunchbase and displays information in a manner that is quicker to get a general impression of the success of a company

This project will run a simple configuration of Django where bulk of the project is in calling on crunchbases API or scraping the website for necessary information. Output will be in either raw JSON or a simple Django template output.

### Endpoints

#### GET /search/

Returns an overview of a company including Name, website, founders, money raised, etc as seen on Crunchbase

Params:

 - **name**(string): Name of a company to search for

 Example:
 ```
 GET /search/?name=cd%20projekt%20red
 ```

#### GET /company/{name:string}/

Returns an overview of a company

Example:
```
GET /company/cd-projekt-red
```

### GET /people/{name:string}/

If time permits, an endpoint can be created allowing the user get data on a given person including companies they are involved in and crunchbase rank.


### Models

#### Company

Includes name, rank, website, money raised, and association to people in the form of founders.

#### People

Includes name and rank
