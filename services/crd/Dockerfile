FROM bitnami/kubectl:1.26
ARG TARGETOS
ARG TARGETARCH

ADD --chmod=755 https://github.com/hairyhenderson/gomplate/releases/download/v3.11.5/gomplate_${TARGETOS}-${TARGETARCH} /usr/local/bin/gomplate
ADD ./manifests /acorn/manifests
ADD ./scripts /acorn/scripts


CMD ["/bin/bash", "-c", "kubectl apply -f /acorn/manifests/*.yaml"]