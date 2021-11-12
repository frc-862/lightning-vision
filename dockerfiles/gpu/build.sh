# Build GPU Docker Image

docker buildx create --name $NEW_BUILDER
docker buildx use $NEW_BUILDER
docker buildx inspect --bootstrap

docker buildx build --platform linux/amd64,linux/arm64 -t edurs0/tfod-wkspc-gpu:latest --load .
