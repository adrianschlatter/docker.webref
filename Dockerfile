FROM python:3.11-slim

RUN apt update

RUN useradd -ms /bin/bash webref
WORKDIR /home/webref

COPY config/requirements.txt .

RUN chown -R webref:webref .

# install web app and wsgi server:
USER root
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache ppf.webref==0.1.1

# run wsgi server:
USER webref
CMD ["waitress-serve", "--call", "ppf.webref:create_app"]
