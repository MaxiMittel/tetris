# Load Balancer

## Config

```conf
#server.conf

#Server port
port="7777"
```

## Endpoints




``POST /update``

Request the ip of a gameserver

```json
>> {
    "name": ""      //name of
}
```

```json
<< {
    "ip": "0.0.0.0",    //IP-Adress of the game server
    "port": "7777",     //Port of the game server
    "name": "EU-2"      //Name of the game server
}
```

***

``GET /api/<path>``

Forwards ``GET``request to an API server and returns the response to the client.

***

``POST /api/<path>``

Forwards ``POST``request to an API server and returns the response to the client.