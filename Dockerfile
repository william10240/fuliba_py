FROM python

LABEL maintainer="williamyan1024@gmail.com"

RUN pip install --no-cache-dir --upgrade --ignore-installed -i https://mirrors.aliyun.com/pypi/simple/ \
	pyquery
	# peewee

CMD ["python3"]

## docker run -d --name fuli -v/data/git/fuliimg_py:/app fuli python /app/app.py