**As a** developer
**I need** a REST API for account management
**So that** customers can be onboarded digitally

### Details and Assumptions

* The service manages customer accounts with name, email, address, phone number, and date joined
* Accounts are stored in a relational database via SQLAlchemy
* The API follows REST conventions and returns JSON
* The service will be deployed as a containerized microservice on Kubernetes / OpenShift
* Authentication and authorization are out of scope for this capstone

### Acceptance Criteria

```gherkin
Given a running accounts service
When I POST a valid account payload to /accounts
Then I should receive a 201 CREATED response with the new account and a Location header

Given accounts exist in the database
When I GET /accounts
Then I should receive a 200 OK response with a list of all accounts

Given an account exists with a known id
When I GET /accounts/{id}
Then I should receive a 200 OK response with that account

Given an account exists with a known id
When I PUT updated data to /accounts/{id}
Then I should receive a 200 OK response with the updated account

Given an account exists with a known id
When I DELETE /accounts/{id}
Then I should receive a 204 NO CONTENT response and the account should be gone

Given a request for an account that does not exist
When I GET /accounts/{id}
Then I should receive a 404 NOT FOUND response
```
