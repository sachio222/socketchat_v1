#### seccure-cli-socketchat-python-v1
# Secure CLI Socket Chat
======
## Street name: Encryptochat

You don't need messenger. **Secure CLI Socket Chat** connects you directly to a host server that you set up. Allows you to chat with other terminals on your network, or around the world. The unencrypted server.py requires no additional libraries and is the software size equivalent of a postage stamp. It's so lightweight it will run almost anywhere, even a Raspberry Pi 1! The encrypted version is also very small, but requires the quick pip install of a Python crytograpic package, and is currently using shared key encryption (Fernet). More levels of encryption to come. 

## Features:
* Secure, client-side encryption/decryption using Fernet cipher (PGP, blowfish coming soon).
* Use it on your own LAN to chat between computers, or across the world with friends.
* Direct message or multiple chat-client connections.
* Simple usage. Just spin up server.py, and use client.py to begin chatting. 
* Secure chat: Encrypt your traffic using symmetric encryption.
* Customize max client count.
* Works out of box with Python 3.x, no libraries required (Secure chat requires addl libraries).
* Tiny filesize footprint and runs with barely any setup.
* Monitor unencrypted chats on your server.
* Audio alerts controllable with mute() or unmute().
* Exit chat with exit().

## Usage

#### No encrypt chat
1. Spin up server.py on any machine, define port number to listen on. 
2. Open server.py, connect to defined port.
3. Chat.

#### Encrypted chat
1. Spin up server.py same as above. 
2. Run keygen-fernet.py to generate secret.key
3. Share this SAME secret.key with any person you want to be able to read your messages, and have them place it in their socketchat folder.
4. Open server.py, connect to defined port. 
5. Chat.

## Contributors
J. Krajewski

### Third party libraries
https://pypi.org/project/cryptography/

## License 
* see [LICENSE](https://github.com/username/sw-name/blob/master/LICENSE.md) file

## Version 
* Version 1.0

## How-to use this code

## Contact
#### Developer/Company

* Twitter: [@jakekrajewski](https://twitter.com/jakekrajewski "@jakekrajewski")
* Medium: [@Jakekrajewski](https://medium.com/@Jakekrajewski)
