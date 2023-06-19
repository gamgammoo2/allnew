build:
	docker build -t cmd .
run:
	docker run -it -d -p 8000:80 cmd
ps:
	docker ps -a
img:
	docker images
rm:
	docker rm -f $$(docker ps -aq)

rmi:
	docker rmi $$(docker images -q)
