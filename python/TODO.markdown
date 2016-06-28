# TODO

## Phase 1: encription primitives

- [x] base64 encoding decoding
- [x] utf8 encoding/decoding after base64
- [x] binary base64
- [x] key generation, export, import
- [x] public key split
- [x] package signing/verification
- [x] token generation

## Phase 2: pack and unpack messages

- [x] Review take yaml's as unicode
- [x] Parser takes key from dictionary and chooses acording the peer code
- [x] Error handling: bad peer code
- [x] Error handling: package is not valid yaml/unicode
- [x] Error handling: payload does not decode base64
- [x] Error handling: payload does not decode as valid yaml/unicode
- [x] Error handling: package has not the required fields
- [x] Error handling: payload has not the required fields

## Phase 3: dummy information sources

- [x] Unsecure temporary data storage
	+ [x] Add a data set
	+ [x] Retrieve a data set
	+ [x] Data set not found

- [x] Keyring
	- [x] Dummy keyring

## Phase 4: API example

- [x] API example
	- [x] Solve mockup injection in flask for testing
	- [x] Implement success case on register data
	- [x] Consider different error cases
	- [x] Implement getter

## Phase 5: Portal example

- [ ] Encapsulate api calling and error handling

- [ ] Peer descriptors
	- [ ] Get by peer id
	- [ ] Get translated string

- [ ] Portal example
	- [ ] Use package 
	- [ ] Propagate api side exception
	- [ ] Handle network error
	- [ ] Return redirection url

## TODO Remainders

- [ ] unsecuredatastorage: Purgue old data
- [ ] packaging: Protect against unsafe yamls (limit yaml parser features)
- [ ] packaging: Embed data in errors so that they can be restored in client
- [ ] api: Return uri instead of (or besides) the uuid
- [ ] api: Check all required values
- [ ] api: Check services availability for the peer
- [ ] api: Check other service specific constraints (geographical, user roles, amount...)
- [ ] Proper keyring (either build one or use peer descriptors
	- [ ] Given a peer id return the public key
	- [ ] Raise an error if no key available
	- [ ] Handle error in the case of bad key format





