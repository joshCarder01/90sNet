
all: output_image

.PHONY: docker_image
docker_image:
	docker build -t web-app:local .

.PHONY: output_image
output_image:
	docker save -o ../image_files/web_app_image.tar

clean:
	rm -f ../image_files/web_app_image.tar