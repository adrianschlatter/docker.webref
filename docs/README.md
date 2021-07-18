# WebRef

WebRef is a web interface to a [JabRef SQL database](https://docs.jabref.org/collaborative-work/sqldatabase).
It allows you to access your references from anywhere in the world and from
any device with a web browser. You do not need to install Java, you
do not need to install an app. Any non-archaic phone, tablet, PC, Mac, or
Raspberry Pi will do.

Create a JabRef database (using your normal JabRef) and configure WebRef 
to point to this database. Voila: Your references just became accessible
worldwide.

Note: WebRef provides *read-only* access to your library. To add, edit, or
delete entries from your library, you still need a standard JabRef installation
somewhere.

<p align="middle">
<img alt="Screenshot" src="imgs/webref_screenshot.png" height=180>
</p>


## Installation

You need:

* JabRef: To create, edit, and extend your library
* Docker: To create and run docker images


Steps:

* Clone this repo
* Create a suitable docker-compose.yml (use
  [docker-compose_templ.yml](../docker-compose_templ.yml) as a starting point)
* Create the following text files (assuming you did not change the paths
  from the template docker-compose.yml):
  - ./secrets/sqlusername: Username used to access your JabRef database
  - ./secrets/sqlpassword: Password for that username
  - ./secrets/sqlserver: The sql server holding your JabRef database
  - ./secrets/sqldatabasename: The name of your JabRef database 
* Run ```docker-compose up```
* Point your webbrowser to localhost:7000 (or where you configured your
  WebRef to be)


This will start WebRef on your local machine which is nice for testing.
To get the most out of WebRef, you will probably want to
run this docker image on a web server.
