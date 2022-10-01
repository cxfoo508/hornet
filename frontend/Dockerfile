FROM node
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
WORKDIR /hornet-frontend
COPY . /hornet-frontend
RUN npm install
ENV  NODE_OPTIONS=--openssl-legacy-provider
CMD ["npm", "run","serve"]
