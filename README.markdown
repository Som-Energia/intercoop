# Intercoop

[![Build Status](https://travis-ci.org/Som-Energia/intercoop.svg?branch=master)](https://travis-ci.org/Som-Energia/intercoop)

## Purpose

In the context of intercooperation among social economy entities,
these libraries implement a protocol to enable a user of a given entity
to use services provided by other entities having a bilateral agreement,
in a way users control which services get enabled and which entities
transfer their personal data to.

Some intended goals:

- Ease extending intercooperation to new entities by sharing a common protocol,
    - single implementation for our users to use services from many other entities,
    - single implementation to offer our services to users of many other entities
- Be certain that the services request comes from the source entity 
- Keep users in control of how and whom their personal data is transferred to
- Still avoid the user from having to type personal data again and again


## Glossary

- Entity: one of the social economy peers that are intercooperating
- User: one of the legal or physical person who have rights regarding a entity
- Role: A set of rights a user might have within an entity (pe. member, worker, different kind of members...)
- Source entity: The entity a member has rights on.
- Target entity: The entity whose services are enabled for members of the source entity.
- Portal: a website for validated users of an entity
- API: B2B web API

## Main protocol sequence

Case: a user of entity A (source) wants to enable service of intercooperation entity B (target):

Preconditions:

- Each entity has its own RSA public/private pair of keys
- Intercooperating entities share their public key among them and keep their private one secret
- User has validated its identity on web portal of entity A

Main course scenario:

- User indicates to entity A's Portal (Portal A) the intent of activating a service on entity B
- Portal A shows the user which data will be transferred to entity B (member number, national id, name, address, emal...) and **asks for consent**
- User consents the transfer
- Portal A builds a message cointaining trasferred data and signs it using A's private key.
- Portal A sends the message to https API on entity B
- API B validates the signature with A's public key, stores the transferred data and generates a token for later reference
- API B responds to Portal A with an url on B having the token embedded inside.
- Portal A redirects user's browser to that url, where the process to get the service can continue.


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






