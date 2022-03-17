# moov-proto

Prototype du nouveau portail Moov.

Utilise l'API REST du CMS https://github.com/codeandscale/moov-cms (powered by Strapi)

## Installation & Configuration

Cette application est prévue pour être installée sur un système type GNU/Linux | Unix

### Pré-requis

* python3
* python3-venv

### Installation via git

Clonez, et configurez

```
$ git clone git@github.com:codeandscale/moov-proto.git
$ cd moov-proto
moov-proto$ python3 -m venv .env
moov-proto$ source .env/bin/activate
(.env)moov-proto$ pip install .
```

### Installation via le paquet moov-website-x.y.z.tar.gz

```
$ mkdir moov-proto
$ cd moov-proto
moov-proto$ python3 -m venv .env
moov-proto$ source .env/bin/activate
(.env)moov-proto$ pip install moov-website-x.y.z.tar.gz
```

Le paquet est installé dans votre environnement virtuel sous le nom `moov-website` et propose une commande `moov`

### Configuration

L'application requiert un fichier de config situé dans  `/etc/moov-website/config.ini` .
Avec la commande `moov` vous pouvez initialiser ce fichier:

```
(.env)moov-proto$ moov config generate
```

### Lancement

L'application propose un serveur HTTP de développement, accessible via:

```
(.env)moov-proto$ moov run
```
