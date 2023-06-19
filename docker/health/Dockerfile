#step 1 : base images
From ubuntu:latest

#step 2 :Install packages
RUN apt -y update && apt -y upgrade && apt -y install nginx && apt -y install curl
RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf

#step 3:
COPY index.html /var/www/html

#step 4:
HEALTHCHECK --interval=10s --timeout=3s CMD curl -f http://localhost/ || exit 1

#step 5:
CMD ["nginx"]

