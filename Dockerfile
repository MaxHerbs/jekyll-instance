FROM ghcr.io/maxherbs/jekyll-base:latest

COPY myblog /myblog
WORKDIR /myblog

RUN chmod +x build.sh
RUN bash /myblog/build.sh

CMD ["apachectl", "-D", "FOREGROUND"]