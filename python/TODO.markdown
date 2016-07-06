# TODO

## Postponed

- [ ] portal: enhance appearance
- [ ] api: continuation page different from info getter api
- [ ] userinfo: Translations for field names
- [ ] userinfo: process differently unsupported and not pressent fields
- [ ] peerinfo: consider more semantic accessors
- [ ] peerinfo: Own exception types (not just plain Exception)
- [ ] remoteuserinfo: Purgue old data
- [ ] packaging: Protect against unsafe yamls (limit yaml parser features)
- [x] packaging: Embed data in errors so that they can be restored in client
- [x] api: Return uri instead of (or besides) the uuid
- [ ] api: service level checks
    - [ ] api: Check all required values
    - [ ] api: Check services availability for the peer
    - [ ] api: Check service version is all right
    - [ ] api: Check other service specific constraints (geographical, user roles, amount...)
- [ ] Nicer keyring (folder based)
	- [ ] Given a peer id return the public key
	- [ ] Raise an error if no key available
	- [ ] Handle error in the case of bad key format

- [ ] portal: extract 'providers' as constructor parameters
    - [x] portal: extract peers info
    - [x] portal: extract user info
    - [ ] portal: extract key
- [ ] activateservice: special display for list fields
- [ ] activateservice: special display for None fields
- [ ] bad peer in required fields
- [ ] bad service in required fields
- [ ] Solve translations
- [ ] Should different types in field be rendered differently
- [ ] No service description
- [ ] No service name
- [ ] No such service
- [ ] Include peer.info optionally
- [ ] require login

## DONE: Initial Roadmap

### Phase 1: encription primitives

- [x] base64 encoding decoding
- [x] utf8 encoding/decoding after base64
- [x] binary base64
- [x] key generation, export, import
- [x] public key split
- [x] package signing/verification
- [x] token generation

### Phase 2: pack and unpack messages

- [x] Review take yaml's as unicode
- [x] Parser takes key from dictionary and chooses acording the peer code
- [x] Error handling: bad peer code
- [x] Error handling: package is not valid yaml/unicode
- [x] Error handling: payload does not decode base64
- [x] Error handling: payload does not decode as valid yaml/unicode
- [x] Error handling: package has not the required fields
- [x] Error handling: payload has not the required fields

### Phase 3: dummy information sources

- [x] Unsecure temporary data storage
	+ [x] Add a data set
	+ [x] Retrieve a data set
	+ [x] Data set not found

- [x] Keyring
	- [x] Dummy keyring

- [x] Peer descriptors
    - [x] Constructor error when no such folder -> Not needed get fails anyway
	- [x] Get by peer id
        - [x] present
        - [x] missing
        - [x] protection against malicious ids (../../) limit to alphanum
    - [x] Iterador

### Phase 4: API example

- [x] API example
	- [x] Solve mockup injection in flask for testing
	- [x] Implement success case on register data
	- [x] Consider different error cases
	- [x] Implement getter

### Phase 5: Portal example

- [x] Encapsulate api calling and error handling

- [x] Translations

- [x] Implement portal example
    - [x] route activateservice/<peer>/<service>
        - [x] fields = portal.requiredFields(peer, service)
            - [x] when service fields, use them
            - [x] when no service fields, use global peer fields
            - [x] when no fields anywhere, raise
        - [+] data = portal.userInfo(userid, fields)
            - [+] all fields
            - [+] filtering
            - [+] no such user
            - [+] no such field
        - [x] translations = portal.fieldTranslation(fields)
            - [+] One level, translation and field exist
            - [+] One level, field exists but translation no
            - [+] One level, field doesn't exist
            - [x] Many level field
        - [x] fieldhtml = portal.renderField(fieldLabel, value)
        - [x] innerhtml = portal.renderUserData(data)
    - [x] route confirmactivateservice/<peer>/<service>
	- [x] Use package 
	- [x] Propagate api side exception
	- [x] Handle network error
	- [x] Return redirection url




