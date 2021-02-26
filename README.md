# Lies!
According to https://gist.github.com/victorhurdugaci/1a817055af6c6fc966d33c0d91408c77...
 
* Language codes listed as ISO 639-1 format... but the actual data contains an error:
  * `fre` which is ISO 639-2/B
* Country codes are listed as ISO 639-1 format... but that's a language spec. Country codes should probably have been listed as ISO 3166-1 format.


## TODO Items:
* Auth(entication|orization) Probably something simple like JWTs:
  * Add permissions model with users & roles, with mappings for roles/operations
  * Add auth to Swagger UI
* Record performance metrics to somewhere (MetricsCore?)
* Create separate services for:
  * Login/authentication/authorization
  * Ad service
  * Performance monitoring, system configuration, user management
  * Create CI/CD pipeline
* For scalability:
  * Place load-balancer on front of service APIs
  * Create a separate database layer (perhaps with caching layer between it and services)
  * Put services into containers (e.g. Docker in Kubernetes)
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
