# Directory Service

## Config

```conf
#server.conf

#Server port
port="7777"
```

## Endpoints

***

``POST /directory-service/register``

Register a game/api/lb server to the directory service.

```json
>> {
    "ip": "0.0.0.0",    //IP-Adress of the server
    "port": "7777",     //Port of the server
    "name": "EU-1/API-1/LB-1",     //Name of the server
    "type": "GS/API/LB"        //Type of the server GS or API
}
```
```json
<< {
    "status": "success/error" 
}
```
***

``DELETE /directory-service/unregister/<id>``

Unregister a game/api/lb server from the directory service.

http://serverip/directory-service/unregister/{EU-1, API-1, LB-1}

```json
<< {
    "status": "success/error" 
}
```
***

``GET /directory-service/get{game,api,lb}Server``

Request the data of all registered game/api/lb servers

```json
<< servers: [{
    "ip": "0.0.0.0",    //IP-Adress of the game server
    "port": "7777",     //Port of the game server
    "name": "EU-1/API-1/LB-1"      //Name of the game server
}, 
{
   "ip": "0.0.0.0",    //IP-Adress of the game server
    "port": "7777",     //Port of the game server
    "name": "EU-2/API-2/LB-2"     
}]
```

***
