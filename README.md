# <h1 align="center">✨CHERWIN脚本使用指南 ✨</h1>
<img align="right" width="150" src="https://github.com/CHERWING/CHERWIN_SCRIPTS/assets/160421895/691b9f30-7d5c-4b55-8af0-0e8f14b6a424">

## 自助挂机：[https://gj.cherwin.cn](https://gj.cherwin.cn)

## 青龙订阅任务
```
名称：CHERWIN_SCRIPT
类型：公开仓库
链接：https://github.com/CHERWING/CHERWIN_SCRIPTS.git
定时类型：crontab
定时规则：(拉库一次就行，后续自动更新)
文件后缀：py
```
```
有其他薅羊毛应用或者有新活动可以Issues提交
格式：
  应用名称：xxxx
  任务奖励：xxxx
  （有时间一定写）
```

## ✨青龙变量设置
  - ck变量名称均为脚本名称，如永辉生活变量：export YHSH="xxxx"
  - SCRIPT_UPDATE变量设置是否自动更新默认开启，关闭请设置export SCRIPT_UPDATE="False"
  - OCR_API由于青龙python版本问题无法直接使用dddocr需要自行搭建API，搭建方式：https://github.com/CHERWING/CHERWIN_OCR
  - 如果你的环境可以安装dddocr库则可以自行修改代码

## ✨ wxpusher一对一推送功能
- 先到https://wxpusher.zjiecode.com/ 注册-新建应用-获取appToken及关注二维码或链接
- 需要定义变量export WXPUSHER=wxpusher的app_token，不设置则不启用wxpusher一对一推送
- 扫描上方二维码并加入推送群组，然后在提交的变量最后添加@wxpusher的UID。

## 🔥 永辉生活 YHSH.py
- ✔ 支持一对一推送。
- 🎉 功能：积分签到，种树，种树任务，成长值任务，试用申请，果园互助，组队互助，助力券。
- 💬 邀请口令：🔐6hDhYvlqIp1😀恭喜你，获得永辉生活免费会员资格。
- 💬 小程序邀请码
  
  <img width="150" src="https://github.com/CHERWING/CHERWIN_SCRIPTS/assets/160421895/6634271f-228a-462b-bd7b-4016cd2d641f">
  
- 💬 APP邀请码
  
  <img  width="150" src="https://github.com/CHERWING/CHERWIN_SCRIPTS/assets/160421895/be65968f-9be2-4fe6-b9c5-7b85c23d5743">
  

- ⚙️ 抓包步骤：
    1. 打开永辉生活APP或小程序并点击“我的”，打开抓包工具。
    2. 点击“积分签到”，找到以下url。
    3. 链接示例： `https://api.yonghuivip.com/web/coupon/credit/coupon/getcreditcouponpageinfo/v2?xxxxx`
    4. 多账号使用 `#` 进行分割。
  
## 🔥 朴朴超市 PPCS.py
- ✔ 支持一对一推送。
- 🎉 功能：
    积分签到
    组队互助
- 💬 邀请码：
  
  <img width="150" src="https://github.com/CHERWING/CHERWIN_SCRIPTS/assets/160421895/a2cfaf8d-c2c2-4d7f-a06c-1794c0f05351">
  
- ⚙️ 抓包步骤：
    1. 打开朴朴超市APP，已登录直接清理应用数据。
    2. 打开抓包。
    3. 抓包链接示例： `https://mcs-mimp-web.sf-express.com/mcs-mimp/share/weChat/shareGiftReceiveRedirect`
    4. 登陆。
    5. 找https://cauth.pupuapi.com/clientauth/user/verify_login
    6. 复制返回body中的refresh_token
    7. 多账号#或&分割

## 🔥 顺丰速运 SFSY.py
- ✔ 支持一对一推送。
- 🎉 功能：积分签到,签到任务
- ⚙️ 抓包步骤：
    1. 打开顺丰速运APP或小程序并点击“我的”，打开抓包工具。
    2. 点击“积分”，找到带以下url复制。
    3. 链接示例： `https://mcs-mimp-web.sf-express.com/mcs-mimp/share/weChat/shareGiftReceiveRedirect`
    4. 多账号使用 `#` 进行分割。

## 🔥 德邦快递 DBKD.py
- ✔ 支持一对一推送。
- 🎉 功能：积分签到
- ✨ 抓包步骤：
      1. 打开德邦快递小程序
      2. 授权登陆
      3. 打开抓包工具
      4. 找到https://www.deppon.com/ndcc-gwapi/userService/eco/user/login请求中body里面的[code]
      5. 复制里面的[code]参数值
    3. 链接示例： `https://mcs-mimp-web.sf-express.com/mcs-mimp/share/weChat/shareGiftReceiveRedirect`
    4. 登陆。
    5. 找https://cauth.pupuapi.com/clientauth/user/verify_login
    6. 复制返回body中的refresh_token
    7. 多账号#或&分割

## 🔥 统一茄皇 TYQH.py
- ✔ 支持一对一推送。
- 🎉 功能：日常任务，互助任务
- ✨ 抓包步骤：
      1. 打开统一快乐星球小程序-活动
      2. 开始抓包-茄皇的家第三期
      3. 抓取.../public/api/login获取thirdId@wid
      4. 多账号#或&分割 

## 🔥 统一茄皇监控 TYQH_JK.py
- ✔ 支持一对一推送。
- 🎉 功能：2-6月每月1日自动兑换

  
## 🔥 海底捞小程序 HDL.py
- ✔ 支持一对一推送。
- 🎉 功能：签到
- ✨ 抓包步骤：
      1. 开始抓包
      2. 打开海底捞小程序
      3. 抓取https://superapp-public.kiwa-tech.com/api/gateway/login/center/login/wechatLogin获取openId@uid
      4. 多账号#或&分割

## 🔥 奈雪点单小程序 NXDD.py
- ✔ 支持一对一推送。
- 🎉 功能：签到
- ✨ 抓包步骤：
      1. 开始抓包
      2. 打开奈雪点单
      3. 抓取任意url获取Authorization
      4. 多账号#或&分割

## 🔥 霸王茶姬小程序 BWCJ.py
- ✔ 支持一对一推送。
- 🎉 功能：签到
- ✨ 抓包步骤：
      1. 开始抓包
      2. 打开霸王茶姬小程序
      3. 抓取任意url获取qm-user-token
      4. 多账号#或&分割
    
## 🔥 韵达快递小程序 YDKD.py
- ✔ 支持一对一推送。
- 🎉 功能：签到
- ✨ 抓包步骤：
      1. 开始抓包
      2. 打开韵达快递小程序
      3. 抓取任意url获取Authorization
      4. 多账号#或&分割

## 🔥 中通快递小程序 ZTKD.py
- ✔ 支持一对一推送。
- 🎉 功能：签到
- ✨ 抓包步骤：
      1. 开始抓包
      2. 打开韵达快递小程序
      3. 抓取任意url获取x-token或者token
      4. 多账号#或&分割

## 🔥 极兔速递小程序 JTSD.py
- ✔ 支持一对一推送。
- 🎉 功能：签到
- ✨ 抓包步骤：
      1. 开始抓包
      2. 打开韵达快递小程序
      3. 抓取任意url获取authtoken
      4. 多账号#或&分割

## 🔥 口味王会员中心小程序 KWW.py
- ✔ 支持一对一推送。
- 🎉 功能：签到
- ✨ 抓包步骤：
      1. 开始抓包
      2. 打开口味王会员中心小程序
      3. 抓取.../member/api/info/获取memberId@unionid@openid
      4. 多账号#或&分割
  
## 🔥 卡夫亨氏新厨艺公众号 KFHS.py
- ✔ 支持一对一推送。
- 🎉 功能：签到
- ✨ 注册链接（复制微信打开）：https://fscrm.kraftheinz.net.cn/?from=N8d3E4AyKCBiu7DuBRNPlw==#/
  
<img  width="150" src="https://github.com/CHERWING/CHERWIN_SCRIPTS/assets/160421895/3f93bbe1-6ebb-462a-b61e-d54b0bbcecfc">

- ✨ 抓包步骤：
      1. 开始抓包
      2. 打开韵达快递小程序
      3. 抓取任意url获取token
      4. 多账号#或&分割
  
## 🔥 天翼云盘 TYYP.py
- ✔ 支持一对一推送。
- 🎉 功能：签到
- ✨ 变量：手机号@密码

## 🔥 蜜雪冰城小程序签到 MXBC.py
- ✔ 支持一对一推送。
- 🎉 功能：签到

- ✨ 抓包步骤：
      1. 开始抓包
      2. 打开蜜雪冰城小程序
      3. 授权登陆
      4. 找https://mxsa.mxbc.net/api/v1/app/loginByUnionid的URl(如果已经授权登陆先退出登陆)
	  5. 复制里面的unionid参数值


# 注意事项&免责申明
 本仓库发布的脚本及其中涉及的任何解密分析脚本，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。本项目内所有资源文件，禁止任何公众号、自媒体进行任何形式的转载、发布。您必须在下载后的 24 小时内从计算机或手机中完全删除以上内容。
