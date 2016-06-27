# Source portal's view

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


# Target api's view

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



