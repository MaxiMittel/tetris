# Rest API

## Config

```conf
#server.conf

#Ip-Adress/port of the load balancer
balancerIP="0.0.0.0"
balancerPort="7777"

#Server name/port
name="EU-2"
port="7777"
```

## Endpoints

`POST /account/signup`

Sign up a new user.

```json
>> {
    "username": "",
    "password": "",
    "mail": "",
}
```

```json
<< {
    "status": "success/error",
    "error": "error/empty",     //Some login error
    "auth": "8fmnfuojgahknldj", //JWT for authentication
    "username": ""              //Username
}
```

---

`POST /account/signin`

Sign in.

```json
>> {
    "username": "",
    "password": "",
}
```

```json
<< {
    "status": "success/error",
    "error": "error/empty",     //Some login error
    "auth": "8fmnfuojgahknldj", //JWT for authentication
    "username": ""              //Username
}
```

---

`GET /account/get`

Returns the account informations of the logged in user.

```json
>> {
    "auth": "8fmnfuojgahknldj",   //Json Web Token
}
```

```json
<< {
    "status": "success/error",
    "error": "error/empty",
    "username": "",     //Username
    "stats": {}         //Game stats
}
```

---

`POST /account/update`

Updates the current user.

```json
>> {
    "auth": "8fmnfuojgahknldj",   //Json Web Token
    "username": "",               //Username
}
```

```json
<< {
    "status": "success/error",
    "error": "error/empty",
    "username": "",             //Username
    "auth": "8fmnfuojgahknldj", //Json Web Token
}
```

---

`POST /account/postgamescore`

Post the result of one game

```json
>> {
    "auth": "",          //Authentication of user
    "gamescore": {}      //Game stats = {"score": score, "bpm": bpm, "date": date}
}
```

```json
<< {
    "status": "success/error",
    "error": "error/empty
}
```

---

`POST /user/search`

Search for other users.

```json
>> {
    "query": ["username1", "username2", "username3"]     //Search query
}
```

```json
<< {
    "users": [
        {
            "id": "",
            "username": "",
            "stats": {}
        },
        {
            "id": "",
            "username": "",
            "stats": {}
        }
    ]
}
```

---

`GET /user?id=<id>`

Get user informations by their id.

```json
<< {
    "id": "",
    "username": "",
    "stats": {}
}
```
