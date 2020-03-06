# XJCraft Apply
小鸡服新玩家申请处理

## 食用说明
### 后端
1. 安装`Python3`和`pip3`
2. 首次使用执行下面的代码安装依赖

    ```shell script
    pip3 install flask
    pip3 install DBUtils
    ```
3. 执行下面的代码启动
    ```shell script
    ./app.py
    ```

#### 从 Sqlite 切换至 MySQL
1. 安装`mysql`驱动

    ```shell script
    pip3 install ???  # 咕咕咕 TODO
    ```
2. 调整`db.py`开头的代码，改为`mysql`的配置，参考如下：

    ```python
    import ???  # 咕咕咕 TODO


    df_pool = PooledDB(
        ???,  # 咕咕咕 TODO
        mincached=1,
        maxcached=10,
        blocking=True,
        host="127.0.0.1",
        port=3306,
        db="mc",
        user="root",
        passwd="123456",
        charset="utf8"
    )
    ```

### 前端
> 推荐使用`yarn`，如希望使用`npm`，请自行变通一下指令
>
> 操作均在 ui 目录中进行
>
> 目前不建议在`Windows`开发，环境配置非常麻烦(主要是`node-sass`)

1. 安装`NodeJS`
2. 安装全局依赖

    ```shell script
    npm i -g yarn
    yarn global add @vue/cli
    ```
3. 安装依赖

    ```shell script
    yarn
    ```
4. 调试运行

    ```shell script
    yarn run dev
    ```
4. 生成构建文件

    ```shell script
    yarn run build:prod
    ```
   
   构建结果会生成在 dist 目录中

### 反代(Nginx 为栗子
#### 开发参考配置
```
server {
    listen       8843;

    location / {
        proxy_pass http://127.0.0.1:9527;
        proxy_set_header Host $host;
        proxy_set_header X-Real-Ip $remote_addr;
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forward-Proto $schema;
    }

    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-Ip $remote_addr;
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forward-Proto $schema;
    }
}
```

#### 产品参考配置
```
server {
    listen       8843;

    root /var/www/xjapply;  # 前端打包结果的存放路径

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-Ip $remote_addr;
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forward-Proto $schema;
    }
}
```
