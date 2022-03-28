# moov-proto

Prototype for the brand new moov.mg portal.

This application is using Flask and consuming the Strapi CMS REST API (https://github.com/codeandscale/moov-cms)

## Installation & Configuration

This app is intended to be installed on a GNU/Linux | Unix system

### Pre-requisites

* python3
* python3-venv

### Installation via git

Clone and configure

```
$ mkdir moov
$ cd moov
moov$ git clone git@github.com:codeandscale/moov-proto.git .
moov$ python3 -m venv .env
moov$ source .env/bin/activate
(.env)moov$ pip install .
```

### Install package moov-x.y.z.tar.gz

```
$ mkdir moov
$ cd moov
moov$ python3 -m venv .env
moov$ source .env/bin/activate
(.env)moov$ pip install moov-x.y.z.tar.gz
```

The package is now installed as `moov` in your environment and provides a management command `moov`

### Configuration

This app requires a configuraiton file located in `/etc/moov/config.ini` .
With the `moov` command, you can actually initalize this file:

```
(.env)moov$ moov config generate
```

### Launching

Dev mode

```
(.env)moov$ moov run
```

Production mode

```
(.env)moov$ gunicorn app:app --bind 127.0.0.1:8000
```
