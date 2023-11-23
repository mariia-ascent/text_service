
docker: 
	cd ../.. ; docker build -t eopti/text_service -f ./services/text_service/Dockerfile ./

webdock_push:
	docker image tag eopti/text_service momoware.vps.webdock.cloud:443/eopti/text_service
	docker push momoware.vps.webdock.cloud:443/eopti/text_service
