# Two Factor Djagno Authentication 
Made using djangorestframework and django-rest-auth, this is just a template and can be extended to support sending email. Right now it just logs the otp instead of sending it to the user.

## Installation
1. Clone the repository
2. ```docker build -t 2fa .```
3. ```docker run -p 8000:8000 2fa```

## Usage
1. Create a user using the following command
```
curl -X POST http://localhost:8000/api/registration/ -H 'Content-Type: application/json' -d '{"email": "test@example.com"} '
```
2. Generate OTP
```
curl -X POST http://localhost:8000/api/request-otp/ -H 'Content-Type: application/json' -d '{"email":test@example.com"}'
```
3. Verify OTP
```
curl -X POST http://localhost:8000/api/otp/verify-otp/ -H 'Content-Type: application/json' -d '{"email": "test", "otp": "$otp"}'

```
4. Test Protected API
```
curl -X GET http://localhost:8000/api/protected/ -H 'Authorization: Bearer $token'
```

## Note
- The OTP is stored in the database and can be used only once.
