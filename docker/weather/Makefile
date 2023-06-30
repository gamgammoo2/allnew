all: build run k8sinit appdep appsvc getdep getsvc getpod
k8srestart: delsvc deldep appdep appsvc getdep getsvc getpod

build:
	docker build -t weather .
run:
	docker run -it -d -p 8000:8000 -v /allnew/node:/app --name weather weather
exec:
	docker exec -it weather /bin/bash
logs:
	docker logs weather
ps:
	docker ps -a
img:
	docker images
rm:
	docker rm -f $$(docker ps -aq)
rmi:
	docker rmi $$(docker images -q)
k8sinit:
	docker commit weather weather-msa
	docker tag weather gamgammoo/weather-msa
	docker push gamgammoo/weather-msa
	docker rm -f $$(docker ps -aq)
	docker rmi gamgammoo/weather-msa
	docker rmi $$(docker images -q)
appdep:
	kubectl apply -f deployment.yaml
appsvc:
	kubectl apply -f service.yaml
getdep:
	kubectl get deployment
getsvc:
	kubectl get svc -o wide
getpod:
	kubectl get pod -o wide
delsvc:
	kubectl delete svc weather-msa
deldep:
	kubectl delete deployment weather-msa
