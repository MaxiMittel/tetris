# Load Balancer

## Config

```conf
#server.conf

#Server port
port="7777"
```

## Endpoints

``POST /register``

Register a GameServer or API server to the load balancer.

```json
>> {
    "ip": "0.0.0.0",    //IP-Adress of the server
    "port": "7777",     //Port of the server
    "name": "EU-1",     //Name of the server
    "type": "GS"        //Type of the server GS or API
}
```
```json
<< {
    "status": "success/error" 
}
```

***

``POST /usage``

Periodically update the utilization of every server.
```json
>> {
    "ip": "0.0.0.0",    //IP-Adress of the server
    "name": "EU-1",     //Name of the server
    "usage": "90"       //Some utilization metric
}
```
```json
<< {
    "status": "success/error" 
}
```

***

``GET /gameserver/allocate``

Request the ip of a gameserver

```json
<< {
    "ip": "0.0.0.0",    //IP-Adress of the game server
    "port": "7777",     //Port of the game server
    "name": "EU-2"      //Name of the game server
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

``GET /api/<path>``

Forwards ``GET``request to an API server and returns the response to the client.

***

``POST /api/<path>``

Forwards ``POST``request to an API server and returns the response to the client.