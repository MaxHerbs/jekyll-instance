FROM ghcr.io/maxherbs/jekyll-base:latest as DEVELOPER

COPY myblog /myblog
COPY build.sh /myblog/build.sh
WORKDIR /myblog

RUN bash /myblog/build.sh

CMD ["apachectl", "-D", "FOREGROUND"]



FROM docker.io/httpd:2.4-alpine as RUNTIME
EXPOSE 80
EXPOSE 443
COPY --from=DEVELOPER /myblog/_site /var/www/html/
CMD ["apachectl", "-D", "FOREGROUND"]

