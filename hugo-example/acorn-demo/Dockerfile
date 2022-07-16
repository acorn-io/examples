FROM klakegg/hugo:0.101.0-alpine AS hugo

ADD . /src
WORKDIR /src
RUN mkdir -p /target && \
    hugo -d /target/ --minify

FROM nginx AS prod
COPY --from=hugo /target /usr/share/nginx/html

FROM hugo AS dev
EXPOSE 1313
CMD [ "server", "--bind", "0.0.0.0", "-D" ]
