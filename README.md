# Digest for Raindrop.io

#### Raindrop API
Documentation: https://developer.raindrop.io/

Obtain authorization code (through browser):
```
curl --location --request GET 'https://raindrop.io/oauth/authorize?redirect_uri=http://localhost:5000&client_id=<client id>'
```

Obtain token:
```
curl --location --request POST 'https://raindrop.io/oauth/access_token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'code=<auth code>' \
--data-urlencode 'client_id=<client id>' \
--data-urlencode 'client_secret=<client secret>' \
--data-urlencode 'grant_type=authorization_code' \
--data-urlencode 'redirect_uri=http://localhost:5000'
```

Refresh token:
```
curl --location --request POST 'https://raindrop.io/oauth/access_token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'client_id=<client id>' \
--data-urlencode 'client_secret=<client secret>' \
--data-urlencode 'grant_type=refresh_token' \
--data-urlencode 'refresh_token=<refresh token>'
```

#### Chromedriver
[Chromedriver download](http://chromedriver.storage.googleapis.com/index.html)

- Download the latest version of the executable and place it inside the project directory
- On Macintosh, right click and Open one first time to make sure it has the right permissions