FROM ghcr.io/maxherbs/jekyll-base:latest



COPY myblog /myblog
COPY build.sh /myblog/build.sh
WORKDIR /myblog


RUN chmod +x build.sh
RUN bash /myblog/build.sh

CMD ["apachectl", "-D", "FOREGROUND"]