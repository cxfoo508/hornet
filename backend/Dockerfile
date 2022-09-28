FROM python:3.9.0
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
WORKDIR /hornet-backend
COPY . /hornet-backend
RUN pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com -r requirements.txt
CMD ["python", "manage.py","runserver","0.0.0.0:8000"]
