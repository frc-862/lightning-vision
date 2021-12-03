# Functions to work with docker containers

# Config
IMAGE=edurs0/tfod-wkspc:latest-jetson
CONTAINER=tfod-trainer
NETWORK=host
RUNTIME=nvidia
LOCAL_JUPYTER_PORT=8888
LOCAL_TENSORBOARD_PORT=6006

# Setup local runner to build for arm64
# may need to run before `build`
qemu:
	docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

# Start stopped container (if exists)
resume:
	docker start -ai $(CONTAINER)

run:
	docker run -it -p $(LOCAL_JUPYTER_PORT):8888 -p $(LOCAL_TENSORBOARD_PORT):6006 -v $(shell pwd):/tensorflow/workspace --runtime $(RUNTIME) --network $(NETWORK) --name $(CONTAINER) $(IMAGE)

# Shell into container
shell:
	docker exec -it $(CONTAINER) bash

# Remove containers
clean:
	docker rm $(CONTAINER)

# Remone images
purge:
	docker rmi $(IMAGE)

# Build image
build:
	docker buildx build --platform linux/arm64 -t $(IMAGE) ./dockerfiles/jetson-dev

# Build image & push to hub
deploy:
	docker buildx build --platform linux/arm64 --push -t $(IMAGE) ./dockerfiles/jetson-dev

# Push image to hub
push:
	docker push $(IMAGE)
        
# Pull image from hub
pull:
	docker pull $(IMAGE)
	