build:
	docker build -t centos .
run:
	docker run -dit --name centos centos
history:
	docker history centos
ps:
	docker ps -a
img:
	docker images
rm:
	docker rm -f $$(docker ps -aq)

rmi:
	docker rmi $$(docker images -q)
