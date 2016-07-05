# Intercoop

[![Build Status](https://travis-ci.org/Som-Energia/intercoop.svg?branch=master)](https://travis-ci.org/Som-Energia/intercoop)

## Purpose

In the context of intercooperation among social economy entities,
these libraries implement a protocol to allow a user of a source portal to enable services on a third entity
in a way users control which third party services get enabled and transfer their personal data to.

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



## Python library

- Examples:

    - portalexample: Flask based example of a source entity portal
    - apiexample: Flask based example of a target entity api

- Fully reusable modules:

    - crypto: cryptography primitives:
        - hides actual algorithms compexity under simple action names
    - package: encapsulates package marshalling/umarshalling, signing/verification
    - apiclient: encapsulates remote acces to the target API

- Data sources: You normally want to rewrite those, for example to take data from a database or similar. Reference implementation use a directory full of YAML files.

    - Source Portal:
        - peerinfo: access yaml info provided by the available targets
        - userinfo: access source user personal dataa

    - Target API:
        - keyring: provided a peer 
        - remoteuserinfo: temporary stores the transferred data

- Utilities:

    - translator: rewrites yamls by picking language on translatable strings
    - perfume: a utility to make Flask apps dependency injectable






