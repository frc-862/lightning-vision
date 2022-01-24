# Functions to work with docker containers

# Placeholders
IMAGE=
ARCH=
DOCKERFILE=
RUNTIME=

# Config
CONTAINER=jetson-vision
NETWORK=host
JUPYTER=8888
TENSORBOARD=6006
NETWORKTABLE=862 # not a coincidence at all

# Determine image to run
whichimage:
ifeq "$(device)" ""
	$(eval IMAGE=edurs0/tfod-wkspc:latest-onboard)
	$(eval DOCKERFILE=./dockerfiles/jetson-onboard/)
	$(eval ARCH=linux/arm64)
	$(eval RUNTIME=nvidia)
	@echo onboard
endif
ifeq "$(device)" "onboard"
	$(eval IMAGE=edurs0/tfod-wkspc:latest-onboard)
	$(eval DOCKERFILE=./dockerfiles/jetson-onboard/)
	$(eval ARCH=linux/arm64)
	$(eval RUNTIME=nvidia)
	@echo onboard
endif
ifeq "$(device)" "gpu"
	$(eval IMAGE=edurs0/tfod-wkspc:latest-gpu)
	$(eval ARCH=linux/amd64)
	$(eval DOCKERFILE=./dockerfiles/std-dev-gpu/)
	$(eval RUNTIME=runc)
	@echo gpu
endif
ifeq "$(device)" "cpu"
	$(eval IMAGE=edurs0/tfod-wkspc:latest)
	$(eval ARCH=linux/amd64)
	$(eval DOCKERFILE=./dockerfiles/std-dev/)
	$(eval RUNTIME=runc)
	@echo cpu
endif
ifeq "$(device)" "jetson"
	$(eval IMAGE=edurs0/tfod-wkspc:latest-jetson)
	$(eval DOCKERFILE=./dockerfiles/jetson-dev/)
	$(eval ARCH=linux/arm64)
	$(eval RUNTIME=nvidia)
	@echo jetson
endif
	@echo $(IMAGE)
	@echo $(DOCKERFILE)
	@echo $(ARCH)
	@echo $(RUNTIME)

# Run onboard container for robot application
onboard:
	docker run --rm -it -p $(JUPYTER):8888 -p $(TENSORBOARD):6006 -v $(shell pwd):/tensorflow/workspace --runtime $(RUNTIME) --network $(NETWORK) --name $(CONTAINER) $(IMAGE)

# Setup local runner to build for arm64, may need to run before `build`
qemu:
	docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

# Start stopped container (if exists)
resume:
	docker start -ai $(CONTAINER)

# Start a new container
run: whichimage
	docker run -it -p $(JUPYTER):8888 -p $(TENSORBOARD):6006 -v $(shell pwd):/tensorflow/workspace --runtime $(RUNTIME) --network $(NETWORK) --name $(CONTAINER) $(IMAGE)

# Shell into container
shell:
	docker exec -it $(CONTAINER) bash

# Remove containers
clean:
	docker rm $(CONTAINER)

# Remone images
purge: whichimage
	docker rmi $(IMAGE)

# Build image
build: whichimage
	docker buildx build --platform $(ARCH) -t $(IMAGE) $(DOCKERFILE)

# Build image & push to hub
deploy: whichimage
	docker buildx build --platform $(ARCH) --push -t $(IMAGE) $(DOCKERFILE)

# Push image to hub
push: whichimage
	docker push $(IMAGE)

# Pull image from hub
pull: whichimage
	docker pull $(IMAGE)

# Stops the container
stop:
	docker stop $(CONTAINER)
