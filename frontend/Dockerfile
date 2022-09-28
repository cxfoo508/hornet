FROM node
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
WORKDIR /hornet-forntend
COPY . /hornet-forntend
RUN npm install 
ENV NODE_OPTIONS=--openssl-legacy-provider
#CMD ["sh","start.sh"]
CMD ["npm","run","serve"]
