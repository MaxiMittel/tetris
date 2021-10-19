# Load Balancer

## Config

```conf
#server.conf

#Server port
port="7777"
```

## Endpoints

***

``POST /directory-service/register``

Register a GameServer server to the directory service.

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

``DELETE /directory-service/unregister/<id>``

Unregister a game server from the directory service.

```json
>> {
    "ip": "0.0.0.0",    //IP-Adress of the server
    "port": "7777",     //Port of the server
    "name": "EU-1",     //Name of the server
}
```
```json
<< {
    "status": "success/error" 
}
```
***

``GET /directory-service/getServer``

Request the data of all registered game servers

```json
<< servers: [{
    "ip": "0.0.0.0",    //IP-Adress of the game server
    "port": "7777",     //Port of the game server
    "name": "EU-1"      //Name of the game server
}, 
{
   "ip": "0.0.0.0",    //IP-Adress of the game server
    "port": "7777",     //Port of the game server
    "name": "EU-2"     
}]
```

***