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

`POST /account/update`  //TODO FIX

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

`POST /account/postgamescore` //TODO FIX

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
    "query": "username" 
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

`GET /user/<id>`

Get user informations by their id.

```json
<< {
    "id": "",
    "username": "",
    "stats": {}
}
```

***

``GET /sessions/list``

Get list of all gamesessions

```json
<< {
    "status": "success/error",
    "sessions": [{
        "_id": "1334ssg45", //code
        "ip": "0.0.0.0",    //IP-Adress of the hosting game server
        "port": "7777",     //Port of the hosting game server
        "name": "EU-2"      //Name of
    }]
    }
```

***

``POST /sessions/allocate``

Allocates for a new gamesession

```json
>> {
    "name": ""      //name of
}
```

```json
<< {
    "_id": "1334ssg45",   //code
    "status": "success/error",
    "error": "error/empty"
}
```

***

``GET /sessions/get/<id>``

Get session by its uniqe id

```json
<< {
    "status": "success/error",
    "ip": "0.0.0.0",    //IP-Adress of the hosting game server
    "port": "7777",     //Port of the hosting game server
}
```

***

``POST /sessions/delete``

Delete 

```json
>> {
    "_id": "",      //code
    "ip": "",  
    "port": ""   
}
```

```json
<< {
    "status": "success/error",
    "error": "error/empty"
}
```

***

``POST sessions/migrate``

```json
>> {
    "_id": "",         //code
    "name": ""   
}
```

```json
<< {
    "status": "success/error",
    "error": "error/empty",
    "ip": "0.0.0.0",            //IP-Adress of the hosting game server
    "port": "7777"              //Port of the hosting game server
}
```

***
