FROM ghcr.io/maxherbs/jekyll-base:latest

COPY myblog /blog
COPY build.sh /blog
WORKDIR /blog

RUN chmod +x build.sh
RUN ./build.sh

CMD ["apachectl", "-D", "FOREGROUND"]