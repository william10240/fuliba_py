# 此版本暂停更新,请使用golang版本
# 福利吧(https://fuliba2020.net) 福利汇总图片下载器

[Golang 版本](https://github.com/williamyan1024/fuliimg_go),  [NodeJs 版本](https://github.com/williamyan1024/fuliimg_js)

## 说明
- ~~保存2019年来福利汇总第二页的图片~~
- 福吧只显示最新7页的内容,所以只能保存最新的
- 每小时自动下载一遍,省事省心省力
- 如果网络不好,等网络好的时候会自动下载


## 自定义 图片存放路径

## 1.如果使用Docker-compose部署
修改 docker-compose.yml
将 "/data/dcdb/fuliimages:/app/images" 修改为 yourimagepath:/app/images

## 2. 如果直接使用python运行的
图片会保存在与本项目同级的fuliimages中
如需修改请修改 app.py 中
"IMG_PATH = os.path.join(os.path.dirname(APP_PATH), "fuliimages")

