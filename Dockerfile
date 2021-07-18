FROM httpd:2.4
RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y libapache2-mod-wsgi-py3
RUN pip3 install flask-sqlalchemy
RUN pip3 install pymysql
RUN pip3 install ppf.jabref==0.1.0
RUN mkdir /var/run/apache2      # needed to store files for WSGI
RUN mkdir /var/www              # home of www-data user
COPY static/ /webapp/static
COPY templates/ /webapp/templates
COPY webref.py /webapp
COPY config/webref.wsgi /webapp
COPY config/httpd.conf /usr/local/apache2/conf
WORKDIR /webapp
CMD ["/usr/local/apache2/bin/httpd", "-D", "FOREGROUND"]
