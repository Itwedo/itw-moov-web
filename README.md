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

This app requires a configuraiton file located in `/opt/moov/moov-web.conf` .
With the `moov` command, you can actually initalize this file:

```
(.env)moov$ moov config generate
```
### Packaging

Good ol' python packaging vibes !

You should simply bump the version in `setup.cfg` and run:

```
(.env)moov$ python -m build
```

It will then create a folder `dist` with `moov-web-x.y.z.tar.gz` in it.

That same package will be fully installable in another environment as such:

```
(other-env)$ pip install moov-web-x.y.z.tar.gz
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
