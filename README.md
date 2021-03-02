# Lies!
According to https://gist.github.com/victorhurdugaci/1a817055af6c6fc966d33c0d91408c77...
 
* Language codes listed as ISO 639-1 format... but the actual data contains an error:
  * `fre` which is ISO 639-2/B
* Country codes are listed as ISO 639-1 format... but that's a language spec. Country codes should probably have been listed as ISO 3166-1 format.
* Ad id = "104438d9" starts at hour 14, and ends at hour 2. Suspicious, if you ask me.
* While we're at it, based on the definition of 'end_hour', I don't think any ads will be served up from 11:00pm to Midnight UTC. (More of a missed opportunity, than an error.)


## TODO Items:
* Create separate services:
  * Login/authentication/authorization
  * UIs for Performance monitoring, system configuration, user management (or even better, integrate into corporate solutions)
  * Service interfaces to allow implementation swapping for extensibility as well as testing
* Create CI/CD pipeline
  * Setup (or integrate with) artifact repository (e.g. Nexus)
* Auth(entication|orization) Probably something simple like JWTs:
  * Add HTTPS support
  * Add permissions model with users & roles, with mappings for roles/operations
  * Add auth to Swagger UI
* For scalability:
  * Create a separate database layer (perhaps with caching layer between it and services)
  * Put services into containers (e.g. Docker in Kubernetes)
  * Place load-balancer on front of service APIs
* Add support for internationalization?
  * i18n for country/language URL params, maybe

## Running:
```
git clone https://github.com/jlfemino/simulmedia.git
cd simulmedia
make all
```
Point browser to:
* `http://localhost:5000/api_docs` for Swagger UI
* `simulmedia/htmlcov/index.html` for test coverage
