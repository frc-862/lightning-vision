# Functions to work with docker containers

# Config
IMAGE=edurs0/tfod-wkspc:latest-jetson
TEST_IMAGE=edurs0/tfod-wkspc:latest-test
CONTAINER=tfod-trainer
NETWORK=host
RUNTIME=nvidia
JUPYTER=8888
TENSORBOARD=6006

# Setup local runner to build for arm64
# may need to run before `build`
qemu:
	docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

# Start stopped container (if exists)
resume:
	docker start -ai $(CONTAINER)

# Start a new container
run:
	docker run -it -p $(JUPYTER):8888 -p $(TENSORBOARD):6006 -v $(shell pwd):/tensorflow/workspace --runtime $(RUNTIME) --network $(NETWORK) --name $(CONTAINER) $(IMAGE)

# Start a new test container
run-test:
	docker run -it -p $(JUPYTER):8888 -p $(TENSORBOARD):6006 -v $(shell pwd):/tensorflow/workspace --runtime $(RUNTIME) --network $(NETWORK) --name $(CONTAINER) $(TEST_IMAGE)

# Shell into container
shell:
	docker exec -it $(CONTAINER) bash

# Remove containers
clean:
	docker rm $(CONTAINER)

# Remone images
purge:
	docker rmi $(IMAGE)
	docker rmi $(TEST_IMAGE)

# Build image
build:
	docker buildx build --platform linux/arm64 -t $(IMAGE) ./dockerfiles/

# Build testing image
build-test:
	docker buildx build --platform linux/amd64 -t $(TEST_IMAGE) ./dockerfiles/test/

# Build image & push to hub
deploy:
	docker buildx build --platform linux/arm64 --push -t $(IMAGE) ./dockerfiles/

# Build image & push to hub
deploy-test:
	docker buildx build --platform linux/amd64 --push -t $(TEST_IMAGE) ./dockerfiles/test/

# Push image to hub
push:
	docker push $(IMAGE)

# Pull image from hub
pull:
	docker pull $(IMAGE)

# Push test image to hub
push-test:
	docker push $(TEST_IMAGE)

# Pull test image from hub
pull-test:
	docker pull $(TEST_IMAGE)

# Stops the container
stop:
	docker stop $(CONTAINER)

