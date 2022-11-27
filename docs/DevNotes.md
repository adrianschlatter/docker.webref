# Development Notes

## Docker Lessons

* Webserver must listen on 0.0.0.0:80: Docker port mapping does not work
  otherwise (127.0.0.1:80 is not enough).
* Running apache in the foreground (as it's usually done inside a docker
  container) has unexpected consequences: Apache reacts to SIGWINCH
  (WINdow CHange SIGnal) by restarting. Therefore, resizing the terminal
  stops the container...


## Deployment to a Synology NAS

Build docker image:

```
docker build -t webref:0.x .
```

Then, save this image into a tar-ball:

```
docker save webref:0.x | gzip > webref-0.x.tar.gz
```

Copy this to your NAS where you run:

```
docker load < webref-0.x.tar.gz
```

Stop your existing webref container and delete it using the commands:

```
docker container ls
docker container stop <hexcode>
docker container rm <hexcode>
```

Go into your directory with your docker-compose.yml and run (maybe after
changing the version number inside docker-compose.yml):

```
docker-compose up --detach
```

We want https://www.ourdomain.com/references to be handled by the webref
docker container => need reverse proxy. Synology's webinterface is not
flexible enough: It can't redirect a subdirectory to a separate webserver.
It is still possible, however, but you have to go via a terminal:
[This article](https://primalcortex.wordpress.com/2018/05/07/synology-reverse-proxy-revisited-again/?unapproved=18819&moderation-hash=e368f1dda03465bca9880d8de938786a#comment-18819) is 
useful. The config we put in '/etc/nginx/conf.d/www.webref.conf' is:

```
location ^~ /references/ {
	proxy_pass http://127.0.0.1:7000/;
}
```

This assumes your webref container has mapped internal port 80 to host port
7000. Make sure you do not forget the slash ("/") in ":7000/". If you 
don't put it there, https://www.ourdomain.com/references maps to
http://127.0.0.1:7000/references instead of http://127.0.0.1:7000/. 

Make sure to run

```nginx -s reload```

to activate your new configuration


## Ugly

* Docker image httpd:2.4 has apache in /usr/local/apache2. But apt installs
  additional apache modules (mod_wsgi) in /usr/lib/apache2.
