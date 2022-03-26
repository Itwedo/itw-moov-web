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
$ git clone git@github.com:codeandscale/moov-proto.git
$ cd moov-proto
moov-proto$ python3 -m venv .env
moov-proto$ source .env/bin/activate
(.env)moov-proto$ pip install .
```

### Install package moov-website-x.y.z.tar.gz

```
$ mkdir moov-proto
$ cd moov-proto
moov-proto$ python3 -m venv .env
moov-proto$ source .env/bin/activate
(.env)moov-proto$ pip install moov-website-x.y.z.tar.gz
```

The package is now installed as `moov-website` in your environment and provides a management command `moov-website`

### Configuration

This app requires a configuraiton file located in `/etc/moov/config.ini` .
With the `moov-website` command, you can actually initalize this file:

```
(.env)moov-proto$ moov-website config generate
```

### Launching

Dev mode

```
(.env)moov-proto$ moov-website run
```

Production mode

```
(.env)moov-proto$ gunicorn app:app --bind 127.0.0.1:8000
```
