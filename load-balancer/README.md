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

``GET /api/<path>``

Forwards ``GET``request to an API server and returns the response to the client.

***

``POST /api/<path>``

Forwards ``POST``request to an API server and returns the response to the client.