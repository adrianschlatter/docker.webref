# docker.webref

docker.webref packs [ppf.webref](https://github.com/adrianschlatter/ppf.webref)
into a Docker container. `ppf.webref` is a web interface to your JabRef
database (see [ppf.webref](https://github.com/adrianschlatter/ppf.webref) for
details).

Create a JabRef database (using your normal JabRef) and configure
`docker.webref` to point to this database. Voila: Your references just became
accessible worldwide.

Note: `ppf.webref` and therefore `docker.webref` provides *read-only* access to
your library. To add, edit, or delete entries from your library, you still need
a standard JabRef installation somewhere.

<p align="middle">
<img alt="Screenshot" src="imgs/webref_screenshot.png" height=180>
</p>


# Installation

You need:

* JabRef: To create, edit, and extend your library
* Docker: To create and run docker images


Steps:

* Clone this repo
* Create a suitable docker-compose.yml (use
  [docker-compose_templ.yml](../docker-compose_templ.yml) as a starting point)
* run (in the directory of your `docker-compose.yml`
```shell
make
```
* generate a secret_key for you web app (required to encrypt cookies):
 ```shell
 python -c 'import secrets; print(secrets.token_hex())'
 ```
* Create the following text files (assuming you did not change the paths
  from the template docker-compose.yml):
  - ./secrets/sqlserver: The sql server holding your JabRef database
  - ./secrets/sqldatabasename: The name of your JabRef database 
  - ./secrets/sqlusername: Username used to access your JabRef database
  - ./secrets/sqlpassword: Password for that username
  - ./secrets/secret_key: Your secret key generated above
* Run
```make up```
* Point your webbrowser to localhost:7000 (or where you configured your
  `docker.webref` to be)

This will start the `docker.webref` container on your local machine which is
nice for testing. To get the most out of `docker.webref`, you will probably
want to run this docker container on a web server.

The website will present a login form. However, as we have not created any
users yet, we can't login. We have to create a user first. This is currently a
bit awkward - don't complain, have a look at the version number, instead. Begin
by starting a shell inside your running docker container:

```shell
docker exec -it <container_id> '/bin/bash'
```

(Find your container_id using ```docker container ls```.) Then, inside that
shell, run:

```shell
flask --app ppf.webref useradd <username>
```

This will:

* create a table 'user' in your db if it does not exist yet
* register user <username> in user table

To set a password for this new user or to change the password of an existing
user, do

```shell
flask --app ppf.webref passwd <username>
```

which will ask for and store (a salted hash of) the password in the
user table. To get out of the container-shell, type <Ctrl-D>.

Now we are able to log in.


# Still reading?

If you read this far, you're probably not here for the first time. If you use
and like this project, would you consider giving it a Github Star? (The button
is at the top of this website.) If not, maybe you're interested in one of my
[my other
projects](https://github.com/adrianschlatter/ppf.sample/blob/develop/docs/list_of_projects.md)?


# Contributing

Did you find a bug and would like to report it? Or maybe you've fixed it
already or want to help fixing it? That's great! Please read
[CONTRIBUTING](./CONTRIBUTING.md) to learn how to proceed.

To help ascertain that contributing to this project is a pleasant experience,
we have established a [code of conduct](./CODE_OF_CONDUCT.md). You can expect
everyone to adhere to it, just make sure you do as well.


# Changelog

* 0.1: Dockerizes `ppf.webref-0.1.1`.
