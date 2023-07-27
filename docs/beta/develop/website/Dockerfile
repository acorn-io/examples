FROM klakegg/hugo:0.111.3-alpine

ADD ./ /src
WORKDIR /src

EXPOSE 1313
CMD [ "server", "--bind", "0.0.0.0", "-D" ]
