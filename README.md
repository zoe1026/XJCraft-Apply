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
> TODO

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
> TODO
