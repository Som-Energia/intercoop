# python-intercoop


[![CI Status](https://github.com/Som-Energia/intercoop/actions/workflows/main.yml/badge.svg)](https://github.com/Som-Energia/intercoop/actions/workflows/main.yml)
[![Coverage Status](https://coveralls.io/repos/github/Som-Energia/intercoop/badge.svg?branch=master)](https://coveralls.io/github/Som-Energia/intercoop?branch=master)


A Python implementation of the intercoop protocol.

## Purpose

In the context of intercooperation among social economy entities,
these libraries implement a protocol to enable a user of a given entity
to use services provided by other entities having a bilateral agreement.
This is done keeping the users in control of which are the enabled
services and, most important, which entities will be transferred
their personal data to.

Some intended goals:

- Ease extending intercooperation to new entities by sharing a common protocol,
    - single implementation for our users to use services from many other entities,
    - single implementation to offer our services to users of many other entities
- Be certain that the services request comes from the source entity 
- Users control how and whom their personal data is transferred to
- Still avoid the user from having to type personal data again and again


## Install

```bash
$ pip install .

```


## Modules

- Examples:

    - `portalexample`: Flask based example of a source entity portal
    - `apiexample`: Flask based example of a target entity api

- Fully reusable modules:

    - `catalog`: functions to manage a service catalog in a portal
    - `apiclient`: encapsulates remote acces to the target API
    - `package`: encapsulates package marshalling/umarshalling, signing/verification
    - `crypto`: cryptography primitives:
        - hides actual algorithms compexity under simple action names

- Data sources: You normally want to rewrite those, for example to take data from a database or similar. Reference implementation use a directory full of YAML files.

    - Source Portal:
        - `peerinfo`: access yaml info provided by the available targets
        - `userinfo`: access source user personal data

    - Target API:
		- `keyring`: gives access to peers public keys (relies on `peerinfo`)
        - `remoteuserinfo`: temporary stores the transferred data

- Utilities:

    - `translator`: rewrites yamls by picking language on translatable strings
    - `perfume`: a Flask wrapper to enable dependency injection on Flask apps

## Example scripts

- `portal-example-somillusio.py`: _somillusio_ portal
- `api-example-somacme.py`: _somacme_ api and service form


## Other scripts

- `validate-intercoop.py`: Validates a peer info yaml



