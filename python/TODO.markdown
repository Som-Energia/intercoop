# TODO

## Phase 1: encription primitives

+ base64 encoding decoding
+ utf8 encoding/decoding after base64
+ binary base64
+ key generation, export, import
+ public key split
+ package signing/verification
- token generation

## Phase 2: pack and unpack messages

+ Review take yaml's as unicode
+ Parser takes key from dictionary and chooses acording the peer code
+ Error handling: bad peer code
+ Error handling: package is not valid yaml/unicode
+ Error handling: payload does not decode base64
+ Error handling: payload does not decode as valid yaml/unicode
+ Error handling: package has not the required fields
+ Error handling: payload has not the required fields
- Protect against unsafe yamls (limit yaml parser features)

## Phase 3: peer descriptors handling

- (Unsecure) temporary data storage
	+ Add a data set
	+ Retrieve a data set
	- Data set not found
	- Purgue old data
- Portal example


## Phase 4: communication

- Use package 
- Propagate api side exception
- Handle network error
- Return redirection url


