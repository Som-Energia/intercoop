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
- [ ] Protect against unsafe yamls (limit yaml parser features)

## Phase 3: peer information


- [ ] Unsecure temporary data storage
	+ [x] Add a data set
	+ [x] Retrieve a data set
	+ [x] Data set not found
	- [ ] Purgue old data

- [ ] Keyring
	- [ ] Given a peer id return the public key
	- [ ] Raise an error if no key available
	- [ ] Handle error in the case of bad key format

- [ ] Portal example
	- [ ] Solve mockup injection in flask for testing
	- [ ] Implement success case
	- [ ] Consider different error cases

- [ ] Peer descriptors
	- [ ] Get by peer id
	- [ ] Get translated string


## Phase 4: client (portal) side

- [ ] Use package 
- [ ] Propagate api side exception
- [ ] Handle network error
- [ ] Return redirection url


