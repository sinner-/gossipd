# gossipd

Python implementation of `gossipd`.

Care has been taken to avoid external dependencies where possible, however `PyTomCrypt` (and underlying `libtomcrypt`) has been chosen for RSA capability.

Developed using Python 3.5.3, also tested on Python 2.7.13.

This software is still in very early stages of development.

## Setup

It's recommended (but not required) to use `virtualenv` and `virtualenvwrapper` to avoid conflicting with system python libraries. This document assumes `virtualenvwrapper` is installed and `virtualenvwrapper.sh` has been sourced into the environment.

```
$ git clone https://github.com/sinner-/gossipd
$ mkvirtualenv gossipd
$ cd gossipd
$ pip install .
$ #Verify installation.
$ which gossipd
$ which gossipc
```


## Usage
### gossipd

`gossipd` reads its configuration from environment variables. An example `gossipdrc` file is provided with the following contents.:
```
export GOSSIPD_DB_PATH='/tmp/sina.db'
export GOSSIPD_LISTEN_IP='127.0.0.1'
export GOSSIPD_LISTEN_PORT=5555
export GOSSIPD_USERNAME=sina
```

You can run multiple gossipd instances on the same host as long as the `GOSSIPD_DB_PATH`, `GOSSIPD_LISTEN_PORT` and `GOSSIPD_USERNAME` are unique for each instance.

`gossipd` runs two independent processes, a daemon and a worker.

The daemon listens for incoming connections from other `gossipd` peers and the worker runs an action loop of the following tasks:
 * Fetch messages from peers in peer list.
 * Generate RSA keys (marking some as bogus).
 * NOT IMPLEMENTED YET: Send bogus challenge strings to peers.
 * Sleeps.

#### Start gossipd:
```
$ gossipd
```

You should see output like this:
```
Sleeping for 5 seconds.
Sleeping for 5 seconds.
Sleeping for 5 seconds.
Generating an RSA key.
Sleeping for 5 seconds.
Fetching messages from peers.
```

On first start, please wait for a while (5 minutes should be sufficient) before you attempt to add any peers, as `gossipd` will need to generate RSA keys.

#### Exit gossipd:
`gossipd` responds to keyboard interrupt, Ctrl-C will exit both daemon and worker processes.

### gossipc

`gossipc` is a crude client for interfacing with the gossipd DB. It depends on `GOSSIPD_DB_PATH` being set.

Full functionality of `gossipc` can be examined by invoking `gossipc --help`:
```
$ gossipc --help
usage: gossipc [-h] [-a] [-P] [-d] [-s] [-g] [-n NAME] [-H HOST] [-p PORT]
               [-k PUBKEY_FILE] [-S SOURCE] [-m MESSAGE]

optional arguments:
  -h, --help            show this help message and exit
  -a, --add-peer
  -P, --set-peer-key
  -d, --delete-peer
  -s, --send-message
  -g, --view-messages
  -n NAME, --name NAME
  -H HOST, --host HOST
  -p PORT, --port PORT
  -k PUBKEY_FILE, --pubkey-file PUBKEY_FILE
  -S SOURCE, --source SOURCE
  -m MESSAGE, --message MESSAGE
```

#### Add a peer
`gossipc --add-peer --name alice --host 100.100.100.100 --port 5555`

When you add a peer to the peer list, `gossipc` will also assign one of the unused and available RSA keypairs for communication with that peer and then present the public key for you to provide to that peer. 
e.g.
```
$ gossipc --add-peer --name alice --host 127.0.0.1 --port 5556
Exchange key:
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCkvAwE6zGxlfSNCLHnwGRi4HYgskEVfRxqxTibGM
DCOJ3Jpye4SayMsBHz8pTQhjNopuHd9aGJ5tU1C94f0P3/fzqXdFHulZZXCNfkd24hdkSkiE9oN451
nBOf+47vR7YAmxt/emFFUoG0Hgnhr5bPzeb2zSWBps8zDhxsL12vVQIDAQAB
-----END PUBLIC KEY-----
```
The peer will run a similar command and be furnished with a public key that they should provide to you, per below.

#### Set peer key
`gossipc --set-peer-key --name alice --pubkey-file /tmp/alice.pub`

When a peer has added you to their peer list, they will need to provide you with a public key before `gossipd` will attempt to fetch messages from them. You can write the public key block to a temporary file and read it in.

#### Broadcast messages
`gossipc --send-message --source bob --message "hello world"`

There is currently no restriction on message size or who you claim to be when you send a message.

### View messages
`gossipc --view-messages`

You can view all the messages gossipc has stored with this command.
```
$ gossipc -g
2017-06-26 14:18:55|delivered_by:node1|sender:poophead|wassuppppppp
2017-06-26 14:18:55|delivered_by:node1|sender:alice|omg how much
```
