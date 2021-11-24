# Build Jetson Docker Image

# docker buildx create --name $NEW_BUILDER
# docker buildx use $NEW_BUILDER
# docker buildx inspect --bootstrap

docker buildx build --platform linux/arm64 -t edurs0/tfod-wkspc:latest-jetson --push .
