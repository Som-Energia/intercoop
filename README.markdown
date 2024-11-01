# Intercoop

[![CI Status](https://github.com/Som-Energia/intercoop/actions/workflows/main.yml/badge.svg)](https://github.com/Som-Energia/intercoop/actions/workflows/main.yml)
[![Coverage Status](https://coveralls.io/repos/github/Som-Energia/intercoop/badge.svg?branch=master)](https://coveralls.io/github/Som-Energia/intercoop?branch=master)

## Purpose

In the context of intercooperation among social economy entities,
these libraries implement a protocol to enable a user of a given entity
to use services provided by other entities having a bilateral agreement.
This is done keeping the users in control of which are the enabled
services and, most important, which entities will be transferred
their personal data to.

Some intended goals:

- Easely extend intercooperation to new entities by sharing a common protocol, so that:
    - You implement once how your users access services provided by many other entities
    - You implement once how to offer our services to users coming from many other entities
- Be certain that the services request comes from a user of the source entity
- Keep users in control of how and whom their personal data is transferred to
- Still avoid the user from having to type personal data again and again


## Glossary

- Entity: one of the social economy peers that are intercooperating
- User: one of the legal or physical person who have rights regarding a entity
- Role: A set of rights a user might have within an entity (pe. member, worker, different kind of members...)
- Source entity: The entity a member has rights on.
- Target entity: The entity whose services are enabled for members of the source entity.
- Portal: Website for validated users of the source entity
- API: B2B web API offered by the target entity to the source entity.

## Main protocol sequence

Case: a user of entity A (source) wants to enable service of intercooperation entity B (target):

Preconditions:

- Each entity has its own RSA public/private pair of keys
- Intercooperating entities share their public key among them and keep their private one secret
- User has validated its identity on web portal of entity A

Main course scenario:

- User indicates to _source Portal_ the intent of activating a service on _target entity_
- _Source portal_ shows the user which data will be transferred to _target entity_ (member number, national id, name, address, emal...) and **asks for consent**
- User consents the transfer
- _Source portal_ builds a message cointaining trasferred data and signs it using Source's private key.
- _Source portal_ sends the message to https API on _target entity_
- _Target API_ validates the signature with source's public key, stores the transferred data and generates a token for later reference
- _Target API_ responds to _Source Portal_ with an url on B having the token embedded inside.
- _Source Portal_ redirects user's browser to that url, where the process to get the service can continue.


## Errors

- Portal -> API
	- Not yaml message
	- Missing message fields
	- Not yaml payload
	- Missing payload fields
	- Source entity has no intercooperation agreement with target one
	- Bad signature

- Service errors
    - Service unavailable (at all, for peer, for user, for role)
    - Missing payload fields (because the application needs)



## Workflow

### Source portal's view

- Portal renders intercooperation options
	- Access to every provider info an services.
		- Provider: Id, name, description, url, logo, services...
		- Services: id, description, image, activation api

- User click on one option
	- Browser sends provider and service id

- Portal asks the user permision to send several data
	- Gather the required data for the service
	- Gather the privacy policy from the service
	- Obtain personal data from the portal ERP user

- User accepts the transfer and the privacy police

- Portal sends the info to the provider Api

	- Gather required data for the service
	- Build a signed package with it
	- Send it to the service url
	- Wait response
	- Handle any error if it happens
	- Else redirect user's browser to the url with the token


### Target api's view

- The API receives signed data from a Portal
	- Check and unpack data from package
		+ Check package utf8 yaml (raise if not valid yaml)
		+ Check fields in package (intercoopversion, payload, signature) (raise if any if missing)
		+ Check for matching intercoopversion (raise if different)
		+ Base64 decode payload (raise if not bas64 utf8)
		+ Parse yaml in decoded payload (raise if not valid yaml)
		+ Check originpeer field (raise if there is not)
		+ Gather public key for origin peer (raise if there is not such pear)
		+ Check signature (raise if untrusted)

	- Check service requirements
		- Check all required fields are in data (raise if not)
		- Check peer-role-service is ok (raise if not)
		- Check info depending of service, for instance:
			- Service geographically availability
			- Limits by user or peer

	- Store data
		+ Generate a token
		+ Save data related to the token

	- Compose response
		- Embed token into url
		- If have raised an error response is composed

- The target web/api receives the request url with the token from the user's browser
	- Expires old stored data
	- Gathers the data by token (raises error if so)
	- Creates a session
	- Renders page to follow service procedure






