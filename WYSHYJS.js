/**
 *
 * 项目名称：网易生活研究社小程序
 * 项目抓包：抓miniprogram.dingwei.netease.com下的userId @ token填入变量
 * 项目变量：WYSHYJS
 * 项目定时：每天9点运行
 * cron: 0 9 * * *
 * github仓库：https://github.com/CHERWING/CHERWIN_SCRIPTS
 * @Author CHERWIN
 *
 */

//===============脚本版本=================//
let local_version = "2024.05.13";
//=======================================//
const APP_NAME = '网易生活研究社小程序'
const ENV_NAME = 'WYSHYJS'
const $ = new Env(APP_NAME);
const notify = $.isNode() ? require('./sendNotify') : '';
const Notify = 1 		//0为关闭通知,1为打开通知,默认为1
// const JSEncrypt = require('node-jsencrypt');
const axios = require('axios');
const parser = require("@babel/parser");
const fs = require('fs');
// const path = require('path');
const xpath = require('xpath')
    , XmldomParser = require('xmldom').DOMParser;
const domParser = new XmldomParser({
    errorHandler: {}
})
const {JSDOM} = require('jsdom');
let request = require("request");
request = request.defaults({jar: true});
const {log} = console;
let APP_CONFIG = "";
let UserCookie = process.env[ENV_NAME] || false;
let SCRIPT_UPDATE = process.env.SCRIPT_UPDATE || true;
let UserCookieArr = [];
let data = '';
let msg = ``;
let one_msg = '';
let gameCookie = '';
let userPhone = '';
let userUnionid = '';
let userOpenid = '';
let SING_URL = '';
let sign_Flag = false
let index_html = ''
let DuibaToken_key = ''
let token_new = ''
let new_token = ''
let orderNum = ''
let signOperatingId = ''

console.log(`✨✨✨ ${APP_NAME} ✨✨✨
` +
    '✨ 功能：\n' +
    '      积分签到\n' +
    '✨ 抓包步骤：\n' +
    '      打开抓包工具\n' +
    '      打开' +APP_NAME+'\n'+
    '      授权登陆\n' +
    '      找miniprogram.dingwei.netease.com的URl提取请求头[userId@token]（@符号连接）\n' +
    '参数示例：4249xxx@+9nnQV2D0US7I0L1sRvWLtIGpKbxQjBxxxxx\n' +
    '✨ ✨✨wxpusher一对一推送功能，\n' +
    '  ✨需要定义变量export WXPUSHER=wxpusher的app_token，不设置则不启用wxpusher一对一推送\n' +
    '  ✨需要在KWW变量最后添加@wxpusher的UID\n' +
    '✨ 设置青龙变量：\n' +
    'export '+ENV_NAME+'=\'userId@token参数值\'多账号#或&分割\n' +
    'export SCRIPT_UPDATE = \'False\' 关闭脚本自动更新，默认开启\n' +
    '✨ 推荐cron：0 9 * * *\n' +
    '✨✨✨ @Author CHERWIN✨✨✨')

//=======================================//
!(async () => {
        if (!(await Envs())) {
        } else {
            // 版本检测
            await getVersion();
            Log(`\n 脚本执行✌北京时间(UTC+8)：${new Date(new Date().getTime() + new Date().getTimezoneOffset() * 60 * 1000 + 8 * 60 * 60 * 1000).toLocaleString()} \n================ 共找到 ${UserCookieArr.length} 个账号 ================\n================ 版本对比检查更新 ================`);
            if (APP_CONFIG['NEW_VERSION'] != local_version) {
                Log(`\n 当前版本：${local_version}`)
                Log(`\n 最新版本：${APP_CONFIG['NEW_VERSION']}`)
                if (SCRIPT_UPDATE==True){
                    console.log('开始更新脚本')
                    const fileUrl = `https://github.com/CHERWING/CHERWIN_SCRIPTS/raw/main/${ENV_NAME}.js`;
                    const downloadPath = `./${ENV_NAME}.js`;
                    downloadFile(fileUrl, downloadPath)
                    .then(() => {
                        console.log('更新成功！✅，请重新运行脚本');
                        process.exit();
                    })
                    .catch((error) => {
                        console.error('更新失败❌，请手动更新:', error);
                    });
                }

            } else {
                Log(`版本信息：${local_version} ，已是最新版本无需更新开始执行脚本`)
            }
            for (let index = 0; index < UserCookieArr.length; index++) {
                one_msg = ''
                let send_UID = ''
                let num = index + 1
                Log(`\n================ 开始第 ${num} 个账号 --------------->>>>>`)
                // console.log(UserCookieArr[index])
                let split_info = UserCookieArr[index].split("@")
                userId = split_info[0];
                userToken = split_info[1];
                // console.log(userId)
                // console.log(userToken)
                let len_split_info = split_info.length
                let last_info = split_info[len_split_info - 1]
                delay()
                await start();
                await $.wait(2000);

                if (len_split_info > 0 && last_info.includes("UID_")) {
                    console.log(`检测到设置了UID:【${last_info}】✅`);
                    send_UID = last_info
                    await send_wxpusher(send_UID, one_msg, APP_NAME);
                } else {
                    Log('未检测到wxpusher UID，不执行一对一推送❌')
                }
            }
            Log(APP_CONFIG['GLOBAL_NTC'])
            await SendMsg(msg);
        }
    }
)()
    .catch((e) => log(e))
    .finally(() => $.done())


async function downloadFile(fileUrl, downloadPath) {
    try {
        const response = await axios({
            method: 'get',
            url: fileUrl,
            responseType: 'stream' // 指定响应类型为流
        });

        // 创建可写流，用于保存下载的文件
        const fileStream = fs.createWriteStream(downloadPath);

        // 监听 'data' 事件，将数据写入文件流
        response.data.pipe(fileStream);

        // 返回 Promise，在文件下载完成时 resolve
        return new Promise((resolve, reject) => {
            fileStream.on('finish', function() {
                console.log('文件下载完成。');
                resolve();
            });

            // 监听 'error' 事件，处理错误
            fileStream.on('error', function(err) {
                console.error('写入文件时发生错误:', err);
                reject(err);
            });
        });
    } catch (error) {
        console.error('下载文件时发生错误:', error);
        throw error;
    }
}




/**
 * 开始脚本
 * @returns {Promise<boolean>}
 */
async function start() {

    await getMemberInfo(2 * 1000);
    await $.wait(2000)
    if (userUnionid == '') {
        Log(`账号【${num}】登录异常，自动跳过任务！❌`);
        return false;
    }
    await get_SING_URL(2 * 1000);
    await $.wait(2000)
    if (SING_URL == '') {
        Log(`账号【${num}】cookies异常，自动跳过任务！❌`);
        return false;
    }
    await setCookies(2 * 1000);
    await $.wait(2000);
    if (gameCookie != '') {
        // 使用正则表达式获取redirect后面的URL
        var redirectUrl = SING_URL.match(/redirect=([^&]+)/)[1];
        // 对获取的URL进行解码
        var baseUrl = decodeURIComponent(redirectUrl);
        var baseHost = baseUrl.split('/')[2];
        const match = baseUrl.match(/[?&]signOperatingId=([^&]+)/);
        // 如果匹配成功，提取出 signOperatingId 的值
        signOperatingId = match ? match[1] : null;
        // console.log(`signOperatingId:${signOperatingId}`)
        // console.log(baseUrl)
        // console.log(baseHost)
        await $.wait(2000);
        await getSignIndex(baseUrl);
        await $.wait(2000);
        if (sign_Flag == false) {
            await $.wait(2000);
            await getSignIndexhtml(baseUrl);
            await $.wait(2000);
            await script_key(index_html);
            await $.wait(2000);
            // await getTokenStr(baseUrl,baseHost)
            await getTokenNew(baseUrl, baseHost)
            await $.wait(2000);
            if (token_new == '') {
                Log(`>token解密失败❌`);
                return false;
            }
            await decrypt_token(token_new, DuibaToken_key)
            // 使用正则表达式匹配URL中的 signOperatingId
            await $.wait(2000);
            await doSign(baseUrl, baseHost);
            if (orderNum == '') {
                Log('>签到失败❌');
                return false;
            }
            await $.wait(2000);
            await signResult(baseUrl, baseHost);
        }
        await $.wait(2000);
        await getCredits(baseUrl, baseHost)
    } else {
        Log(`>gameCookie异常❌`);
        return false;
    }
    return true;
}

async function script_key(html) {
    console.log('\n开始获取Script_key_str--->>>')
    return new Promise((resolve) => {
            //console.log(html)
            try {
                let doc = domParser.parseFromString(html);
                let nodes = xpath.select('//script', doc);
                let node = nodes[10].childNodes['0'].data;
                console.log('>Script_key_str获取成功✅');
                // console.log(nodes[8].childNodes['0'].data);
                get_key(nodes[8].childNodes['0'].data);
                resolve()
            } catch (e) {
                console.log(e)
            }

        }
    )

}

async function get_key(str) {
    console.log('\n开始获得KEY值--->>>')
    return new Promise(() => {
        try {
            let dom = new JSDOM(`<script>${str}</script>`, {
                runScripts: 'dangerously'
            })
            let getDuibaToken_funtion = dom.window.getDuibaToken.toString();
            // console.log(getDuibaToken_funtion)
            DuibaToken_key = getDuibaToken_funtion.match(/var key = '(.*)?';/)[1];
            console.log(`>DuibaToken_key获取成功：${DuibaToken_key}✅`);

            dom.window.close();


        } catch (e) {
            console.log(e)
        }


    })

}


async function getTokenNew(baseUrl, baseHost) {
    console.log('\n开始获取token--->>>')
    return new Promise((resolve) => {
        //console.log('检查consumerId值')
        //console.log(consumerId)
        let ts = Math.round(new Date().getTime() / 1000).toString();
        let url = 'https://' + baseHost + '/chw/ctoken/getToken';
        let host = (url.split('//')[1]).split('/')[0];
        let options = {
            method: 'post',
            url: url,
            headers: {
                'Host': host,
                'Connection': 'keep-alive',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.8',
                'Accept-Encoding': 'gzip',
                'User-Agent': getUA(),
                'Cookie': gameCookie,
                'Referer': baseUrl + '&from=login&spm=89420.1.1.1',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data: `timestamp=${timestampMs()}`
        }
        axios.request(options).then(function (response) {
            try {
                let result = response.data;
                //console.log(result)
                let success = result.success;
                if (success == true) {
                    token_new = result.token;
                    console.log('>token获取成功✅');
                }else{
                console.log('>token异常❌');
                }

            } catch (e) {
                console.log(e)
            }
        }).then(() => {
            resolve();
        }).catch(function (err) {
            console.log(err);
        })

    })

}

async function doSign(baseUrl, baseHost) {
    Log('\n开始签到--->>>')
    return new Promise((resolve) => {
        //console.log('检查consumerId值')
        //console.log(consumerId)
        let ts = Math.round(new Date().getTime() / 1000).toString();
        let url = 'https://' + baseHost + '/sign/component/doSign?_=' + timestampMs();
        let host = (url.split('//')[1]).split('/')[0];
        let options = {
            method: 'post',
            url: url,
            headers: {
                'Host': host,
                'Connection': 'keep-alive',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.8',
                'Accept-Encoding': 'gzip',
                'User-Agent': getUA(),
                'Cookie': gameCookie,
                'Referer': baseUrl + '&from=login&spm=89420.1.1.1',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data: `signOperatingId=${signOperatingId}&token=${new_token}`
        }
        axios.request(options).then(function (response) {
            try {
                // console.log(response)
                let result = response.data;
                // console.log(result)
                let data = result.data;
                let success = result.success;

                if (success == true) {
                    orderNum = data.orderNum;
                    Log(`>成功获取到orderNum：${orderNum}✅`);
                } else {
                    let desc = result.desc;
                    Log(`>${desc}✅`);
                }
            } catch (e) {
                console.log(e)
            }
        }).then(() => {
            resolve();
        }).catch(function (err) {
            console.log(err);
        })

    })

}

async function signResult(baseUrl, baseHost) {
    Log('\n开始获取签到结果--->>>')
    return new Promise((resolve) => {
        let ts = Math.round(new Date().getTime() / 1000).toString();
        let url = 'https://' + baseHost + '/sign/component/signResult'
        let host = (url.split('//')[1]).split('/')[0]
        let options = {
            method: 'get',
            url: url,
            headers: {
                'Host': host,
                'Connection': 'keep-alive',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.8',
                'Accept-Encoding': 'gzip',
                'User-Agent': getUA(),
                'Cookie': gameCookie,
                'Referer': baseUrl + '&from=login&spm=89420.1.1.1',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data: `orderNum=${orderNum}&_=${timestampMs()}`
        }
        axios.request(options).then(function (response) {
            try {
                // console.log(response)
                let result = response.data
                let success = result.success;
                if (success == true) {
                    // console.log(result)
                    let data = result.data
                    signResult = data.signResult
                    if (signResult == 1) {
                        Log(`>签到成功获得：${signResult}积分✅`)
                    }
                }else{
                    Log(`>签到结果异常❌`)
                }
            } catch (e) {
                console.log(e)
            }
        }).then(() => {
            resolve();
        }).catch(function (err) {
            console.log(err);
        })

    })

}

async function decrypt_token(str, key) {
    Log('\n开始解密token值--->>>')
    return new Promise((resolve) => {
        let dom = new JSDOM(`<script>${str}</script>`, {
            runScripts: 'dangerously'
        })
        try {
            new_token = dom.window[key]
            Log(`>解密成功token:${new_token}✅`)
            resolve()
        } catch (e) {
            console.log(e);
        }
    });
}

async function getMemberInfo(timeout = 2000) {
    Log('\n开始获取用户信息--->>>')
    return new Promise((resolve) => {
        var options = {
            method: 'GET',
            url: `https://miniprogram.dingwei.netease.com/api/miniprogram/user/detail?userId=` + userId,
            params: {},
            headers: {
                Host: 'miniprogram.dingwei.netease.com',
                Connection: 'keep-alive',
                'userId': userId,
                'token': userToken,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/9129',
                Referer: 'https://servicewechat.com/wx91a054c39722497e/59/page-frame.html'
            },
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                // console.log(data)
                // console.log(data.result)
                let result = data.result;
                if (data.code = 200) {
                    userPhone = result.phone
                    userUnionid = result.unionId
                    userOpenid = result.openid
                    Log(`>手机号：【${userPhone}】,登录成功: ✅ `)
                    // Log(`>手机号：【${userPhone}】`)
                    // Log(`>unionId：【${userUnionid}】`)
                    // Log(`>openid：【${userOpenid}】`)
                } else {
                    addNotifyStr(`登录失败❌，原因是：${data.msg}`, true)
                }
            } catch (e) {
                log(`登录失败：${data}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(1, error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        }, timeout)
    })
}

async function get_SING_URL(timeout = 2000) {
    console.log('\n获取签到url--->>>')
    return new Promise((resolve) => {
        var options = {
            method: 'GET',
            url: `https://miniprogram.dingwei.netease.com/api/miniprogram/duiba/authUrl/get?type=1&` + userId,
            params: {},
            headers: {
                Host: 'miniprogram.dingwei.netease.com',
                Connection: 'keep-alive',
                'userId': userId,
                'token': userToken,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/9129',
                Referer: 'https://servicewechat.com/wx91a054c39722497e/59/page-frame.html'
            },
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                // console.log(data)
                // console.log(data.result)
                if (data.code = 200) {
                    SING_URL = data.result;
                    console.log(`>获取签到URL成功: ✅ `)
                    // console.log(`SING_URL：【${SING_URL}】`)
                } else {
                    addNotifyStr(`获取签到URL❌，原因是：${data.msg}`, true)
                }
            } catch (e) {
                log(`获取签到URL异常：${data}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(1, error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        }, timeout)
    })
}


/**
 * 设置cookie
 * @returns {Promise<unknown>}
 */
async function setCookies() {
    console.log(`\n转换Cookie--->>>`)
    return new Promise((resolve) => {
        var host = (SING_URL.split('//')[1]).split('/')[0];
        try {
            request(
                {
                    url: SING_URL,
                    method: "GET",
                    headers: {
                        'Host': host,
                        'Connection': 'keep-alive',
                        'User-Agent': getUA(),
                        "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-User": "?1",
                        "Sec-Fetch-Dest": "document",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "en-us,en",
                    },
                }, function (err, res, body) {
                    gameCookie = res.request.headers.cookie;
                    // console.log(gameCookie)
                    console.log(`>转换Cookie成功！`)
                })
        } catch (e) {
            console.log(e)
        } finally {
            resolve();

        }
    })
}

async function getSignIndexhtml(baseUrl) {
    console.log('\n获取签到页Html--->>>')
    qgySignFlag = false;
    return new Promise((resolve) => {
        var url = baseUrl + '&preview=false';

        var host = (url.split('//')[1]).split('/')[0];
        // console.log(gameCookie)
        var options = {
            method: 'GET',
            url: url,
            params: {_: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: baseUrl + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {}
        };
        // console.log(options)
        axios.request(options).then(function (response) {
            try {
                let result = response.data
                index_html = result
                console.log('>获取签到页Html成功✅')
            } catch (e) {
                console.log(`>获取签到页Html: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}

async function getSignIndex(baseUrl) {
    Log('\n获取签到状态--->>>')
    sign_Flag = false;
    return new Promise((resolve) => {
        baseUrl = baseUrl.replace('page', 'index')
        // console.log(baseUrl)
        var url = baseUrl + '&preview=false';

        var host = (url.split('//')[1]).split('/')[0];
        // console.log(gameCookie)
        var options = {
            method: 'GET',
            url: url,
            params: {_: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: baseUrl + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {}
        };
        // console.log(options)
        axios.request(options).then(function (response) {
            try {
                var data = response.data.data;
                var signResult = data.signResult;
                // console.log(signResult)
                if (signResult == true) {
                    sign_Flag = true
                    Log('>今日已签到,跳过✅')
                } else {
                    sign_Flag = false
                    Log('>今日未签到❌')
                }
                // console.log(data)
            } catch (e) {
                Log(`获取签到状态: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}

async function getCredits(baseUrl, baseHost) {
    Log('\n开始获取积分信息--->>>')
    qgySignFlag = false;
    return new Promise((resolve) => {
        var url = 'https://' + baseHost + '/ctool/getCredits';
        var host = (url.split('//')[1]).split('/')[0];
        // console.log(gameCookie)
        var options = {
            method: 'POST',
            url: url,
            params: {_: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: baseUrl + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {}
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data.data;
                credits = data.credits
                Log(`当前积分：【${credits}】✅`)
            } catch (e) {
                Log(`获取积分: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}


// ============================================一对一推送============================================ \\
async function send_wxpusher(UID, send_msg, title, help = false) {
    const WXPUSHER = process.env.WXPUSHER || false;
    if (WXPUSHER) {
        console.log('\n设置了WXPUSHER变量✅,开始一对一推送--->>>')
        if (help) {
            title += '互助';
        }
        // console.log('\n开始wxpusher推送------>>>>');
        // console.log(`标题：【${title}】\n内容：${send_msg}`);
        const webapi = 'http://wxpusher.zjiecode.com/api/send/message';
        // send_msg = send_msg.replace("\n", "<br>");
        const tips = APP_CONFIG['GLOBAL_NTC_HTML']
        const data = {
            "appToken": WXPUSHER,
            "content": `${title}<br>${send_msg}<br>${tips}`,
            // "summary": msg.substring(0, 99), // 可选参数，默认为 msg 的前10个字符
            "summary": title,
            "contentType": 2,
            "uids": [UID],
            "url": "https://gj.cherwin.cn"
        };

        axios.post(webapi, data)
            .then(response => {
                if (response.data.success) {
                    console.log(">wxpusher消息发送成功✅");
                } else {
                    console.error(`>wxpusher消息发送失败❌。错误信息：${response.data.msg}`);
                }
            })
            .catch(error => {
                console.error(`>wxpusher发送消息时发生错误❌：${error.message}`);
            });
    } else {
        console.log('>未设置WXPUSHER变量❌，取消一对一推送')
    }
}


// ============================================变量检查============================================ \\
async function Envs() {
    if (UserCookie) {

        if (UserCookie.includes('&')) {
            var amp_parts = UserCookie.split('&');
            for (var i = 0; i < amp_parts.length; i++) {
                if (amp_parts[i].includes('#')) {
                    var hash_parts = amp_parts[i].split('#');
                    for (var j = 0; j < hash_parts.length; j++) {
                        UserCookieArr.push(hash_parts[j]);
                    }
                } else {
                    UserCookieArr.push(amp_parts[i]);
                }
            }

        } else if (UserCookie.includes('#')) {
            hash_parts = UserCookie.split('#');
            UserCookieArr.push(hash_parts);

        } else {
            var out_str = UserCookie.toString();
            UserCookieArr.push(out_str);
        }
    } else {
        console.log(`\n 系统变量【KWW】未定义❌`)
        return;
    }
    return true;
}

// ============================================发送消息============================================ \\
async function SendMsg(message) {
    if (!message)
        return;

    if (Notify > 0) {
        if ($.isNode()) {
            var notify = require('./sendNotify');
            await notify.sendNotify($.name, message);
        } else {
            $.msg(message);
        }
    } else {
        log(message);
    }
}

/**
 * 添加消息
 * @param str
 * @param is_log
 */
function addNotifyStr(str, is_log = true) {
    if (is_log) {
        log(`${str}\n`)
    }
    msg += `${str}\n`
    one_msg += `${str}\n<br>`;
}

/**
 * 双平台log输出
 */
function Log(data) {
    console.log(`${data}\n`);
    msg += `${data}\n`;
    one_msg += `${data}\n<br>`;
}

function randomNum(min, max) {
    if (arguments.length === 0) return Math.random()
    if (!max) max = 10 ** (Math.log(min) * Math.LOG10E + 1 | 0) - 1
    return Math.floor(Math.random() * (max - min + 1) + min);
}

/**
 * 随机延时1-30s，避免大家运行时间一样
 * @returns {*|number}
 */
function delay() {
    let time = parseInt(Math.random() * 100000);
    if (time > 30000) {// 大于30s重新生成
        return delay();
    } else {
        console.log('随机延时1-30s避免大家运行时间一样：', `本次延时：${time}ms`)
        return time;// 小于30s，返回
    }
}


/**
 * 随机UA
 * @param inputString
 * @returns {*}
 */
function getUA() {
    $.UUID = randomString(40)
    const buildMap = {
        "167814": `10.1.4`,
        "167841": `10.1.6`,
        "167853": `10.2.0`
    }
    $.osVersion = `${randomNum(13, 14)}.${randomNum(3, 6)}.${randomNum(1, 3)}`
    let network = `network/${['4g', '5g', 'wifi'][randomNum(0, 2)]}`
    $.mobile = `iPhone${randomNum(9, 13)},${randomNum(1, 3)}`
    $.build = ["167814", "167841", "167853"][randomNum(0, 2)]
    $.appVersion = buildMap[$.build]
    return `jdapp;iPhone;${$.appVersion};${$.osVersion};${$.UUID};M/5.0;${network};ADID/;model/${$.mobile};addressid/;appBuild/${$.build};jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS ${$.osVersion.replace(/\./g, "_")} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1;`
}

// ============================================签名加密============================================ \\
var i,
    l = ["A", "Z", "B", "Y", "C", "X", "D", "T", "E", "S", "F", "R", "G", "Q", "H", "P", "I", "O", "J", "N", "k", "M", "L", "a", "c", "d", "f", "h", "k", "p", "y", "n"];
var o = 8

function s(e, t) {
    var a, n, r, i, o, l, s, u, p;
    for (e[t >> 5] |= 128 << t % 32, e[14 + (t + 64 >>> 9 << 4)] = t, a = 1732584193,
             n = -271733879, r = -1732584194, i = 271733878, o = 0; o < e.length; o += 16) l = a,
        s = n, u = r, p = i, a = d(a, n, r, i, e[o + 0], 7, -680876936), i = d(i, a, n, r, e[o + 1], 12, -389564586),
        r = d(r, i, a, n, e[o + 2], 17, 606105819), n = d(n, r, i, a, e[o + 3], 22, -1044525330),
        a = d(a, n, r, i, e[o + 4], 7, -176418897), i = d(i, a, n, r, e[o + 5], 12, 1200080426),
        r = d(r, i, a, n, e[o + 6], 17, -1473231341), n = d(n, r, i, a, e[o + 7], 22, -45705983),
        a = d(a, n, r, i, e[o + 8], 7, 1770035416), i = d(i, a, n, r, e[o + 9], 12, -1958414417),
        r = d(r, i, a, n, e[o + 10], 17, -42063), n = d(n, r, i, a, e[o + 11], 22, -1990404162),
        a = d(a, n, r, i, e[o + 12], 7, 1804603682), i = d(i, a, n, r, e[o + 13], 12, -40341101),
        r = d(r, i, a, n, e[o + 14], 17, -1502002290), n = d(n, r, i, a, e[o + 15], 22, 1236535329),
        a = c(a, n, r, i, e[o + 1], 5, -165796510), i = c(i, a, n, r, e[o + 6], 9, -1069501632),
        r = c(r, i, a, n, e[o + 11], 14, 643717713), n = c(n, r, i, a, e[o + 0], 20, -373897302),
        a = c(a, n, r, i, e[o + 5], 5, -701558691), i = c(i, a, n, r, e[o + 10], 9, 38016083),
        r = c(r, i, a, n, e[o + 15], 14, -660478335), n = c(n, r, i, a, e[o + 4], 20, -405537848),
        a = c(a, n, r, i, e[o + 9], 5, 568446438), i = c(i, a, n, r, e[o + 14], 9, -1019803690),
        r = c(r, i, a, n, e[o + 3], 14, -187363961), n = c(n, r, i, a, e[o + 8], 20, 1163531501),
        a = c(a, n, r, i, e[o + 13], 5, -1444681467), i = c(i, a, n, r, e[o + 2], 9, -51403784),
        r = c(r, i, a, n, e[o + 7], 14, 1735328473), n = c(n, r, i, a, e[o + 12], 20, -1926607734),
        a = f(a, n, r, i, e[o + 5], 4, -378558), i = f(i, a, n, r, e[o + 8], 11, -2022574463),
        r = f(r, i, a, n, e[o + 11], 16, 1839030562), n = f(n, r, i, a, e[o + 14], 23, -35309556),
        a = f(a, n, r, i, e[o + 1], 4, -1530992060), i = f(i, a, n, r, e[o + 4], 11, 1272893353),
        r = f(r, i, a, n, e[o + 7], 16, -155497632), n = f(n, r, i, a, e[o + 10], 23, -1094730640),
        a = f(a, n, r, i, e[o + 13], 4, 681279174), i = f(i, a, n, r, e[o + 0], 11, -358537222),
        r = f(r, i, a, n, e[o + 3], 16, -722521979), n = f(n, r, i, a, e[o + 6], 23, 76029189),
        a = f(a, n, r, i, e[o + 9], 4, -640364487), i = f(i, a, n, r, e[o + 12], 11, -421815835),
        r = f(r, i, a, n, e[o + 15], 16, 530742520), n = f(n, r, i, a, e[o + 2], 23, -995338651),
        a = h(a, n, r, i, e[o + 0], 6, -198630844), i = h(i, a, n, r, e[o + 7], 10, 1126891415),
        r = h(r, i, a, n, e[o + 14], 15, -1416354905), n = h(n, r, i, a, e[o + 5], 21, -57434055),
        a = h(a, n, r, i, e[o + 12], 6, 1700485571), i = h(i, a, n, r, e[o + 3], 10, -1894986606),
        r = h(r, i, a, n, e[o + 10], 15, -1051523), n = h(n, r, i, a, e[o + 1], 21, -2054922799),
        a = h(a, n, r, i, e[o + 8], 6, 1873313359), i = h(i, a, n, r, e[o + 15], 10, -30611744),
        r = h(r, i, a, n, e[o + 6], 15, -1560198380), n = h(n, r, i, a, e[o + 13], 21, 1309151649),
        a = h(a, n, r, i, e[o + 4], 6, -145523070), i = h(i, a, n, r, e[o + 11], 10, -1120210379),
        r = h(r, i, a, n, e[o + 2], 15, 718787259), n = h(n, r, i, a, e[o + 9], 21, -343485551),
        a = m(a, l), n = m(n, s), r = m(r, u), i = m(i, p);
    return Array(a, n, r, i);
}

function u(e, t, a, n, r, i) {
    return m(p(m(m(t, e), m(n, i)), r), a);
}

function d(e, t, a, n, r, i, o) {
    return u(t & a | ~t & n, e, t, r, i, o);
}

function c(e, t, a, n, r, i, o) {
    return u(t & n | a & ~n, e, t, r, i, o);
}

function f(e, t, a, n, r, i, o) {
    return u(t ^ a ^ n, e, t, r, i, o);
}

function h(e, t, a, n, r, i, o) {
    return u(a ^ (t | ~n), e, t, r, i, o);
}

function m(e, t) {
    var a = (65535 & e) + (65535 & t),
        n = (e >> 16) + (t >> 16) + (a >> 16);
    return n << 16 | 65535 & a;
}

function p(e, t) {
    return e << t | e >>> 32 - t;
}

function b(e) {
    var t, a = Array(),
        n = (1 << o) - 1;
    for (t = 0; t < e.length * o; t += o)
        a[t >> 5] |= (e.charCodeAt(t / o) & n) << t % 32;
    return a;
}

function _(e) {
    var t, a = i ? "0123456789ABCDEF" : "0123456789abcdef",
        n = "";
    for (t = 0; t < 4 * e.length; t++) n += a.charAt(15 & e[t >> 2] >> t % 4 * 8 + 4) + a.charAt(15 & e[t >> 2] >> t % 4 * 8);
    return n;
}

function v(e) {
    return _(s(b(_(s(b(e), e.length * o)) + "iussoft"), (_(s(b(e), e.length * o)) + "iussoft").length * o));
}

function y(e) {
    var t = e + '6b4ba4460e064dee87ccbe5652a01fdc';
    return _(s(b(t), t.length * o));
}

function g(e) {
    var t = e + "14YVeC0PToxklds";
    return _(s(b(t), t.length * o));
}

function w(e, t, a) {
    t || (t = "86109D696C9CC58A504EFE21662DF1B9");
    var n = e + t + l[a];
    return _(s(b(n), n.length * o));
}

function getRandom(e, t) {
    return Math.floor(Math.random() * (e - t)) + t;
}

function getUserSign(memberId, userTimestamp, userRandom) {
    return (0, w)(userTimestamp, memberId, userRandom)
}

/**
 * 获取当前小时数
 */
function local_hours() {
    let myDate = new Date();
    let h = myDate.getHours();
    return h;
}

/**
 * 获取当前分钟数
 */
function local_minutes() {
    let myDate = new Date();
    let m = myDate.getMinutes();
    return m;
}

/**
 * 随机数生成
 */
function randomString(e) {
    e = e || 32;
    var t = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890",
        a = t.length,
        n = "";
    for (i = 0; i < e; i++)
        n += t.charAt(Math.floor(Math.random() * a));
    return n
}

/**
 * 随机整数生成
 */
function randomInt(min, max) {
    return Math.round(Math.random() * (max - min) + min)
}

/**
 * 获取毫秒时间戳
 */
function timestampMs() {
    return new Date().getTime();
}

/**
 *
 * 获取秒时间戳
 */
function timestampS() {
    return Date.parse(new Date()) / 1000;
}


/**
 * 修改配置文件
 */
function modify() {
    fs.readFile('/ql/data/config/config.sh', 'utf8', function (err, dataStr) {
        if (err) {
            return log('读取文件失败！' + err)
        } else {
            var result = dataStr.replace(/regular/g, string);
            fs.writeFile('/ql/data/config/config.sh', result, 'utf8', function (err) {
                if (err) {
                    return log(err);
                }
            });
        }
    })
}

/**
 * 获取远程版本
 */

function getVersion(timeout = 3 * 1000) {
    return new Promise((resolve) => {
        let url = {
            url: `https://py.cherwin.cn/CHERWIN_SCRIPT_CONFIG.json`,
        }
        $.get(url, async (err, resp, data) => {
            try {
                // 解析响应数据
                const config = JSON.parse(data);
                // console.log(config)
                // 获取所需的配置值
                const newVersion = config['APP_CONFIG'][ENV_NAME]['NEW_VERSION'];
                // console.log(newVersion)
                const ntc = config['APP_CONFIG'][ENV_NAME]['NTC'];
                const ENABLE = config['APP_CONFIG'][ENV_NAME]['ENABLE'];
                if(ENABLE==false){
                    console.log('脚本未开放')
                    process.exit();
                }
                // console.log(ntc)
                const globalNtcHtml = config['GLOBAL_NTC_HTML'];
                const globalNtc = config['GLOBAL_NTC'];
                // console.log(globalNtc)
                // 将获取到的值作为对象返回
                APP_CONFIG = {
                    'NEW_VERSION': newVersion,
                    'NTC': ntc,
                    'GLOBAL_NTC_HTML': globalNtcHtml,
                    'GLOBAL_NTC': globalNtc
                }
                resolve(APP_CONFIG);

            } catch (e) {
                $.logErr(e, resp);
            } finally {
                resolve()
            }
        }, timeout)
    })
}

/**
 * time 输出格式：1970-01-01 00:00:00
 */
function t() {
    var date = new Date();
    // 获取当前月份
    var nowMonth = date.getMonth() + 1;
    // 获取当前是几号
    var strDate = date.getDate();
    //获取当前小时（0-23）
    var nowhour = date.getHours()
    //获取当前分钟（0-59）
    var nowMinute = date.getMinutes()
    //获取当前秒数(0-59)
    var nowSecond = date.getSeconds();
    // 添加分隔符“-”
    var seperator = "-";
    // 添加分隔符“:”
    var seperator1 = ":";
    // 对月份进行处理，1-9月在前面添加一个“0”
    if (nowMonth >= 1 && nowMonth <= 9) {
        nowMonth = "0" + nowMonth;
    }
    // 对月份进行处理，1-9号在前面添加一个“0”
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    // 对小时进行处理，0-9号在前面添加一个“0”
    if (nowhour >= 0 && nowhour <= 9) {
        nowhour = "0" + nowhour;
    }
    // 对分钟进行处理，0-9号在前面添加一个“0”
    if (nowMinute >= 0 && nowMinute <= 9) {
        nowMinute = "0" + nowMinute;
    }
    // 对秒数进行处理，0-9号在前面添加一个“0”
    if (nowSecond >= 0 && nowSecond <= 9) {
        nowSecond = "0" + nowSecond;
    }

    // 最后拼接字符串，得到一个格式为(yyyy-MM-dd)的日期
    var nowDate = date.getFullYear() + seperator + nowMonth + seperator + strDate + ` ` + nowhour + seperator1 + nowMinute + seperator1 + nowSecond
    return nowDate
}


// md5
function MD5Encrypt(a) {
    function b(a, b) {
        return a << b | a >>> 32 - b
    }

    function c(a, b) {
        var c, d, e, f, g;
        return e = 2147483648 & a, f = 2147483648 & b, c = 1073741824 & a, d = 1073741824 & b, g = (1073741823 & a) + (1073741823 & b), c & d ? 2147483648 ^ g ^ e ^ f : c | d ? 1073741824 & g ? 3221225472 ^ g ^ e ^ f : 1073741824 ^ g ^ e ^ f : g ^ e ^ f
    }

    function d(a, b, c) {
        return a & b | ~a & c
    }

    function e(a, b, c) {
        return a & c | b & ~c
    }

    function f(a, b, c) {
        return a ^ b ^ c
    }

    function g(a, b, c) {
        return b ^ (a | ~c)
    }

    function h(a, e, f, g, h, i, j) {
        return a = c(a, c(c(d(e, f, g), h), j)), c(b(a, i), e)
    }

    function i(a, d, f, g, h, i, j) {
        return a = c(a, c(c(e(d, f, g), h), j)), c(b(a, i), d)
    }

    function j(a, d, e, g, h, i, j) {
        return a = c(a, c(c(f(d, e, g), h), j)), c(b(a, i), d)
    }

    function k(a, d, e, f, h, i, j) {
        return a = c(a, c(c(g(d, e, f), h), j)), c(b(a, i), d)
    }

    function l(a) {
        for (var b, c = a.length, d = c + 8, e = (d - d % 64) / 64, f = 16 * (e + 1), g = new Array(f - 1), h = 0, i = 0; c > i;) b = (i - i % 4) / 4, h = i % 4 * 8, g[b] = g[b] | a.charCodeAt(i) << h, i++;
        return b = (i - i % 4) / 4, h = i % 4 * 8, g[b] = g[b] | 128 << h, g[f - 2] = c << 3, g[f - 1] = c >>> 29, g
    }

    function m(a) {
        var b, c, d = "", e = "";
        for (c = 0; 3 >= c; c++) b = a >>> 8 * c & 255, e = "0" + b.toString(16), d += e.substr(e.length - 2, 2);
        return d
    }

    function n(a) {
        a = a.replace(/\r\n/g, "\n");
        for (var b = "", c = 0; c < a.length; c++) {
            var d = a.charCodeAt(c);
            128 > d ? b += String.fromCharCode(d) : d > 127 && 2048 > d ? (b += String.fromCharCode(d >> 6 | 192), b += String.fromCharCode(63 & d | 128)) : (b += String.fromCharCode(d >> 12 | 224), b += String.fromCharCode(d >> 6 & 63 | 128), b += String.fromCharCode(63 & d | 128))
        }
        return b
    }

    var o, p, q, r, s, t, u, v, w, x = [], y = 7, z = 12, A = 17, B = 22, C = 5, D = 9, E = 14, F = 20, G = 4, H = 11,
        I = 16, J = 23, K = 6, L = 10, M = 15, N = 21;
    for (a = n(a), x = l(a), t = 1732584193, u = 4023233417, v = 2562383102, w = 271733878, o = 0; o < x.length; o += 16) p = t, q = u, r = v, s = w, t = h(t, u, v, w, x[o + 0], y, 3614090360), w = h(w, t, u, v, x[o + 1], z, 3905402710), v = h(v, w, t, u, x[o + 2], A, 606105819), u = h(u, v, w, t, x[o + 3], B, 3250441966), t = h(t, u, v, w, x[o + 4], y, 4118548399), w = h(w, t, u, v, x[o + 5], z, 1200080426), v = h(v, w, t, u, x[o + 6], A, 2821735955), u = h(u, v, w, t, x[o + 7], B, 4249261313), t = h(t, u, v, w, x[o + 8], y, 1770035416), w = h(w, t, u, v, x[o + 9], z, 2336552879), v = h(v, w, t, u, x[o + 10], A, 4294925233), u = h(u, v, w, t, x[o + 11], B, 2304563134), t = h(t, u, v, w, x[o + 12], y, 1804603682), w = h(w, t, u, v, x[o + 13], z, 4254626195), v = h(v, w, t, u, x[o + 14], A, 2792965006), u = h(u, v, w, t, x[o + 15], B, 1236535329), t = i(t, u, v, w, x[o + 1], C, 4129170786), w = i(w, t, u, v, x[o + 6], D, 3225465664), v = i(v, w, t, u, x[o + 11], E, 643717713), u = i(u, v, w, t, x[o + 0], F, 3921069994), t = i(t, u, v, w, x[o + 5], C, 3593408605), w = i(w, t, u, v, x[o + 10], D, 38016083), v = i(v, w, t, u, x[o + 15], E, 3634488961), u = i(u, v, w, t, x[o + 4], F, 3889429448), t = i(t, u, v, w, x[o + 9], C, 568446438), w = i(w, t, u, v, x[o + 14], D, 3275163606), v = i(v, w, t, u, x[o + 3], E, 4107603335), u = i(u, v, w, t, x[o + 8], F, 1163531501), t = i(t, u, v, w, x[o + 13], C, 2850285829), w = i(w, t, u, v, x[o + 2], D, 4243563512), v = i(v, w, t, u, x[o + 7], E, 1735328473), u = i(u, v, w, t, x[o + 12], F, 2368359562), t = j(t, u, v, w, x[o + 5], G, 4294588738), w = j(w, t, u, v, x[o + 8], H, 2272392833), v = j(v, w, t, u, x[o + 11], I, 1839030562), u = j(u, v, w, t, x[o + 14], J, 4259657740), t = j(t, u, v, w, x[o + 1], G, 2763975236), w = j(w, t, u, v, x[o + 4], H, 1272893353), v = j(v, w, t, u, x[o + 7], I, 4139469664), u = j(u, v, w, t, x[o + 10], J, 3200236656), t = j(t, u, v, w, x[o + 13], G, 681279174), w = j(w, t, u, v, x[o + 0], H, 3936430074), v = j(v, w, t, u, x[o + 3], I, 3572445317), u = j(u, v, w, t, x[o + 6], J, 76029189), t = j(t, u, v, w, x[o + 9], G, 3654602809), w = j(w, t, u, v, x[o + 12], H, 3873151461), v = j(v, w, t, u, x[o + 15], I, 530742520), u = j(u, v, w, t, x[o + 2], J, 3299628645), t = k(t, u, v, w, x[o + 0], K, 4096336452), w = k(w, t, u, v, x[o + 7], L, 1126891415), v = k(v, w, t, u, x[o + 14], M, 2878612391), u = k(u, v, w, t, x[o + 5], N, 4237533241), t = k(t, u, v, w, x[o + 12], K, 1700485571), w = k(w, t, u, v, x[o + 3], L, 2399980690), v = k(v, w, t, u, x[o + 10], M, 4293915773), u = k(u, v, w, t, x[o + 1], N, 2240044497), t = k(t, u, v, w, x[o + 8], K, 1873313359), w = k(w, t, u, v, x[o + 15], L, 4264355552), v = k(v, w, t, u, x[o + 6], M, 2734768916), u = k(u, v, w, t, x[o + 13], N, 1309151649), t = k(t, u, v, w, x[o + 4], K, 4149444226), w = k(w, t, u, v, x[o + 11], L, 3174756917), v = k(v, w, t, u, x[o + 2], M, 718787259), u = k(u, v, w, t, x[o + 9], N, 3951481745), t = c(t, p), u = c(u, q), v = c(v, r), w = c(w, s);
    var O = m(t) + m(u) + m(v) + m(w);
    return O.toLowerCase()
}

// 完整 Env
function Env(t, e) {
    "undefined" != typeof process && JSON.stringify(process.env).indexOf("GITHUB") > -1 && process.exit(0);

    class s {
        constructor(t) {
            this.env = t
        }

        send(t, e = "GET") {
            t = "string" == typeof t ? {url: t} : t;
            let s = this.get;
            return "POST" === e && (s = this.post), new Promise((e, i) => {
                s.call(this, t, (t, s, r) => {
                    t ? i(t) : e(s)
                })
            })
        }

        get(t) {
            return this.send.call(this.env, t)
        }

        post(t) {
            return this.send.call(this.env, t, "POST")
        }
    }

    return new class {
        constructor(t, e) {
            this.name = t, this.http = new s(this), this.data = null, this.dataFile = "box.dat", this.logs = [], this.isMute = !1, this.isNeedRewrite = !1, this.logSeparator = "\n", this.startTime = (new Date).getTime(), Object.assign(this, e), this.log("", `🔔${this.name}, 开始!`)
        }

        isNode() {
            return "undefined" != typeof module && !!module.exports
        }

        isQuanX() {
            return "undefined" != typeof $task
        }

        isSurge() {
            return "undefined" != typeof $httpClient && "undefined" == typeof $loon
        }

        isLoon() {
            return "undefined" != typeof $loon
        }

        toObj(t, e = null) {
            try {
                return JSON.parse(t)
            } catch {
                return e
            }
        }

        toStr(t, e = null) {
            try {
                return JSON.stringify(t)
            } catch {
                return e
            }
        }

        getjson(t, e) {
            let s = e;
            const i = this.getdata(t);
            if (i) try {
                s = JSON.parse(this.getdata(t))
            } catch {
            }
            return s
        }

        setjson(t, e) {
            try {
                return this.setdata(JSON.stringify(t), e)
            } catch {
                return !1
            }
        }

        getScript(t) {
            return new Promise(e => {
                this.get({url: t}, (t, s, i) => e(i))
            })
        }

        runScript(t, e) {
            return new Promise(s => {
                let i = this.getdata("@chavy_boxjs_userCfgs.httpapi");
                i = i ? i.replace(/\n/g, "").trim() : i;
                let r = this.getdata("@chavy_boxjs_userCfgs.httpapi_timeout");
                r = r ? 1 * r : 20, r = e && e.timeout ? e.timeout : r;
                const [o, h] = i.split("@"), n = {
                    url: `http://${h}/v1/scripting/evaluate`,
                    body: {script_text: t, mock_type: "cron", timeout: r},
                    headers: {"X-Key": o, Accept: "*/*"}
                };
                this.post(n, (t, e, i) => s(i))
            }).catch(t => this.logErr(t))
        }

        loaddata() {
            if (!this.isNode()) return {};
            {
                this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path");
                const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile),
                    s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e);
                if (!s && !i) return {};
                {
                    const i = s ? t : e;
                    try {
                        return JSON.parse(this.fs.readFileSync(i))
                    } catch (t) {
                        return {}
                    }
                }
            }
        }

        writedata() {
            if (this.isNode()) {
                this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path");
                const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile),
                    s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e), r = JSON.stringify(this.data);
                s ? this.fs.writeFileSync(t, r) : i ? this.fs.writeFileSync(e, r) : this.fs.writeFileSync(t, r)
            }
        }

        lodash_get(t, e, s) {
            const i = e.replace(/\[(\d+)\]/g, ".$1").split(".");
            let r = t;
            for (const t of i) if (r = Object(r)[t], void 0 === r) return s;
            return r
        }

        lodash_set(t, e, s) {
            return Object(t) !== t ? t : (Array.isArray(e) || (e = e.toString().match(/[^.[\]]+/g) || []), e.slice(0, -1).reduce((t, s, i) => Object(t[s]) === t[s] ? t[s] : t[s] = Math.abs(e[i + 1]) >> 0 == +e[i + 1] ? [] : {}, t)[e[e.length - 1]] = s, t)
        }

        getdata(t) {
            let e = this.getval(t);
            if (/^@/.test(t)) {
                const [, s, i] = /^@(.*?)\.(.*?)$/.exec(t), r = s ? this.getval(s) : "";
                if (r) try {
                    const t = JSON.parse(r);
                    e = t ? this.lodash_get(t, i, "") : e
                } catch (t) {
                    e = ""
                }
            }
            return e
        }

        setdata(t, e) {
            let s = !1;
            if (/^@/.test(e)) {
                const [, i, r] = /^@(.*?)\.(.*?)$/.exec(e), o = this.getval(i),
                    h = i ? "null" === o ? null : o || "{}" : "{}";
                try {
                    const e = JSON.parse(h);
                    this.lodash_set(e, r, t), s = this.setval(JSON.stringify(e), i)
                } catch (e) {
                    const o = {};
                    this.lodash_set(o, r, t), s = this.setval(JSON.stringify(o), i)
                }
            } else s = this.setval(t, e);
            return s
        }

        getval(t) {
            return this.isSurge() || this.isLoon() ? $persistentStore.read(t) : this.isQuanX() ? $prefs.valueForKey(t) : this.isNode() ? (this.data = this.loaddata(), this.data[t]) : this.data && this.data[t] || null
        }

        setval(t, e) {
            return this.isSurge() || this.isLoon() ? $persistentStore.write(t, e) : this.isQuanX() ? $prefs.setValueForKey(t, e) : this.isNode() ? (this.data = this.loaddata(), this.data[e] = t, this.writedata(), !0) : this.data && this.data[e] || null
        }

        initGotEnv(t) {
            this.got = this.got ? this.got : require("got"), this.cktough = this.cktough ? this.cktough : require("tough-cookie"), this.ckjar = this.ckjar ? this.ckjar : new this.cktough.CookieJar, t && (t.headers = t.headers ? t.headers : {}, void 0 === t.headers.Cookie && void 0 === t.cookieJar && (t.cookieJar = this.ckjar))
        }

        get(t, e = (() => {
        })) {
            t.headers && (delete t.headers["Content-Type"], delete t.headers["Content-Length"]), this.isSurge() || this.isLoon() ? (this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, {"X-Surge-Skip-Scripting": !1})), $httpClient.get(t, (t, s, i) => {
                !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i)
            })) : this.isQuanX() ? (this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, {hints: !1})), $task.fetch(t).then(t => {
                const {statusCode: s, statusCode: i, headers: r, body: o} = t;
                e(null, {status: s, statusCode: i, headers: r, body: o}, o)
            }, t => e(t))) : this.isNode() && (this.initGotEnv(t), this.got(t).on("redirect", (t, e) => {
                try {
                    if (t.headers["set-cookie"]) {
                        const s = t.headers["set-cookie"].map(this.cktough.Cookie.parse).toString();
                        s && this.ckjar.setCookieSync(s, null), e.cookieJar = this.ckjar
                    }
                } catch (t) {
                    this.logErr(t)
                }
            }).then(t => {
                const {statusCode: s, statusCode: i, headers: r, body: o} = t;
                e(null, {status: s, statusCode: i, headers: r, body: o}, o)
            }, t => {
                const {message: s, response: i} = t;
                e(s, i, i && i.body)
            }))
        }

        post(t, e = (() => {
        })) {
            if (t.body && t.headers && !t.headers["Content-Type"] && (t.headers["Content-Type"] = "application/x-www-form-urlencoded"), t.headers && delete t.headers["Content-Length"], this.isSurge() || this.isLoon()) this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, {"X-Surge-Skip-Scripting": !1})), $httpClient.post(t, (t, s, i) => {
                !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i)
            }); else if (this.isQuanX()) t.method = "POST", this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, {hints: !1})), $task.fetch(t).then(t => {
                const {statusCode: s, statusCode: i, headers: r, body: o} = t;
                e(null, {status: s, statusCode: i, headers: r, body: o}, o)
            }, t => e(t)); else if (this.isNode()) {
                this.initGotEnv(t);
                const {url: s, ...i} = t;
                this.got.post(s, i).then(t => {
                    const {statusCode: s, statusCode: i, headers: r, body: o} = t;
                    e(null, {status: s, statusCode: i, headers: r, body: o}, o)
                }, t => {
                    const {message: s, response: i} = t;
                    e(s, i, i && i.body)
                })
            }
        }

        time(t, e = null) {
            const s = e ? new Date(e) : new Date;
            let i = {
                "M+": s.getMonth() + 1,
                "d+": s.getDate(),
                "H+": s.getHours(),
                "m+": s.getMinutes(),
                "s+": s.getSeconds(),
                "q+": Math.floor((s.getMonth() + 3) / 3),
                S: s.getMilliseconds()
            };
            /(y+)/.test(t) && (t = t.replace(RegExp.$1, (s.getFullYear() + "").substr(4 - RegExp.$1.length)));
            for (let e in i) new RegExp("(" + e + ")").test(t) && (t = t.replace(RegExp.$1, 1 == RegExp.$1.length ? i[e] : ("00" + i[e]).substr(("" + i[e]).length)));
            return t
        }

        msg(e = t, s = "", i = "", r) {
            const o = t => {
                if (!t) return t;
                if ("string" == typeof t) return this.isLoon() ? t : this.isQuanX() ? {"open-url": t} : this.isSurge() ? {url: t} : void 0;
                if ("object" == typeof t) {
                    if (this.isLoon()) {
                        let e = t.openUrl || t.url || t["open-url"], s = t.mediaUrl || t["media-url"];
                        return {openUrl: e, mediaUrl: s}
                    }
                    if (this.isQuanX()) {
                        let e = t["open-url"] || t.url || t.openUrl, s = t["media-url"] || t.mediaUrl;
                        return {"open-url": e, "media-url": s}
                    }
                    if (this.isSurge()) {
                        let e = t.url || t.openUrl || t["open-url"];
                        return {url: e}
                    }
                }
            };
            if (this.isMute || (this.isSurge() || this.isLoon() ? $notification.post(e, s, i, o(r)) : this.isQuanX() && $notify(e, s, i, o(r))), !this.isMuteLog) {
                let t = ["", "==============📣系统通知📣=============="];
                t.push(e), s && t.push(s), i && t.push(i), console.log(t.join("\n")), this.logs = this.logs.concat(t)
            }
        }

        log(...t) {
            t.length > 0 && (this.logs = [...this.logs, ...t]), console.log(t.join(this.logSeparator))
        }

        logErr(t, e) {
            const s = !this.isSurge() && !this.isQuanX() && !this.isLoon();
            s ? this.log("", `❗️${this.name}, 错误!`, t.stack) : this.log("", `❗️${this.name}, 错误!`, t)
        }

        wait(t) {
            return new Promise(e => setTimeout(e, t))
        }

        done(t = {}) {
            const e = (new Date).getTime(), s = (e - this.startTime) / 1e3;
            this.log("", `🔔${this.name}, 结束! 🕛 ${s} 秒`), this.log(), (this.isSurge() || this.isQuanX() || this.isLoon()) && $done(t)
        }
    }(t, e)
}
