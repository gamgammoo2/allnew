#syntax=docker/dockerfile:1
FROM docker
COPY --from=docker/buildx-bin buildx /usr/libexec/docker/cli-plugins/docker-buildx
RUN docker buildx version
