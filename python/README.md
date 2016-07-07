# python-intercoop

[![Build Status](https://travis-ci.org/Som-Energia/intercoop.svg?branch=master)](https://travis-ci.org/Som-Energia/intercoop)


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

    - `crypto`: cryptography primitives:
        - hides actual algorithms compexity under simple action names
    - `package`: encapsulates package marshalling/umarshalling, signing/verification
    - `apiclient`: encapsulates remote acces to the target API

- Data sources: You normally want to rewrite those, for example to take data from a database or similar. Reference implementation use a directory full of YAML files.

    - Source Portal:
        - `peerinfo`: access yaml info provided by the available targets
        - `userinfo`: access source user personal dataa

    - Target API:
        - `keyring`: provided a peer 
        - `remoteuserinfo`: temporary stores the transferred data

- Utilities:

    - `translator`: rewrites yamls by picking language on translatable strings
    - `perfume`: a Flask wrapper to enable dependency injection on Flask apps

## Example scripts

- portal-example.py: _somillusio_ portal
- api-example.py: _somacme_ api




