## 起因

  999会员中心脚本因为服务器不允许使用不安全的传统重新协商，报错（unsafe legacy renegotiation），所以需要使用反代解决
  
## 当然，如果你有服务器和域名最好使用用自己的Nginx反代（Cloudflare可能会存在域名污染）
  
  Nginx反代配置：
  
  ```
    #PROXY-START/
    location ^~ /
    {
        proxy_pass https://mc.999.com.cn;
        proxy_set_header Host mc.999.com.cn;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header REMOTE-HOST $remote_addr;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_http_version 1.1;
        # proxy_hide_header Upgrade;
    
        add_header X-Cache $upstream_cache_status;
        #Set Nginx Cache
    
        set $static_fileBp4k50Sg 0;
        if ( $uri ~* "\.(gif|png|jpg|css|js|woff|woff2)$" )
        {
            set $static_fileBp4k50Sg 1;
            expires 1m;
        }
        if ( $static_fileBp4k50Sg = 0 )
        {
            add_header Cache-Control no-cache;
        }
    }
    #PROXY-END/
  ```

## 简介

这个 Cloudflare Workers 脚本充当了一个反向代理，它的主要功能是接收客户端的请求，并将请求代理到目标地址，然后将目标地址的响应返回给客户端。具体功能包括：

- 代理客户端请求到目标地址。
- 修改响应中的相对路径为绝对路径，以确保资源的正确加载。
- 处理重定向并进行适当的修改，以保持资源路径的正确性。
- 添加 CORS 头部，以允许跨域访问。

## 如何部署

以下是部署 Cloudflare Workers 反向代理脚本的详细步骤：

1. 注册 Cloudflare 账户：如果您尚未拥有 Cloudflare 账户，请在 [Cloudflare 官方网站](https://www.cloudflare.com/) 上注册一个账户。

2. 创建 Workers 脚本：登录到 Cloudflare 账户后，进入 "Workers" 部分，创建一个新的 Workers 脚本。

3. 复制[999域名反代.js](https://github.com/CHERWING/CHERWIN_SCRIPTS/raw/main/Cloudflare%20Workers%20Proxy/999%E5%9F%9F%E5%90%8D%E5%8F%8D%E4%BB%A3.js)：将提供的反向代理脚本粘贴到 Workers 编辑器中。

4. 保存并部署：保存脚本后，点击 "Deploy" 按钮，以部署您的 Workers 脚本。

5. 配置域名：在 Cloudflare 中，将您的域名与部署的 Workers 脚本关联。确保将流量路由到您的 Workers 脚本。

6. 测试：访问您的域名或者 Cloudflare Workers URL 你会看到 【系统升级维护中】 即为成功代理
   
7. 设置变量 CF_PROXY_URL = "Workers项目url"后面加/ 例：https://xxx.xxxxx.workers.dev/

## 感谢

- [ymyuuu](https://github.com/ymyuuu/Cloudflare-Workers-Proxy)
