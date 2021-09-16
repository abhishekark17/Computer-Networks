# Multi-Person Chat Room
The code consists of two parts<br>
- client Side
- Server Side
  
## Server side
- run `python3 server.py --n **Maximum number of cients** --Port **PORT**`
- Port default = 1234
- Default n=10

## Client Side
- run `python3 client.py --Server **ServerName** --username **UserName** --Port **PORT**`
- If the username is already exists break the connection and join again

Once the client receives **ERROR 103** it must disconnect(CTRL+C) and connect again to the server as a fresh connection

### Message Format
The message must be typed in the following format<br>
- `@[username]: [message]`
- The recipient will receive message in the format `@[sendername]: [message]`

If 