FROM ghcr.io/maxherbs/jekyll-base:latest as developer

COPY myblog /myblog
COPY build.sh /myblog/build.sh
WORKDIR /myblog

RUN bash /myblog/build.sh

RUN sed -i 's/Listen 80/Listen 5000/' /etc/apache2/ports.conf
CMD ["apachectl", "-D", "FOREGROUND"]



FROM docker.io/httpd:2.4-alpine as runtime
EXPOSE 80
EXPOSE 443
COPY --from=developer /myblog/_site /var/www/html/
CMD ["apachectl", "-D", "FOREGROUND"]

