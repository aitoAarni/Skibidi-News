FROM node:20-alpine

WORKDIR /app

COPY package.json .
COPY package-lock.json .

ENV HTTP_PROXY=http://fihel1d-proxy.emea.nsn-net.net:8080 \
    HTTPS_PROXY=http://fihel1d-proxy.emea.nsn-net.net:8080 \
    NO_PROXY=localhost,127.0.0.1,mcp_router_agent,mcp_humorizer,mcp_news_aggr,mcp_prompt_opt,mcp_text_to_audio,skibidinews_appnet,*.local,172.23.0.0/16 \
    http_proxy=http://fihel1d-proxy.emea.nsn-net.net:8080 \
    https_proxy=http://fihel1d-proxy.emea.nsn-net.net:8080 \
    no_proxy=localhost,127.0.0.1,mcp_router_agent,mcp_humorizer,mcp_news_aggr,mcp_prompt_opt,mcp_text_to_audio,skibidinews_appnet,*.local,172.23.0.0/16

RUN npm install

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]