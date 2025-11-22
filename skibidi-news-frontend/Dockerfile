FROM node:20-alpine

WORKDIR /app
ENV HTTP_PROXY=http://fihel1d-proxy.emea.nsn-net.net:8080
ENV HTTPS_PROXY=http://fihel1d-proxy.emea.nsn-net.net:8080
ENV NO_PROXY=localhost,127.0.0.1
ENV http_proxy=http://fihel1d-proxy.emea.nsn-net.net:8080
ENV https_proxy=http://fihel1d-proxy.emea.nsn-net.net:8080
ENV no_proxy=localhost,127.0.0.1

COPY package.json .
COPY package-lock.json .

RUN npm install

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]