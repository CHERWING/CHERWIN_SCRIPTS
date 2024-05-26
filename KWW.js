/**
 *
 * 项目名称：口味王小程序
 * 项目抓包：抓tls-xw.mengniu.cn下的memberId & memberUnionid填入变量
 * 项目变量：KWW
 * 项目定时：每天9，18，20
 * cron: 0 9,18,20 * * *
 * github仓库：https://github.com/CHERWING/CHERWIN_SCRIPTS
 *
 */

//===============脚本版本=================//
let local_version = "2024.05.24";
//=======================================//
const APP_NAME = '口味王小程序'
const $ = new Env('口味王小程序');
const ENV_NAME = 'KWW'

const notify = $.isNode() ? require('./sendNotify') : '';
const Notify = 1 		//0为关闭通知,1为打开通知,默认为1
const JSEncrypt = require('node-jsencrypt');
const axios = require('axios');
const parser = require("@babel/parser");
const fs = require('fs');
const path = require('path');
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
let UserCookie = ($.isNode() ? process.env.KWW : process.env.KWW ) || '';
let SCRIPT_UPDATE = process.env.SCRIPT_UPDATE || true;
// console.log(process.env.KWW)
let UserCookieArr = [];
let data = '';
let msg =``;
let one_msg = '';
let isSign = false;
let signCateId = '';
let signRulesName = '';
let signParamNo = '';
let signOrderNo = '';
let userKeys = 'v1.0';
let formName = 'searchForm';
let memberUnionid = '1';
let qgyUrl = '';
let gameCookie = '';
let loginUrl = '';
let qgyTaskData = [];
let qgySignFlag = false;
let isTravelling = false;
let leftEnergyNum = 0;
let qgyProcess = '';
let greenFruitNum = 0;
let tokenStr = '';
let tokenKeyStr = '';
let qgyToken = '';
let isArticleReadFlag = false;
let articleReadList = [];
let taskBeforeScore = 0;
var timestamp = new Date().getTime();
var trandom = randomNum(1, 28);
let drawTimes = ''
let lessGameCount= 0;
let loveGame_recordId='';
let FKPHtml = ''
let downTime = 0
let pointRain_times = 0
let JFY_URL = ''
let FKP_URL = ''
let pointRain_startId = ''
let pointRain_activityStatus = true
let QGY_inviteCode = []
let AuthorinviteCode= ['IDTCLG','7LUL2L','BZZWJJ']
let AuthorCid = ['4116743840','4094106667','4093679412']
let QGY_canSteal = []
let TYT_URL = ''
let Jump_creditsCostId=''
let Jump_startId=''
let Jump_costResult = false
let Jump_PKstatus = false
console.log('✨✨✨ 口味王会员中心小程序签到✨✨✨\n' +
    '✨ 功能：\n' +
    '      积分签到\n' +
    '      部分积分任务\n' +
    '✨ 抓包步骤：\n' +
    '      打开抓包工具\n' +
    '      打开口味王会员中心小程序\n' +
    '      授权登陆\n' +
    '      找/member/api/info/的URl提取返回[memberId@unionid]（@符号连接）\n' +
    '参数示例：4249095xxxxxx@oWmTE6IqrlDFRzxxxxx\n' +
    '✨ ✨✨wxpusher一对一推送功能，\n' +
    '  ✨需要定义变量export WXPUSHER=wxpusher的app_token，不设置则不启用wxpusher一对一推送\n' +
    '  ✨需要在KWW变量最后添加@wxpusher的UID\n' +
    '✨ 设置青龙变量：\n' +
    'export KWW=\'memberId@unionid@openid参数值\'多账号#或&分割\n' +
    'export SCRIPT_UPDATE = \'False\' 关闭脚本自动更新，默认开启\n' +
    '✨ 推荐cron：0 9 * * *\n' +
    '✨✨✨ @Author CHERWIN✨✨✨')
//=======================================//
UserCookieArr = ENV_SPLIT(UserCookie)
!(async () => {
        if (!(UserCookieArr)) {
            console.log(`未定义${ENV_NAME}变量`)
            process.exit();
        } else {
        // 版本检测
        await getVersion();
        Log(`\n 脚本执行✌北京时间(UTC+8)：${new Date(new Date().getTime() + new Date().getTimezoneOffset() * 60 * 1000 + 8 * 60 * 60 * 1000).toLocaleString()} `)
        console.log(`\n================ 共找到 【${UserCookieArr.length}】 个账号 ================ \n================ 版本对比检查更新 ================`);
        if (await compareVersions(local_version, APP_CONFIG['NEW_VERSION'])){
                Log(`\n 当前版本：${local_version}`)
                Log(`\n 最新版本：${APP_CONFIG['NEW_VERSION']}`)
                if (SCRIPT_UPDATE==true){
                    console.log('开始更新脚本')
                    const fileUrl = `https://github.com/CHERWING/CHERWIN_SCRIPTS/raw/main/${ENV_NAME}.js`;
                    const downloadPath = `./${ENV_NAME}.js`;
                    downloadFile(fileUrl, downloadPath)
                }

        }else{
            console.log(`版本信息：${local_version} ，已是最新版本无需更新开始执行脚本`)
        }

        for (let index = 0; index < UserCookieArr.length; index++) {
            one_msg = ''
            let send_UID = ''
            let num = index + 1
            Log(`\n================ 开始第 【${num}】 个账号 -------->>>>>\n`)
            // console.log(UserCookieArr[index])
            if (num % 4 === 0) {
                console.log('>>>>>>每4个账号等待60秒继续执行')
                await $.wait(1000*60);
            }
            await $.wait(await delay());
            let split_info = UserCookieArr[index].split("@")
            memberId = split_info[0];
            unionid = split_info[1];
            let len_split_info = split_info.length
            let last_info = split_info[len_split_info - 1]
            // await DO_Jump()
            taskBeforeScore = 0;
            await start();
            await $.wait(2000);
            if (isArticleReadFlag) {
                Log(`账号【${num}】: ❌ , 阅读失败,已经完成了`)
            } else {
                await readSubmit();
                await $.wait(2000);
            }
            await $.wait(2000);
            // await activeTaskFlag(2 * 1000)
            await DO_QGY(num);
            // await $.wait(2000);
            // await DO_FKP();已结束
            // await $.wait(5000);
            // await DO_PointRain();已结束
            await $.wait(5000);
            //await DO_Jump();
            //log(`\n==== 积分查询 ====\n`)
            await getMemberScore();

            console.log('\n====== 开始一对一推送 ======')
            if (len_split_info > 0 && last_info.includes("UID_")) {
                console.log(`>检测到设置了UID:【${last_info}】✅`);
                send_UID = last_info
                await send_wxpusher(send_UID,one_msg,APP_NAME);
            }else{
                Log('>未检测到wxpusher UID，不执行一对一推送❌')
            }
            await $.wait(3000);
        }
        // for (let index = 0; index < UserCookieArr.length; index++) {
        //     one_msg = ''
        //     let send_UID = ''
        //     let num = index + 1
        //     Log(`\n================ 开始第 【${num}】 个账号本地互助 -------->>>>>\n`)
        //     await $.wait(await delay());
        //     let split_info = UserCookieArr[index].split("@")
        //     memberId = split_info[0];
        //     unionid = split_info[1];
        //     let len_split_info = split_info.length
        //     let last_info = split_info[len_split_info - 1]
        //
        //     await QGY_help(num)
        //     console.log('\n====== 开始一对一推送 ======')
        //     if (len_split_info > 0 && last_info.includes("UID_")) {
        //         console.log(`>检测到设置了UID:【${last_info}】✅`);
        //         send_UID = last_info
        //         await send_wxpusher(send_UID,one_msg,APP_NAME);
        //     }else{
        //         Log('>未检测到wxpusher UID，不执行一对一推送❌')
        //     }
        //     await $.wait(5000);
        // }
        Log(APP_CONFIG['GLOBAL_NTC'])
        await SendMsg(msg);

    }}
)()
    .catch((e) => log(e))
    .finally(() => $.done())

/**
 * 获取基础信息
 * @returns {Promise<boolean>}
 */
async function start() {
    await getMemberInfo(2 * 1000);
    await $.wait(2000);
    await getMemberScore();
    // await $.wait(2000);
    // await getQgyUrl();
    await $.wait(2000);
    await getMrYdUrl();
    await $.wait(2000);
    // await getOtherUrl();
    // await $.wait(2000);
    await xxsBanner();
    // await $.wait(2000);
    // await getAnswerLists();
    await $.wait(2000);
    await selectTaskList();

    return true;
}
/**
 * 查询会员信息
 * @param timeout
 * @returns {Promise<unknown>}
 */
function getMemberInfo(timeout = 2000) {
    return new Promise((resolve) => {
        let url = {
            url: `https://member.kwwblcj.com/member/api/info/?userKeys=${userKeys}&pageName=member-info-index-search&formName=${formName}&kwwMember.memberId=${memberId}&kwwMember.unionid=${unionid}&memberId=${memberId}`,
            headers: {
                Host: 'member.kwwblcj.com',
                Connection: 'keep-alive',
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'User-Agent': getUA(),
                'content-type': 'application/json',
                Referer: 'https://servicewechat.com/wxfb0905b0787971ad/58/page-frame.html'
            },
        }
        $.get(url, async (error, response, data) => {
            try {
                let result = JSON.parse(data);
                if (result.hasOwnProperty('flag') && result.flag == "T") {
                    userCname = result.result.memberInfo.userCname
                    memberUnionid = result.result.memberInfo.unionid
                    Log(`>登录成功✅`)
                    Log(`>用户名：【${userCname}】`)
                } else {
                    Log(`>登录失败: ❌ ，原因是：${data}`)
                }
            } catch (e) {
                console.log(`>查询会员信息异常❌：${data}，原因：${e}`)
            } finally {
                resolve();
            }
        }, timeout)
    })
}

/**
 * 获取会员积分
 * @returns {Promise<unknown>}
 */
async function getMemberScore(timeout = 2000) {
    Log('====== 获取积分信息 ======')
    return new Promise((resolve) => {
        var options = {
            method: 'GET',
            url: 'https://member.kwwblcj.com/member/api/list/',
            params: {
                userKeys: userKeys,
                pageName: 'select-member-score',
                formName: formName,
                memberId: memberId
            },
            headers: {
                Host: 'member.kwwblcj.com',
                Connection: 'keep-alive',
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'User-Agent': getUA(),
                'content-type': 'application/json',
                'xweb_xhr': '1',
                'user-paramname': 'memberId',
                'Accept': '*/*',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                Referer: 'https://servicewechat.com/wxfb0905b0787971ad/58/page-frame.html'
            },
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                if (data.hasOwnProperty('flag') && data.flag == "T") {
                    if (taskBeforeScore == 0) {
                        taskBeforeScore = data.rows;
                        Log(`>当前积分：${data.rows}`)
                    } else {
                        var calScore = parseInt(data.rows) - parseInt(taskBeforeScore);
                        // Log(`>\n获取积分信息成功✅`)
                        Log(`>执行后积分：${data.rows}，本次获得【${calScore}】积分`)
                    }
                } else {
                    console.log(`>查询积分失败❌，原因是：${data.msg}`)
                }
            } catch (e) {
                log(`>查询积分失败异常：${data}，原因：${e}`)
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
 * 查询任务列表
 * @returns {Promise<unknown>}
 */
async function selectTaskList() {
    console.log('====== 查询签到任务列表 ======')
    return new Promise((resolve) => {
        var options = {
            method: 'GET',
            url: 'https://member.kwwblcj.com/member/api/list/',
            params: {
                userKeys: userKeys,
                pageName: 'select-task-list',
                formName: formName,
                memberId: memberId
            },
            headers: {
                Host: 'member.kwwblcj.com',
                Connection: 'keep-alive',
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'User-Agent': getUA(),
                'content-type': 'application/json',
                Referer: 'https://servicewechat.com/wxfb0905b0787971ad/58/page-frame.html'
            },
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                if (data.hasOwnProperty('flag') && data.flag == "T") {
                    for (var i in data.rows) {
                        var infoId = data.rows[i]['infoId'];
                        var ruleType = data.rows[i]['ruleType'];
                        var complete = data.rows[i]['complete'];
                        if (ruleType == "articleRead") {
                            isArticleReadFlag = (complete == 1) ? true : false;
                        }
                    }
                    console.log(`>获取任务列表成功✅`)
                } else {
                    console.log(`>获取任务列表失败❌`)
                    console.log(`获取任务列表，原因是：${data.msg}`)
                }
            } catch (e) {
                console.log(`获取任务列表异常：${data}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(1, error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
/**
 * 签到
 * @returns {Promise<unknown>}
 */
async function signIn() {
    return new Promise((resolve) => {
        var options = {
            method: 'POST',
            url: 'https://member.kwwblcj.com/member/api/submit/',
            params: {userKeys: userKeys},
            headers: {
                Host: 'member.kwwblcj.com',
                Connection: 'keep-alive',
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'content-type': 'application/json',
                'User-Agent': getUA(),
                Referer: 'https://servicewechat.com/wxfb0905b0787971ad/58/page-frame.html'
            },
            data: {
                pageName: 'AddSignSvmInfo',
                formName: 'addForm',
                orderNo: signOrderNo,
                paramNo: signParamNo,
                cateId: signCateId,
                memberId: memberId,
                memberName: userCname
            }
        };
        axios.request(options).then(function (response) {
            var data = response.data;
            if (data.hasOwnProperty('flag') && data.flag == "T") {
                Log(`签到成功: ✅ ，${signRulesName}获得 ${signParamNo} 积分`)
            } else {
                Log(`签到失败: ❌ ，失败原因是：${data.msg}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
/**
 * 获取资讯
 * @returns {Promise<unknown>}
 */
async function xxsBanner() {
    return new Promise((resolve) => {
        var options = {
            method: 'GET',
            url: 'https://cms2.kwwblcj.com/data/xxsbanner2.json',
            params: {T: timestampMs()},
            headers: {
                Host: 'cms.kwwblcj.com',
                Connection: 'keep-alive',
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'User-Agent': getUA(),
                'content-type': 'application/json',
                Referer: 'https://servicewechat.com/wxfb0905b0787971ad/34/page-frame.html',
            }
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                articleReadList = data.rows;
                log(`获取到${articleReadList.length}条资讯`)
            } catch (e) {
                console.log(`获取资讯信息异常❌：${data}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
/**
 * 阅读信息
 * @returns {Promise<unknown>}
 */
async function readInfo() {
    return new Promise((resolve) => {
        var options = {
            method: 'GET',
            url: 'https://qrcode.kwwblcj.com/qrc/api/info/' + unionid + '/',
            params: {T: timestampMs(), memberId: memberId},
            headers: {
                Host: 'qrcode.kwwblcj.com',
                Connection: 'keep-alive',
                'User-Agent': getUA(),
                'content-type': 'application/json',
                Referer: 'https://servicewechat.com/wxfb0905b0787971ad/34/page-frame.html',
            }
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                if (data.hasOwnProperty('flag') && data.flag == "T") {
                    console.log(`>查询阅读信息成功✅`)
                } else {
                    console.log(`>查询阅读信息失败❌，原因是：${data.msg}`)
                }
            } catch (e) {
                console.log(`>查询阅读信息异常❌：${data}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
/**
 * 提交阅读
 * @returns {Promise<unknown>}
 */
async function readSubmit() {
    var max = articleReadList.length - 1;
    var articleTitle = articleReadList[randomInt(0, max)]['title'];
    return new Promise((resolve) => {
        var options = {
            method: 'GET',
            url: 'https://member.kwwblcj.com/member/api/list/',
            params: {
                userKeys: userKeys,
                pageName: 'setNewsReadTaskFlag',
                formName: 'addForm',
                memberId: memberId,
                userCname: userCname,
                articleTitle: articleTitle
            },
            headers: {
                Host: 'member.kwwblcj.com',
                Connection: 'keep-alive',
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'User-Agent': getUA(),
                'content-type': 'application/json',
                Referer: 'https://servicewechat.com/wxfb0905b0787971ad/34/page-frame.html',
            }
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                if (data.hasOwnProperty('flag') && data.flag == "T") {
                    Log(`每日阅读: 成功✅ ${data.rows}`)
                } else {
                    Log(`每日阅读: 失败❌ 原因是：${data.msg}`)
                }
            } catch (e) {
                console.log(`阅读信息异常❌：${data}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}

async function activeTaskFlag(timeout = 2000) {
    let options = {
        url: `https://member.kwwblcj.com/member/api/list/?userKeys=${userKeys}&pageName=activeTaskFlag&formName=editForm&memberId=${memberId}&userCname=%7F%7F`,
        headers: {
            Host: 'member.kwwblcj.com',
            Connection: 'keep-alive',
            'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
            'user-timestamp': timestamp,
            'user-random': trandom,
            'content-type': 'application/json',
            'User-Agent': getUA(),
            Referer: 'https://servicewechat.com/wxfb0905b0787971ad/58/page-frame.html'
        },
    };
    return new Promise((resolve) => {
        $.get(options, async (error, response, data) => {
            try {
                let result = JSON.parse(data);
                if (result.hasOwnProperty('flag') && result.flag == "T") {
                    console.log(`青果信息: 获取成功✅ 时间：${result.rows}`)
                } else {
                    console.log(`青果信息:  失败❌原因是：${data}`)
                }
            } catch (e) {
                console.log(`点击青果 异常❌：${data}，原因：${e}`)
            } finally {
                resolve();
            }
        }, timeout)
    })
}

/**
 * 登入
 * @param redirect
 * @returns {Promise<unknown>}
 */
async function loginFreePlugin(redirect) {
    return new Promise((resolve) => {
        var options = {
            method: 'GET',
            url: 'https://member.kwwblcj.com/member/api/info/',
            params: {
                userKeys: userKeys,
                pageName: 'loginFreePlugin',
                formName: 'searchForm',
                uid: memberId,
                levelCode: '1',
                redirect: redirect
            },
            headers: {
                Host: 'member.kwwblcj.com',
                Connection: 'keep-alive',
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'content-type': 'application/json',
                'User-Agent': getUA(),
                Referer: 'https://servicewechat.com/wxfb0905b0787971ad/58/page-frame.html'
            }
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                if (data.hasOwnProperty('flag') && data.flag == 'T') {
                    loginUrl = data.result;
                    Log(`>登入成功✅`)
                }
            } catch (e) {
                console.log(`登入异常❌：${data}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
/**
 * 设置cookie
 * @returns {Promise<unknown>}
 */
async function setCookies() {
    return new Promise((resolve) => {
        var host = (loginUrl.split('//')[1]).split('/')[0];
        try {
            request(
                {
                    url: loginUrl,
                    method: "GET",
                    headers: {
                        'Host': host,
                        'Connection': 'keep-alive',
                        'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                        'user-timestamp': timestamp,
                        'user-random': trandom,
                        'Upgrade-Insecure-Requests': '1',
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
                    if (gameCookie){
                        console.log(`>转换Cookie成功！✅`)
                    }else{
                        console.log(`>转换Cookie失败！❌`)
                    }

                })
        } catch (e) {
            console.log(e)
        } finally {
            resolve();
        }
    })
}


/**
 * 完成青果园
 * @param num
 * @returns {Promise<boolean>}
 */
async function DO_QGY(num) {
    console.log('\n--------------------开始嫩青果园活动----------------------')
    qgyUrl = 'https://89420.activity-20.m.duiba.com.cn/projectx/p124e3402/index.html?appID=89420';
    await loginFreePlugin(qgyUrl);
    await $.wait(3000)
    if (loginUrl == "") {
        Log(`账号【${num}】登录青果园异常❌，自动跳过任务！`);
        return false;
    }
    await setCookies();
    await $.wait(3000);
    if (gameCookie == "") {
        Log(`账号【${num}】cookies异常❌，自动跳过任务！`);
        return false;
    }
    var urlMatch = qgyUrl.match('([^/]+)/?$');
    var baseUrl = qgyUrl.replace(urlMatch[0], '');
    await getTokenKeyStr(baseUrl);
    await $.wait(2000);
    await getTokenStr(baseUrl);
    qgyToken = dealToken(tokenStr, tokenKeyStr);
    let isGuide = false
    isGuide = await stepNewGuide(baseUrl, qgyToken)
    while(isGuide == false){
        await $.wait(2000);
        await getTokenStr(baseUrl);
        qgyToken = dealToken(tokenStr, tokenKeyStr);
        await $.wait(2000);
        isGuide = await stepNewGuide()
    }



    await $.wait(2000);
    await getQgyInfo(baseUrl);

    await getTokenStr(baseUrl);
    await $.wait(2000);
    await qgyCheckQuery(baseUrl);
    await $.wait(2000);
    if (qgySignFlag) {
        Log(`>果园签到:  今天已经签到过了！✅`);
    } else {
        Log(`>今日未签到✅`);
        try {
            await getTokenStr(baseUrl);
            await $.wait(2000);
            qgyToken = dealToken(tokenStr, tokenKeyStr);
            await $.wait(2000);
            // await qgyCreateItem(baseUrl, qgyToken)
            await $.wait(await delay());
            await getTokenStr(baseUrl);
            await $.wait(2000);
            qgyToken = dealToken(tokenStr, tokenKeyStr);
            await qgySign(baseUrl, qgyToken);

            if(upNeedNum==null || upNeedNum==0){
                await getTokenStr(baseUrl);
                await $.wait(2000);
                qgyToken = dealToken(tokenStr, tokenKeyStr);
                await collectCoconut(baseUrl, qgyToken)
            }
        } catch (e) {
            Log(`>账号【${num}】青果园签到异常！${e}`);
        }

    }
    if (!isTravelling && greenFruitNum >= 20) {
        try {
            console.log(`>>>准备执行任务:【旅行】`);
            await getTokenStr(baseUrl);
            await $.wait(2000);
            qgyToken = dealToken(tokenStr, tokenKeyStr);
            await $.wait(2000);
            await startTravel(baseUrl, qgyToken);
            await $.wait(2000);
        } catch (e) {
            console.log(`>账号【${num}】青果园旅行异常❌！${e}`);
        }
    } else {
        console.log(`>正在旅行中或青果不足20`);
    }
    await $.wait(2000);
    await queryQgyTask(baseUrl);
    await $.wait(2000);
    if (qgyTaskData.length == 0) {
        Log(`账号【${num}】获取青果园任务异常！❌`);
    } else {
        // console.log(qgyTaskData)
        for (var i in qgyTaskData) {
            // console.log(`>当前任务: 【${title}】`)
            await $.wait(2000);
            var id = qgyTaskData[i]["id"];
            var taskCode = qgyTaskData[i]["code"];
            var title = qgyTaskData[i]["title"];
            var prizePendingCode = qgyTaskData[i]["prizePendingCode"];
            var taskStatus = parseInt(qgyTaskData[i]["taskStatus"]);
            if (taskStatus == 2) {
                console.log(`>任务: 【${title}】已经完成了！✅`);
            }else if(taskStatus == 1 && prizePendingCode){
                console.log(`>任务: 【${title}】待领取！`);
                await getTokenStr(baseUrl);
                await $.wait(2000);
                qgyToken = dealToken(tokenStr, tokenKeyStr);
                await $.wait(2000);
                await sendPrize(baseUrl,taskCode,prizePendingCode,title,qgyToken);
            } else {
                switch (id) {
                    case '1vp2qd9d':// 邀请好友参与种树
                        console.log(`>>>准备执行任务:【${title}】`);
                        await getTokenStr(baseUrl);
                        await $.wait(2000);
                        await get_QGY_InviteCode(baseUrl,dealToken(tokenStr, tokenKeyStr))
                        break;

                    case 'jnb9obsa':// 赠送好友能量
                        console.log(`>>>准备执行任务:【${title}】`);
                        for (var i=0;i<=AuthorCid.length;i++){
                            await getTokenStr(baseUrl);
                            await $.wait(2000);
                            await QGY_giveEnergy(baseUrl,dealToken(tokenStr, tokenKeyStr),AuthorCid[i-1])
                        }
                        break;
                    case '5re9y7rb':// 浏览资讯页
                    case '8pu8vs3s':// 参与海岛跳一跳
                    case 'm2jlv8yb':// 参与欢乐消除
                    case 'wk3mv0k9':// 参与美味连连看
                    case 'irigwir9':// 参与点卤大作战
                        //完成任务
                        console.log(`>>>准备执行任务:【${title}】`);
                        try {
                            await getTokenStr(baseUrl);
                            await $.wait(2000);
                            qgyToken = dealToken(tokenStr, tokenKeyStr);
                            await $.wait(2000);
                            prizePendingCode = await doCompleted(baseUrl, qgyToken, taskCode, title);

                            if (prizePendingCode != ''){
                                await getTokenStr(baseUrl);
                                await $.wait(2000);
                                qgyToken = dealToken(tokenStr, tokenKeyStr);
                                await $.wait(2000);
                                await sendPrize(baseUrl,taskCode,prizePendingCode,title,qgyToken);
                            }

                        } catch (e) {
                            console.log(`>任务:【${title}】异常❌！${e}`);
                        }
                        break;
                    default:
                        console.log(`>任务:【${title}】暂不支持，跳过！`)
                        break;
                }
            }

        }
    }

    if (AuthorinviteCode){
        for(var i = 1;i <= AuthorinviteCode.length;i++){
            await $.wait(2000);
            await getTokenStr(baseUrl);
            qgyToken = dealToken(tokenStr, tokenKeyStr);
            await $.wait(2000);
            await qgyInviteAssist(baseUrl,qgyToken,AuthorinviteCode[i-1])
        }
    }

    await getQgyInfo(baseUrl);

    if (qgyProcess !== 'NaN%') {
        if (leftEnergyNum > 0) {
            var leftEnergyTimes = Math.ceil(leftEnergyNum / 20);;
            console.log(`>可以加能量【${leftEnergyTimes}】次`);
            for (var i = 1; i <= leftEnergyTimes; i++) {
                console.log(`>>开始第 ${i} 次能量加速！`);
                try {
                    await getTokenKeyStr(baseUrl);
                    await $.wait(2000);
                    await getTokenStr(baseUrl);
                    await $.wait(2000);
                    qgyToken = dealToken(tokenStr, tokenKeyStr);
                    await feed(baseUrl, qgyToken)
                } catch (e) {
                    console.log(`>能量加速: 加速异常❌！${e}`);
                }
            }
        } else {
            console.log('>能量不足跳过加速❌')
        }

    } else {
        console.log('>您还是先去种植把！❌')
    }
    await qgyFriendList(baseUrl)
    if (QGY_canSteal.length >0){
        for(var i=0;i<QGY_canSteal.length;i++){
            await getTokenKeyStr(baseUrl);
            await $.wait(2000);
            await getTokenStr(baseUrl);
            await $.wait(2000);
            qgyToken = dealToken(tokenStr, tokenKeyStr);
            var cid = QGY_canSteal[i]
            await qgySteal(qgyToken,cid)
        }
        await $.wait(2000);
    }

    return true;
}

async function QGY_help(num){
    console.log('\n====== 开始嫩青果园本地互助 ======')
    qgyUrl = 'https://89420.activity-20.m.duiba.com.cn/projectx/p124e3402/index.html?appID=89420';
    await loginFreePlugin(qgyUrl);
    await $.wait(3000)
    if (loginUrl == "") {
        Log(`账号【${num}】登录青果园异常❌，自动跳过任务！`);
        return false;
    }
    await setCookies();
    await $.wait(3000);
    if (gameCookie == "") {
        Log(`账号【${num}】cookies异常❌，自动跳过任务！`);
        return false;
    }
    var urlMatch = qgyUrl.match('([^/]+)/?$');
    var baseUrl = qgyUrl.replace(urlMatch[0], '');
    await getTokenKeyStr(baseUrl);
    await $.wait(2000);
    if (QGY_inviteCode){
            console.log('当前全部邀请码：'+QGY_inviteCode)
            for(var i = 1;i <= QGY_inviteCode.length;i++){
                await $.wait(2000);
                await getTokenStr(baseUrl);
                qgyToken = dealToken(tokenStr, tokenKeyStr);
                await $.wait(2000);
                await qgyInviteAssist(baseUrl,qgyToken,QGY_inviteCode[i-1])
            }
    }
}
/**
 * 获取token
 * @param baseUrl
 * @returns {Promise<unknown>}
 */
async function getTokenStr(baseUrl) {
    return new Promise((resolve) => {
        var url = baseUrl + 'getToken';
        var host = (url.split('//')[1]).split('/')[0];
        const options = {
            method: 'GET',
            url: url,
            params: {_t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: baseUrl + '/index.html?appID=89420&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br'
            },
            data: {}
        };
        axios.request(options).then(function (response) {
            try {
                tokenStr = response.data.data;
            } catch (e) {
                console.log(`获取任务: ❌ ，获取失败：${JSON.stringify(response.data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}

/**
 * 青果园签到检查
 * @returns {Promise<unknown>}
 */
async function qgyCheckQuery(baseUrl) {
    console.log('====== 查询青果园签到状态 ======')
    qgySignFlag = false;
    return new Promise((resolve) => {
        var url = baseUrl + 'checkin_1/query.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            params: {_t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {}
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                qgySignFlag = data.data.todaySign;
            } catch (e) {
                console.log(`>果园签到: 状态异常❌：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
/**
 * 青果园助力
 * @returns {Promise<unknown>}
 */
async function qgyInviteAssist(baseUrl,token,inviteCode) {
    // console.log('====== 助力 ======')
    qgySignFlag = false;
    return new Promise((resolve) => {
        var url = baseUrl + 'inviteAssist_1/doAssist.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'POST',
            url: url,
            params: {_t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {inviteCode:inviteCode,token:token,user_type:1,is_from_share:1,_t:timestampMs()}
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                if(data.success){
                    if(AuthorinviteCode.includes(inviteCode)){
                        console.log(`>助力作者成功！感谢您的支持！`)
                    }else{
                        console.log(`>助力【${inviteCode}】成功！`)
                    }

                }else{
                    console.log(`>助力【${inviteCode}】失败！`)

                }
            } catch (e) {
                console.log(`>助力异常❌：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
async function qgyFriendList(baseUrl) {
    console.log('====== 获取好友列表 ======')
    qgySignFlag = false;
    return new Promise((resolve) => {
        var url = baseUrl + 'main/friendRank.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            params: {user_type:1,is_from_share:1,_t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {}
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                if(data.success){
                    var rankList = data.data.rankList
                    for (var i=0;i>rankList.length;i++){
                        var canSteal = rankList[i]['rankList']
                        var cid = rankList[i]['cid']
                        var nickname = rankList[i]['nickname']
                        if (canSteal==true){
                            console.log(`好友：【${nickname}】】可偷取`)
                            QGY_canSteal.push(cid)
                        }
                    }
                }else{
                    console.log(`>获取好友列表失败！`)

                }
            } catch (e) {
                console.log(`>获取好友列表异常❌：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
async function qgySteal(baseUrl,token,cid) {
    console.log('====== 偷取好友能量 ======')
    qgySignFlag = false;
    return new Promise((resolve) => {
        var url = baseUrl + 'main/steal.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            params: {token:token,cid:cid,user_type:1,is_from_share:1,_t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {}
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                if(data.success){
                    var num = data.data.num
                    Log(`>偷取好友成功，获得：【${num}】青果`)
                }else{
                    console.log(`>偷取好友列表失败！`)
                }
            } catch (e) {
                console.log(`>偷取好友异常❌：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
/**
 * 过引导
 * @param baseUrl
 * @param token
 * @returns {Promise<unknown>}
 */
async function stepNewGuide(baseUrl, token) {
    console.log('====== 检测游戏引导 ======')
    return new Promise((resolve) => {
        var url = baseUrl + 'newGuide_1/stepNewGuide.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'POST',
            url: url,
            params: {_t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Origin: 'https://89420.activity-20.m.duiba.com.cn',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
            },
            data: {token: token, user_type: '1', is_from_share: '1', _t: timestampMs()}
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                if(data.code == "200900"){
                    console.log('>已完成游戏引导')
                    return true
                }
                var allGuideSteps = data.data.allGuideSteps;
                var alreadyGuideSteps = data.data.alreadyGuideSteps;
                if (allGuideSteps == alreadyGuideSteps){
                    console.log('>已完成游戏引导')
                    return true
                }else{
                    console.log(`>未完成引导，当前第【${alreadyGuideSteps}】步`)
                    return false
                }
            } catch (e) {
                console.log(`游戏引导异常❌：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
/**
 * 青果园签到
 * @param baseUrl
 * @param token
 * @returns {Promise<unknown>}
 */
async function qgySign(baseUrl, token) {
    return new Promise((resolve) => {
        var url = baseUrl + 'checkin_1/doSign.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'POST',
            url: url,
            params: {_t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                Connection: 'keep-alive',
                'User-Agent': getUA(),
                'Content-Type': 'application/x-www-form-urlencoded',
                Accept: '*/*',
                Referer: qgyUrl + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'en-us,en'
            },
            data: {token: token, user_type: '0', is_from_share: '1', _t: timestampMs()}
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                if (data.hasOwnProperty('data') && data.data.hasOwnProperty('options')) {
                    qgySignFlag = true;
                    Log(`果园签到: 成功✅，${data.data.options[0].optionName}`)
                } else {
                    Log(`果园签到: 失败❌：${JSON.stringify(data)}，原因：${e}`)
                }

            } catch (e) {
                console.log(`青果园签到异常：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
/**
 * 获取每日阅读地址
 * @returns {Promise<unknown>}
 */
async function getMrYdUrl() {
    console.log('====== 获取每日阅读地址 ======')
    return new Promise((resolve) => {
        var options = {
            method: 'GET',
            url: 'https://cms.kwwblcj.com/data/c02.json',
            params: {T: timestampMs(), memberId: memberId},
            headers: {
                Host: 'cms.kwwblcj.com',
                Connection: 'keep-alive',
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'content-type': 'application/json',
                'User-Agent': getUA(),
                Referer: 'https://servicewechat.com/wxfb0905b0787971ad/58/page-frame.html'
            }
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                for (var i in data.rows) {
                    var url = data.rows[i]["url"];
                    var title = data.rows[i]["title"];
                    if (url.indexOf('https') >= 0 && title.indexOf('每日阅读') >= 0) {
                        mrYdUrl = url;
                        //log(`获取${title}地址成功✅`);
                        return
                    }
                }
            } catch (e) {
                log(`获取每日阅读异常❌：${data}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
/**
 * 获取其他地址
 * @returns {Promise<unknown>}
 */
async function getOtherUrl() {
    return new Promise((resolve) => {
        var options = {
            method: 'GET',
            url: 'https://cms.kwwblcj.com/data/c05.json',
            params: {T: timestampMs(), memberId: memberId},
            headers: {
                Host: 'cms.kwwblcj.com',
                Connection: 'keep-alive',
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'content-type': 'application/json',
                'User-Agent': getUA(),
                Referer: 'https://servicewechat.com/wxfb0905b0787971ad/58/page-frame.html'
            }
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                for (var i in data.rows) {
                    var url = data.rows[i]["url"];
                    var title = data.rows[i]["title"];
                    var manuscriptId = data.rows[i]["manuscriptId"];
                    if (title.indexOf('每日答题') >= 0 && url.indexOf('https') >= 0) {
                        mrDtUrl = url+"&from=login&spm=89420.1.1.1";
                        Log(`获取${title}地址成功✅`)
                    } else if (title.indexOf('天降好礼') >= 0 && url.indexOf('https') >= 0) {
                        tjUrl = url;
                        Log(`获取${title}地址成功✅`)
                    } else if (title.indexOf('海岛游乐场') >= 0 && url.indexOf('https') >= 0) {
                        hdUrl = url;
                        Log(`获取${title}地址成功✅`)
                    } else if (title.indexOf('疯狂摇奖机') >= 0 && url.indexOf('https') >= 0) {
                        yjjUrl = url;
                        Log(`获取${title}地址成功✅`)
                    }
                }
            } catch (e) {
                log(`查询其他地址异常：${data}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
/**
 * 翻牌次数查询
 * @returns {Promise<unknown>}
 */
async function fkpindex(baseUrl) {
    return new Promise((resolve) => {
        var url = baseUrl + 'main/index.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            params: { user_type: '1', is_from_share: '1', _t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {}
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                drawTimes = data.data.drawTimes;
                if (drawTimes > 0){
                    console.log(`>可翻牌【${drawTimes}】次`)
                    return true
                }else{
                    console.log(`>无翻牌次数`)
                    return false
                }

            } catch (e) {
                console.log(`>获取可翻牌次数失败: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
async function openBox(baseUrl,token) {
    Log('====== 开始开宝箱  ======')
    return new Promise((resolve) => {
        var url = baseUrl + 'main/openBox.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            params: { token: token, user_type: '1', is_from_share: '1', _t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {}
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                if (data.code == "500009"){
                    Log(`开宝箱次数不足`);
                    return
                }
                if (data.data.prizeName){
                     let prizeName = data.data.prizeName;
                    Log(`开宝箱获得：【${prizeName}】`)
                }else if(data.message){
                    Log(data.message)
                }else{
                    console.log(data)
                }

                return drawTimes
            } catch (e) {
                console.log(`开宝箱失败: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
async function fkp_draw(baseUrl,token) {
    Log('====== 开始翻牌  ======')
    return new Promise((resolve) => {
        var url = baseUrl + 'main/draw.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            params: { place: 1, token: token, user_type: '1', is_from_share: '1', _t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {}
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                if (data.data.prizeId){
                     let prizeId = data.data.prizeId;
                    Log(`翻牌获得：【${prizeId}】`)
                }else if(data.message){
                    Log(data.message)
                }else{
                    console.log(data)
                }

                return drawTimes
            } catch (e) {
                console.log(`翻牌失败: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
/**
 * 获取翻卡牌html
 * @returns {Promise<unknown>}
 */
async function getFKPHtml() {
    return new Promise((resolve) => {
        var url = FKP_URL + '&from=login&spm=89420.1.1.1';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: FKP_URL + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {}
        };
        axios.request(options).then(function (response) {
            FKPHtml = response.data;
            console.log(FKPHtml)
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
/**
 * 找爱游戏
 * @returns {Promise<unknown>}
 */
async function loveGame_gameIndex(baseUrl,Token) {
    console.log('====== 访问找爱游戏 ======')
    return new Promise((resolve) => {
        var url = baseUrl + 'loveGame/gameIndex.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            params: { token:Token,user_type: '1', is_from_share: '1', _t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: FKP_URL + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {}
        };
        axios.request(options).then(function (response) {

            try {
                var data = response.data;
                // console.log(data)
                lessGameCount = data.data.lessGameCount;
                downTime = data.data.downTime;
                console.log(`可参与找爱游戏次数：${lessGameCount}次`);
                if (downTime != null){
                    lessGameCount = 1
                }else{
                   downTime = 0
                }


            } catch (e) {
                console.log(`获取游戏次数失败: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
/**
 * 找爱游戏
 * @returns {Promise<unknown>}
 */
async function loveGame_startGame(baseUrl,Token) {
    console.log('====== 开始获取找爱游戏ID ======')
    return new Promise((resolve) => {
        var url = baseUrl + 'loveGame/startGame.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            params: { token:Token,user_type: '1', is_from_share: '1', _t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: FKP_URL + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {}
        };
        axios.request(options).then(function (response) {

            try {
                var data = response.data;
                if(data.code == "500004"){
                    loveGame_recordId = ''
                    console.log(`>游戏次数不足`)
                    $.wait(1)
                }else{
                    loveGame_recordId = data.data.recordId;
                    console.log(`>获取游戏ID成功：${loveGame_recordId}`)
                }

            } catch (e) {
                console.log(`>获取游戏ID失败: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
/**
 * 找爱游戏
 * @returns {Promise<unknown>}
 */
async function loveGame_submitGame(baseUrl,Token) {
    return new Promise((resolve) => {
        var url = baseUrl + 'loveGame/submitGame.do';
        var host = (url.split('//')[1]).split('/')[0];

        var req_time = timestampMs()
        // console.log(loveGame_recordId)
        // console.log(req_time)
        var req_sign = `recordId=${loveGame_recordId}&score=3&time=${req_time}&salt=9m9shb1mskjam1`
        // console.log(req_sign)
        req_sign = MD5Encrypt(req_sign)
        // console.log(req_sign)
        var options = {
            method: 'GET',
            url: url,
            params: { recordId:loveGame_recordId,token:Token,sign:req_sign,user_type: '1',score: '3', is_from_share: '1',time: req_time, _t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: FKP_URL + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {}
        };
        axios.request(options).then(function (response) {

            let prizeCount;
            try {
                var data = response.data;

                if (data.success){
                    prizeCount = data.data.prizeCount;
                    Log(`>获得翻牌机会：${prizeCount}✅`)
                }else{
                    Log(`>提交游戏结果失败: ❌`)
                }

            } catch (e) {
                console.log(`>提交游戏结果失败: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
async function pointRain_gameIndex(baseUrl,Token) {
    console.log('====== 访问积分雨活动页 ======')
    return new Promise((resolve) => {
        var url = baseUrl + 'points/index.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            params: { token:Token,user_type: '1', is_from_share: '1', _t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: JFY_URL,
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {}
        };
        axios.request(options).then(function (response) {

            try {
                var data = response.data;
                // console.log(data)
                pointRain_times = data.data.times;
                activityStatus = data.data.activityStatus;
                if (activityStatus != '2'){
                    pointRain_activityStatus = false;
                    console.log(`>积分雨活动结束❌`);
                }else{
                    pointRain_activityStatus = true;
                    console.log(`>可参与积分雨次数：${pointRain_times}次`);
                }



            } catch (e) {
                console.log(`获取游戏次数失败: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
async function pointRain_startGame(baseUrl,Token) {
    console.log('====== 开始积分雨游戏 ======')
    return new Promise((resolve) => {
        var url = baseUrl + 'points/start.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            // token=p7f4e9c7&user_type=1&is_from_share=1&_t=1715620488721
            params: { token:Token,user_type: '1', is_from_share: '1', _t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: FKP_URL + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {}
        };
        axios.request(options).then(function (response) {

            try {
                var data = response.data;
                // console.log(data)
                pointRain_startId = data.data.startId;
                console.log(`获取游戏ID成功：${pointRain_startId}`)
            } catch (e) {
                console.log(`获取游戏ID失败: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
/**
 * 找爱游戏
 * @returns {Promise<unknown>}
 */
async function pointRain_submitGame(baseUrl,Token) {
    console.log('====== 提交积分雨分数 ======')
    return new Promise((resolve) => {
        var url = baseUrl + 'points/submit.do';
        var host = (url.split('//')[1]).split('/')[0];
        // console.log(pointRain_startId)
        // console.log(req_time)score startId ulugE8zIZeTU3tDNKtohw false
        var score =randomInt(350, 400)
        var req_sign = `${score}${pointRain_startId}ulugE8zIZeTU3tDNKtohwfalse`
        // console.log(req_sign)
        req_sign = MD5Encrypt(req_sign)
        // console.log(req_sign)
        var options = {
            method: 'GET',
            url: url,
            // score=224&extra=false&startId=723246932&sign=c55b7c0cf24b4b38d08c8e3ca510409e&token=p0fd5174&user_type=1&is_from_share=1&_t=1715621049442
            params: { score: score,extra: false,startId:pointRain_startId,sign:req_sign,token:Token,user_type: '1', is_from_share: '1', _t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: FKP_URL + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {}
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                var points = data.data.points;
                Log(`>获得：${points}积分`)
            } catch (e) {
                console.log(`提交游戏结果失败: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
async function DO_FKP(num) {
    console.log('\n--------------------开始翻卡牌活动----------------------')
    FKP_URL= 'https://89420.activity-20.m.duiba.com.cn/projectx/p9027e011/index.html?appID=89420'
    await loginFreePlugin(FKP_URL);
    await $.wait(2000)
    if (loginUrl == "") {
        Log(`账号【${num}】登录翻卡牌异常❌，自动跳过任务！`);
        return false;
    }
    await setCookies();
    await $.wait(2000);
    if (gameCookie == "") {
        Log(`账号【${num}】cookies异常❌，自动跳过任务！`);
        return false;
    }

    var urlMatch = FKP_URL.match('([^/]+)/?$');
    var baseUrl = FKP_URL.replace(urlMatch[0], '');
    await $.wait(2000);
    await fkpindex(baseUrl);

    await getTokenKeyStr(baseUrl);
    await getTokenStr(baseUrl);
    await loveGame_gameIndex(baseUrl, dealToken(tokenStr, tokenKeyStr))
    // console.log(lessGameCount)
    await $.wait(2000);
    while (lessGameCount != 0){
        //①每日首次登录活动获得1次游戏机会，通关后获得1次免费翻卡牌机会；
        //②完成首次通关，倒计时30秒后获得1次游戏机会，通关获得1次免费翻卡牌机会；
        //③完成第2次通关，倒计时1分钟后获得1次机会，通关后获得1次免费翻卡牌机会；
        //④完成第3次通关，倒计时3分钟后获得1次机会，通关后获得1次免费翻卡牌机会；
        //⑤完成第4次通关，倒计时5分钟后获得1次机会，通关后获得1次免费翻卡牌机会。

        console.log('====== 开始找爱游戏 ======')

        await getTokenStr(baseUrl);
        await $.wait(2000);
        let Token = dealToken(tokenStr, tokenKeyStr);
        await loveGame_startGame(baseUrl, Token)
        if (loveGame_recordId!=''){
            await getTokenStr(baseUrl);
            await $.wait(2000);
            let Token = dealToken(tokenStr, tokenKeyStr);
            await loveGame_submitGame(baseUrl, Token)
        }
        await $.wait(2000);
        await getTokenStr(baseUrl);
        await $.wait(2000);
        await loveGame_gameIndex(baseUrl, dealToken(tokenStr, tokenKeyStr))

        await $.wait(2000);
        if (downTime!=0){
            console.log(`>暂停${downTime+5000}毫秒秒可继续游戏`)
            await $.wait(downTime+5000);
        }


    }

    await fkpindex(baseUrl)
    await $.wait(2000);
    if(drawTimes > 0){
        for (var i=1;i<=drawTimes;i++){
            console.log(`开始第【${i}】次翻牌`)
            await getTokenKeyStr(baseUrl);
            await getTokenStr(baseUrl);
            await $.wait(2000);
            await fkp_draw(baseUrl,dealToken(tokenStr, tokenKeyStr))
        }
    }
    await getTokenKeyStr(baseUrl);
    await getTokenStr(baseUrl);
    await $.wait(2000);
    await openBox(baseUrl,dealToken(tokenStr, tokenKeyStr))


}
async  function DO_PointRain(){
    console.log('\n--------------------开始积分雨活动----------------------')
    JFY_URL= 'https://89420.activity-20.m.duiba.com.cn/projectx/p03c58ec7/index.html?appID=89420'
    urlMatch = JFY_URL.match('([^/]+)/?$');
    baseUrl = JFY_URL.replace(urlMatch[0], '');
    // console.log(baseUrl)
    await loginFreePlugin(JFY_URL);
    await $.wait(3000)
    if (loginUrl == "") {
        Log(`账号【${num}】登录积分雨异常❌，自动跳过任务！`);
        return false;
    }
    await setCookies();
    await $.wait(3000);
    if (gameCookie == "") {
        Log(`账号【${num}】积分雨cookies异常❌，自动跳过任务！`);
        return false;
    }
    await $.wait(2000);
    await getTokenKeyStr(baseUrl);
    await getTokenStr(baseUrl);
    await $.wait(2000);
    await pointRain_gameIndex(baseUrl, dealToken(tokenStr, tokenKeyStr))
    if (!pointRain_activityStatus){
        return false;
    }
    if (pointRain_times!=0){
        console.log('开始积分雨游戏')
        await $.wait(2000);
        await getTokenKeyStr(baseUrl);
        await $.wait(2000);
        await getTokenStr(baseUrl);
        await $.wait(2000);
        await pointRain_startGame(baseUrl, dealToken(tokenStr, tokenKeyStr))
        console.log('等待20秒提交分数')
        await $.wait(1000*20);
        if(pointRain_startId != '' ||pointRain_startId != undefined){
            // await getTokenKeyStr(baseUrl);
            await $.wait(2000);
            await getTokenStr(baseUrl);
            await $.wait(2000);
            await pointRain_submitGame(baseUrl, dealToken(tokenStr, tokenKeyStr))
        }

    }



}

async  function DO_Jump(){
    console.log('\n--------------------开始跳一跳游戏----------------------')
    TYT_URL= 'https://89420.activity-20.m.duiba.com.cn/projectx/p60459935/index.html?appID=89420'
    let urlMatch = TYT_URL.match('([^/]+)/?$');
    let baseUrl = TYT_URL.replace(urlMatch[0], '');
    // console.log(baseUrl)
    await loginFreePlugin(TYT_URL);
    await $.wait(3000)
    if (loginUrl == "") {
        Log(`账号【${num}】登录跳一跳异常❌，自动跳过任务！`);
        return false;
    }
    await setCookies();
    await $.wait(3000);
    if (gameCookie == "") {
        Log(`账号【${num}】跳一跳cookies异常❌，自动跳过任务！`);
        return false;
    }

    await $.wait(2000);
    await Jump_creditsCost(baseUrl)
    if (Jump_creditsCostId != ''){
        await $.wait(2000);
        await Jump_queryStatus(baseUrl,Jump_creditsCostId)
        if (Jump_costResult == true){
            await $.wait(2000);
            await getTokenKeyStr(baseUrl);
            await getTokenStr(baseUrl);
            await Jump_start(baseUrl,dealToken(tokenStr, tokenKeyStr),Jump_creditsCostId)
            if (Jump_startId != ''){

                while (Jump_PKstatus == false){
                    await Jump_queryPkStatus(baseUrl,Jump_startId)
                    await $.wait(1000);
                }

            console.log('等待30秒提交分数')
            await $.wait(1000*30);
            await getTokenStr(baseUrl);
            await Jump_submit(baseUrl,dealToken(tokenStr, tokenKeyStr))

            }






        }
    }

}

async function Jump_creditsCost(baseUrl) {
    console.log('====== 开始创建跳一跳订单 ======')
    return new Promise((resolve) => {
        var url = baseUrl + 'credits/creditsCost.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            // token=p7f4e9c7&user_type=1&is_from_share=1&_t=1715620488721
            params: {
                toPlaywayId: 'matching',
                toActionId: 'start',
                credits: 10,
                desc: 'sub_credits_desc',
                user_type: 1,
                is_from_share:1,
                _t: timestampMs()
            },
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: TYT_URL + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {
            }
        };
        axios.request(options).then(function (response) {

            try {
                var data = response.data;
                // console.log(data)
                if (data.success) {
                    Jump_creditsCostId = data.data
                    console.log(`获取订单ID成功：${Jump_creditsCostId}`)
                }


            } catch (e) {
                console.log(`获取游戏ID失败: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}

async function Jump_queryStatus(baseUrl,ticketNum) {
    console.log('====== 开始提交跳一跳订单 ======')
    return new Promise((resolve) => {
        var url = baseUrl + 'credits/queryStatus.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            // credits/queryStatus.do?ticketNum=p604599358ef4ba9928d241ed278c33e&user_type=1&is_from_share=1&_t=1716222238997
            params: {
                ticketNum: ticketNum,
                user_type: 1,
                is_from_share:1,
                _t: timestampMs()
            },
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: TYT_URL + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {
            }
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                console.log(data)
                if (data.success) {
                    console.log(`订单成功`)
                    Jump_costResult = true

                }else{
                    console.log(`订单失败❌`)
                    Jump_costResult = false
                }
            } catch (e) {
                console.log(`获取游戏ID失败: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
                Jump_costResult = false
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}

async function Jump_start(baseUrl,token,ticketNum) {
    console.log('====== 开始跳一跳游戏 ======')
    return new Promise((resolve) => {
        var url = baseUrl + 'matching/start.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            // matching/start.do?ticketNum=p604599358ef4ba9928d241ed278c33e&token=pc5f12d2&user_type=1&is_from_share=1&_t=1716222239241
            params: {
                ticketNum: ticketNum,
                user_type: 1,
                token: token,
                is_from_share:1,
                _t: timestampMs()
            },
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: TYT_URL + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {
            }
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                console.log(data)
                if (data.success) {
                    Jump_startId = data.data.startId
                    console.log(`开始跳一跳游戏成功,ID:【${Jump_startId}】`)
                    return true
                }else{
                    console.log(`开始跳一跳游戏失败❌`)
                    return false
                }
            } catch (e) {
                console.log(`开始跳一跳游戏失败: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
                return false
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}

async function Jump_queryPkStatus(baseUrl,startId) {
    console.log('====== 开始匹配对手 ======')
    return new Promise((resolve) => {
        var url = baseUrl + 'matching/queryPkStatus.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            // https://89420.activity-20.m.duiba.com.cn/projectx/p60459935/matching/queryPkStatus.do?startId=4116743840_1716231400126&user_type=1&is_from_share=1&_t=1716231389780
            params: {
                startId: startId,
                user_type: 1,
                is_from_share:1,
                _t: timestampMs()
            },
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: TYT_URL + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {
            }
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                console.log(data)
                if (data.success) {
                    if (data.data.status == '2'){
                        console.log(`匹配对手成功,`)
                        Jump_PKstatus = true
                        return true
                    }else{
                        console.log(`匹配对手失败❌`)
                        Jump_PKstatus = false
                    }

                }else{
                    console.log(`匹配对手失败❌`)
                    Jump_PKstatus = false
                    return false
                }
            } catch (e) {
                console.log(`开始跳一跳游戏失败: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
                Jump_PKstatus = false
                return false
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}


async function Jump_submit(baseUrl,startId) {
    console.log('====== 开始跳一跳游戏 ======')
    return new Promise((resolve) => {
        var url = baseUrl + 'matching/submit.do';
        var host = (url.split('//')[1]).split('/')[0];
        var currScore = randomInt(350, 400)
        // startId+currScore+'1'+timestampMs()+'duibatiaoyitiao'
        t = timestampMs()
        var sign = MD5Encrypt(`${startId}${currScore}1${t}duibatiaoyitiao`)
        console.log(`签名数据：【${startId}${currScore}1${timestampMs()}duibatiaoyitiao】`)
        console.log(`SIGN：【${sign}】`)
        var options = {
            method: 'POST',
            url: url,
            // matching/start.do?ticketNum=p604599358ef4ba9928d241ed278c33e&token=pc5f12d2&user_type=1&is_from_share=1&_t=1716222239241
            params: {
                _t: t
            },
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, t, trandom).toLowerCase(),
                'user-timestamp': t,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: TYT_URL + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {
                startId: startId,
                score: currScore,
                type: 1,
                timestamp: t,
                sign: sign,
                token: 1,
                user_type: 1,
                is_from_share:1
            }
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                console.log(data)
                // if (data.success) {
                //     Jump_startId = data.data.startId
                //     console.log(`开始跳一跳游戏成功,ID:【${Jump_startId}】`)
                //     return true
                // }else{
                //     console.log(`开始跳一跳游戏失败❌`)
                //     return false
                // }
            } catch (e) {
                console.log(`开始跳一跳游戏失败: ❌ , 状态异常：${JSON.stringify(data)}，原因：${e}`)
                return false
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}



/**
 * 获取
 * @returns {Promise<boolean>}
 */
async function getAnswerLists() {
    answerLists = JSON.parse('{"1":1,"2":1,"3":1,"4":1,"5":4,"6":1,"7":1,"8":1,"9":1,"10":1,"11":1,"12":1,"13":2,"14":1,"15":2,"16":1,"17":2,"18":2,"19":1,"20":1,"21":4,"22":1,"23":4,"24":1,"25":3,"26":1,"27":4,"28":1,"29":4,"30":4,"31":1,"32":4,"33":1,"34":1,"35":1,"36":1,"37":4,"38":1,"39":3,"40":4,"41":2,"42":1,"43":2,"44":4,"45":4,"46":2,"47":1,"48":1,"49":1,"50":2,"51":4,"52":4,"53":1,"54":3,"55":3,"56":4,"57":4,"58":4,"59":1,"60":4,"61":1,"62":1,"63":1,"64":2,"65":1,"66":3,"67":1,"68":1,"69":4,"70":4,"71":4,"72":1,"73":4,"74":2,"75":4,"76":4,"77":4,"78":1,"79":2,"80":1,"81":2,"82":3,"83":3,"84":4,"85":1,"86":2,"87":3,"88":2,"89":4,"90":2,"91":4,"92":3,"93":4,"94":2,"95":3,"96":2,"97":3,"98":2,"99":4,"100":4,"101":4,"102":3,"103":4,"104":4,"105":4,"106":4}');
    return true;
}

/**
 * 获取签到信息
 * @param timeout
 * @returns {Promise<unknown>}
 */
async function getSignInfo(timeout = 2000) {
    signCateId = '';
    isSign = false;
    let options = {
        url: `https://member.kwwblcj.com/member/api/list/?userKeys=${userKeys}&pageName=selectSignInfo&formName=searchForm&memberId=${memberId}`,
        headers: {
            Host: 'member.kwwblcj.com',
            Connection: 'keep-alive',
            'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
            'user-timestamp': timestamp,
            'user-random': trandom,
            'content-type': 'application/json',
            'User-Agent': getUA(),
            Referer: 'https://servicewechat.com/wxfb0905b0787971ad/58/page-frame.html'
        },
    };
    return new Promise((resolve) => {
        $.get(options, async (error, response, data) => {
            try {
                let result = JSON.parse(data);
                if (result.hasOwnProperty('flag') && result.flag == "T") {
                    var nowDate = time("yyyy-MM-dd");
                    for (var i in result.rows.data) {
                        var actionDate = result.rows.data[i]["actionDate"];
                        var cateId = result.rows.data[i]["cateId"];
                        var flag = result.rows.data[i]["flag"];
                        if (actionDate == nowDate) {
                            signCateId = cateId;
                            signRulesName = result.rows.data[i]["rulesName"];
                            signParamNo = result.rows.data[i]["paramNo"];
                            signOrderNo = result.rows.data[i]["orderNo"];
                            if (flag == 1) {
                                isSign = true;
                            } else {
                                isSign = false;
                            }
                        }
                    }
                    console.log(`查询签到信息成功✅`)
                } else {
                    console.log(`查询签到信息失败❌，原因是：${data}`)
                }
            } catch (e) {
                console.log(`查询签到信息异常❌：${data}，原因：${e}`)
            } finally {
                resolve();
            }
        }, timeout)
    })
}

/**
 * 查询接口
 * @param timeout
 * @returns {Promise<unknown>}
 */
async function dbInterface(timeout = 2000) {
    let options = {
        url: `https://member.kwwblcj.com/member/api/info/?userKeys=${userKeys}&pageName=dbInterface&formName=treeStatus&uid=${memberId}`,
        headers: {
            Host: 'member.kwwblcj.com',
            Connection: 'keep-alive',
            'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
            'user-timestamp': timestamp,
               'user-random': trandom,
            'content-type': 'application/json',
            'User-Agent': getUA(),
            Referer: 'https://servicewechat.com/wxfb0905b0787971ad/58/page-frame.html'
        },
    };
    return new Promise((resolve) => {
        $.get(options, async (error, response, data) => {
            try {
                let result = JSON.parse(data);
                if (result.hasOwnProperty('flag') && result.flag == "T") {
                    //Log(`接口${result.msg}`)
                } else {
                    console.log(`查询接口失败❌，原因是：${data}`)
                }
            } catch (e) {
                console.log(`查询接口异常❌：${data}，原因：${e}`)
            } finally {
                resolve();
            }
        }, timeout)
    })
}

/**
 * 能力加速
 * @param baseUrl
 * @param token
 * @returns {Promise<unknown>}
 */
async function feed(baseUrl, token) {
    return new Promise((resolve) => {
        var url = baseUrl + 'main/feed.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            params: {token:token,user_type:1,is_from_share:1,_t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'Content-Type': 'application/x-www-form-urlencoded',
                Origin: 'https://89420.activity-20.m.duiba.com.cn',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&shareCode=BZZWJJ&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
            },
            data: {

            }
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                console.log(`>能量加速成功✅`)
            } catch (e) {
                console.log(`>能量失败❌ ，原因：${data.message}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
async function collectCoconut(baseUrl, token) {
    console.log('====== 果园收取青果 ======')
    return new Promise((resolve) => {
        var url = baseUrl + '/main/charge.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'POST',
            url: url,
            params: {token:token,user_type:1,is_from_share:1,_t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'Content-Type': 'application/x-www-form-urlencoded',
                Origin: 'https://89420.activity-20.m.duiba.com.cn',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&shareCode=BZZWJJ&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
            },
            data: {
            }
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                Log(`>收取青果成功✅`)
            } catch (e) {
                console.log(`>收取青果失败❌ ，原因：${data.message}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })

}
/**
 * 获取信息
 * @param baseUrl
 * @returns {Promise<unknown>}
 */
async function getQgyInfo(baseUrl) {
    console.log('====== 获取果园信息 ======')
    return new Promise(async(resolve) => {
        var url = baseUrl + 'main/index.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            params: {user_type: '1', is_from_share: '1', _t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&shareCode=BZZWJJ&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
            },
            data: {}
        };
        axios.request(options).then(async function (response) {
            try {
                var data = response.data;
                if (data.hasOwnProperty('data') && data.data.hasOwnProperty('treeInfo')) {
                    energyNum = data.data.treeInfo.energyNum;
                    upNeedNum = data.data.treeInfo.upNeedNum;
                    isTravelling = data.data.travel;
                    leftEnergyNum = data.data.leftEnergyNum
                    greenFruitNum = data.data.greenFruitNum
                    qgyProcess = ((energyNum / upNeedNum) * 100).toFixed(2) + "%"
                    console.log(`>>>获取信息成功✅`)
                    Log(`>当前进度：${qgyProcess}\n>能量：${leftEnergyNum}\n>青果：${greenFruitNum}`)
                } else {
                    console.log(`>获取信息失败❌：${JSON.stringify(data)}`)
                }
            } catch (e) {
                console.log(`>获取信息异常❌：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })

}
/**
 * 查询青果园任务
 * @param baseUrl
 * @returns {Promise<unknown>}
 */
async function queryQgyTask(baseUrl) {
    console.log('====== 获取青果园任务列表 ======')
    qgyTaskData = [];
    var url = baseUrl + 'task_1/queryTasks.do';
    var host = (url.split('//')[1]).split('/')[0];
    return new Promise((resolve) => {
        var options = {
            method: 'GET',
            url: url,
            params: {user_type: '1', is_from_share: '1', _t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&shareCode=BZZWJJ&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br'
            },
            data: {}
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                if (data.hasOwnProperty('data')) {
                    console.log(`>获取果园任务列表成功✅`)
                    qgyTaskData = data.data.item;
                }else{
                    console.log(`>获取果园任务列表失败❌`)
                }

            } catch (e) {
                console.log(`获取果园任务列表异常❌：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })

}

/**
 * 完成青果园任务
 * @param baseUrl
 * @param token
 * @param taskCode
 * @param taskTitle
 * @returns {Promise<unknown>}
 */
async function doCompleted(baseUrl, token, taskCode, taskTitle) {
    // Log('====== 执行青果')
    return new Promise((resolve) => {
        var url = baseUrl + 'task_1/doCompleted.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'POST',
            url: url,
            params: {_t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Origin: 'https://89420.activity-20.m.duiba.com.cn',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&shareCode=BZZWJJ&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
            },
            data: {
                taskCode: taskCode,
                token: token,
                user_type: '1',
                is_from_share: '1',
                _t: timestampMs()
            }
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                if (data.hasOwnProperty('success') && data.success) {
                    console.log(`>已完成【${taskTitle}】任务，获得：【${data.data.completedSize}】能量✅`)
                    let prizePendingCode = data.data.prizePendingCode
                    return prizePendingCode
                } else {
                    console.log(`>完成【${taskTitle}】任务失败❌：${data.message}`)
                    return ''
                }
            } catch (e) {
                console.log(`>完成【${taskTitle}】任务异常❌：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })

}

/**
 * 领取奖励信息
 * @param baseUrl
 * @returns {Promise<unknown>}
 */
async function sendPrize(baseUrl,taskCode,PendingCode,title,qgyToken) {
    // Log('====== 领取任务奖励 ======')
    return new Promise((resolve) => {
        var url = baseUrl + 'task_1/sendPrize.do?_t='+ timestampMs();
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'POST',
            url: url,
            // taskCode=browse_finishQuestion&prizePendingCode=f28349f41b7e4232ab7be68476245120&token=p78683bb&user_type=1&is_from_share=1&_t=1715794521686
            params: {},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&shareCode=BZZWJJ&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            },
            data: {taskCode: taskCode, prizePendingCode: PendingCode,token: qgyToken,user_type: 1, is_from_share: '1', _t: timestampMs()}
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                Log(`>领取【${title}】奖励成功✅。`)
            } catch (e) {
                console.log(`>领取【${title}】奖励失败❌：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}
async function get_QGY_InviteCode(baseUrl, token) {
    // Log('====== 执行青果')
    return new Promise((resolve) => {
        var url = baseUrl + 'inviteAssist_1/getInviteCode.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            params: {_t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Origin: 'https://89420.activity-20.m.duiba.com.cn',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&shareCode=BZZWJJ&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
            },
            data: {}
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                if (data.hasOwnProperty('success') && data.success) {
                    var inviteCode = data.data.inviteCode
                    console.log(`>获取邀请码成功：【${inviteCode}】✅`)
                    QGY_inviteCode.push(inviteCode)
                    console.log('当前全部邀请码：'+QGY_inviteCode)
                    return QGY_inviteCode
                } else {
                    console.log(`>完成【${taskTitle}】任务失败❌：${data.message}`)
                    return ''
                }
            } catch (e) {
                console.log(`>完成【${taskTitle}】任务异常❌：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })

}

async function QGY_giveEnergy(baseUrl, token,cid) {
    // Log('====== 执行青果')
    return new Promise((resolve) => {
        var url = baseUrl + 'main/giveEnergy.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            // main/giveEnergy.do?cid=4093679412&token=paeb87e2&user_type=1&is_from_share=1&_t=1715877738068
            params: {cid:cid,token:token,user_type:1,is_from_share:1,_t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Origin: 'https://89420.activity-20.m.duiba.com.cn',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&shareCode=BZZWJJ&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
            },
            data: {}
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                if (data.hasOwnProperty('success') && data.success) {
                    console.log(`>赠送能量成功！(不消耗自身能量)✅`)

                } else {
                    console.log(`>赠送好友能量失败❌：${data.message}`)

                }
            } catch (e) {
                console.log(`>完成【${taskTitle}】任务异常❌：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })

}

/**
 * 获取tokenKey
 * @param baseUrl
 * @returns {Promise<unknown>}
 */
async function getTokenKeyStr(baseUrl) {
    return new Promise((resolve) => {
        var url = baseUrl + 'getTokenKey';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'GET',
            url: url,
            params: {_t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                Accept: '*/*',
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                Connection: 'keep-alive',
                'User-Agent': getUA(),
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                Referer: baseUrl + 'index.html?appID=89420&from=login&spm=89420.1.1.1',
            }
        };
        axios.request(options).then(function (response) {
            try {
                tokenKeyStr = response.data;
                log(`>获取tokenKey成功✅`)
            } catch (e) {
                log(`>获取tokenKey失败❌：${JSON.stringify(data)}，原因：${e}`)
            }
        }).catch(function (error) {
            console.error(error);
        }).then(res => {
            //这里处理正确返回
            resolve();
        });
    })
}



/**
 * 开始旅行
 * @param baseUrl
 * @param token
 * @returns {Promise<unknown>}
 */
async function startTravel(baseUrl, token) {
    return new Promise((resolve) => {
        var url = baseUrl + 'customTask1/startTravel.do';
        var host = (url.split('//')[1]).split('/')[0];
        var options = {
            method: 'POST',
            url: url,
            params: {_t: timestampMs()},
            headers: {
                cookie: gameCookie,
                Host: host,
                'user-sign': getUserSign(memberId, timestamp, trandom).toLowerCase(),
                'user-timestamp': timestamp,
                'user-random': trandom,
                'Content-Type': 'application/x-www-form-urlencoded',
                Origin: 'https://89420.activity-20.m.duiba.com.cn',
                Connection: 'keep-alive',
                Accept: '*/*',
                'User-Agent': getUA(),
                Referer: qgyUrl + '&from=login&spm=89420.1.1.1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
            },
            data: {token: token, user_type: '1', is_from_share: '1', _t: timestampMs()}
        };
        axios.request(options).then(function (response) {
            try {
                var data = response.data;
                Log(`果园旅行: 成功✅${data.success}`)
            } catch (e) {
                console.log(`果园旅行: 失败❌：${JSON.stringify(data)}，原因：${e}`)
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
async function send_wxpusher(UID, send_msg, title, help=false) {
    const WXPUSHER = process.env.WXPUSHER || false;
    if (WXPUSHER) {
        console.log('>WXPUSHER变量已设置✅')
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
                    console.log(">>>一对一推送成功！✅");
                } else {
                    console.error(`>>>一对一推送消息发送失败❌。错误信息：${response.data.msg}`);
                }
            })
            .catch(error => {
                console.error(`>>>一对一推送发送消息时发生错误❌：${error.message}`);
            });
    }else{
        console.log('>未设置WXPUSHER变量，取消一对一推送❌')
    }
}


// ============================================变量检查============================================ \\
function ENV_SPLIT(input_str) {
    var parts = [];
    if (input_str.includes('&')) {
        var amp_parts = input_str.split('&');
        for (var i = 0; i < amp_parts.length; i++) {
            if (amp_parts[i].includes('#')) {
                var hash_parts = amp_parts[i].split('#');
                for (var j = 0; j < hash_parts.length; j++) {
                    parts.push(hash_parts[j]);
                }
            } else {
                parts.push(amp_parts[i]);
            }
        }
        return parts;
    } else if (input_str.includes('#')) {
        var hash_parts = input_str.split('#');
        return hash_parts;
    } else {
        var out_str = input_str.toString();
        return [out_str];
    }
}


function saveUserData(fileName, newData) {
    try {
        let data;
        try {
            // 读取现有的 JSON 文件（如果存在）
            data = JSON.parse(fs.readFileSync(fileName, 'utf8'));
        } catch (err) {
            // 如果文件不存在，创建所需目录并一个新的空 JSON 文件
            if (err.code === 'ENOENT') {
                const directory = path.dirname(fileName);
                if (!fs.existsSync(directory)) {
                    fs.mkdirSync(directory, { recursive: true });
                }
                data = {};
            } else {
                throw err;
            }
        }

        // 检查是否已存在相同的键，如果存在，合并数据
        for (const key in newData) {
            if (newData.hasOwnProperty(key)) {
                if (data.hasOwnProperty(key)) {
                    // 如果键已存在，将新数据合并到现有数据中
                    Object.assign(data[key], newData[key]);
                } else {
                    // 如果键不存在，直接插入新数据
                    data[key] = newData[key];
                }
            }
        }

        // 将更新后的数据写入 JSON 文件
        fs.writeFileSync(fileName, JSON.stringify(data, null, 4));
        console.log(`数据已保存到文件 ${fileName}`);
    } catch (err) {
        console.error(`保存数据到 ${fileName} 时发生错误：`, err);
    }
}
// 读取用户数据
function readUserData(filename) {
    try {
        if (fs.existsSync(filename)) {
            return JSON.parse(fs.readFileSync(filename, 'utf8'));
        } else {
            console.log(`文件 ${filename} 不存在，返回空对象`);
            return {};
        }
    } catch (err) {
        console.error(`读取 ${filename} 时发生错误：`, err);
        return null;
    }
}
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
                console.log('更新成功！✅，请重新运行脚本');
                process.exit();
                resolve();
            });
            // 监听 'error' 事件，处理错误
            fileStream.on('error', function(err) {
                console.error('更新失败❌，请手动更新:', error);
                console.error('写入文件时发生错误:', err);
                reject(err);
            });
        });
    } catch (error) {
        console.error('下载文件时发生错误:', error);
        throw error;
    }
}
async function compareVersions(localVersion, serverVersion) {
    const localParts = localVersion.split('.'); // 将本地版本号拆分成数字部分
    const serverParts = serverVersion.split('.'); // 将服务器版本号拆分成数字部分

    for (let i = 0; i < localParts.length && i < serverParts.length; i++) {
        const localNum = parseInt(localParts[i]);
        const serverNum = parseInt(serverParts[i]);

        if (localNum < serverNum) {
            return true; // 当前版本低于服务器版本
        } else if (localNum > serverNum) {
            return false; // 当前版本高于服务器版本
        }
    }

    // 如果上述循环没有返回结果，则表示当前版本与服务器版本的数字部分完全相同
    if (localParts.length < serverParts.length) {
        return true; // 当前版本位数较短，即版本号形如 x.y 比 x.y.z 低
    } else {
        return false; // 当前版本与服务器版本相同或更高
    }
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
	if ($.isNode()) {
		if (data) {
			console.log(`${data}`);
			msg += `${data}\n`;
            one_msg += `${data}<br>`;
		}
	} else {
		console.log(`${data}`);
		msg += `${data}\n`;
        one_msg += `${data}<br>`;
	}
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
function dealToken(tokenStr, tokenKeyStr) {
    let scriptToken, scriptKey;
    scriptToken = DealScriptStr(tokenStr);
    scriptKey = DealScriptStr(tokenKeyStr);
    let tdom = new JSDOM(
        `<script>${scriptToken}</script><script>${scriptKey}</script>`,
        {
            runScripts: 'dangerously'
        }
    )
    let str = scriptKey;
    var babelStr;
    str = str.replaceAll(/eval/g, 'var babelStr=');
    str = str.replaceAll(/\\u0065\\u0076\\u0061\\u006c/g, 'var babelStr=')
    eval(str);
    eval(babelStr);
    let ast = parser.parse(babelStr);
    let funcStr = ast.program.body[0].id.name;
    // console.log(ast.program.body);
    let res = tdom.window[funcStr]();
    // console.log(tdom.window);
    tdom.window.close();
    //console.log(window['pf8b6b']);
    return res;
}
function DealScriptStr(str) {
    str = str.replace(/\/\*.*?\*\//g, ' ');
    str = str.replace(/\b0(\d+)/g, '0o$1');
    return str;
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
var i,  l = ["A", "Z", "B", "Y", "C", "X", "D", "T", "E", "S", "F", "R", "G", "Q", "H", "P", "I", "O", "J", "N", "k", "M", "L", "a", "c", "d", "f", "h", "k", "p", "y", "n"];
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
function timestampMs(){
    return new Date().getTime();
}

/**
 *
 * 获取秒时间戳
 */
function timestampS(){
    return Date.parse(new Date())/1000;
}


/**
 * 修改配置文件
 */
function modify() {
    fs.readFile('/ql/data/config/config.sh','utf8',function(err,dataStr){
        if(err){
            return log('读取文件失败！'+err)
        }
        else {
            var result = dataStr.replace(/regular/g,string);
            fs.writeFile('/ql/data/config/config.sh', result, 'utf8', function (err) {
                if (err) {return log(err);}
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
                // console.log(ntc)
                const globalNtcHtml = config['GLOBAL_NTC_HTML'];
                const globalNtc= config['GLOBAL_NTC'];
                // console.log(globalNtc)
                // 将获取到的值作为对象返回
                APP_CONFIG ={ 'NEW_VERSION':newVersion, 'NTC':ntc, 'GLOBAL_NTC_HTML':globalNtcHtml,'GLOBAL_NTC':globalNtc }
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
function MD5Encrypt(a) { function b(a, b) { return a << b | a >>> 32 - b } function c(a, b) { var c, d, e, f, g; return e = 2147483648 & a, f = 2147483648 & b, c = 1073741824 & a, d = 1073741824 & b, g = (1073741823 & a) + (1073741823 & b), c & d ? 2147483648 ^ g ^ e ^ f : c | d ? 1073741824 & g ? 3221225472 ^ g ^ e ^ f : 1073741824 ^ g ^ e ^ f : g ^ e ^ f } function d(a, b, c) { return a & b | ~a & c } function e(a, b, c) { return a & c | b & ~c } function f(a, b, c) { return a ^ b ^ c } function g(a, b, c) { return b ^ (a | ~c) } function h(a, e, f, g, h, i, j) { return a = c(a, c(c(d(e, f, g), h), j)), c(b(a, i), e) } function i(a, d, f, g, h, i, j) { return a = c(a, c(c(e(d, f, g), h), j)), c(b(a, i), d) } function j(a, d, e, g, h, i, j) { return a = c(a, c(c(f(d, e, g), h), j)), c(b(a, i), d) } function k(a, d, e, f, h, i, j) { return a = c(a, c(c(g(d, e, f), h), j)), c(b(a, i), d) } function l(a) { for (var b, c = a.length, d = c + 8, e = (d - d % 64) / 64, f = 16 * (e + 1), g = new Array(f - 1), h = 0, i = 0; c > i;)b = (i - i % 4) / 4, h = i % 4 * 8, g[b] = g[b] | a.charCodeAt(i) << h, i++; return b = (i - i % 4) / 4, h = i % 4 * 8, g[b] = g[b] | 128 << h, g[f - 2] = c << 3, g[f - 1] = c >>> 29, g } function m(a) { var b, c, d = "", e = ""; for (c = 0; 3 >= c; c++)b = a >>> 8 * c & 255, e = "0" + b.toString(16), d += e.substr(e.length - 2, 2); return d } function n(a) { a = a.replace(/\r\n/g, "\n"); for (var b = "", c = 0; c < a.length; c++) { var d = a.charCodeAt(c); 128 > d ? b += String.fromCharCode(d) : d > 127 && 2048 > d ? (b += String.fromCharCode(d >> 6 | 192), b += String.fromCharCode(63 & d | 128)) : (b += String.fromCharCode(d >> 12 | 224), b += String.fromCharCode(d >> 6 & 63 | 128), b += String.fromCharCode(63 & d | 128)) } return b } var o, p, q, r, s, t, u, v, w, x = [], y = 7, z = 12, A = 17, B = 22, C = 5, D = 9, E = 14, F = 20, G = 4, H = 11, I = 16, J = 23, K = 6, L = 10, M = 15, N = 21; for (a = n(a), x = l(a), t = 1732584193, u = 4023233417, v = 2562383102, w = 271733878, o = 0; o < x.length; o += 16)p = t, q = u, r = v, s = w, t = h(t, u, v, w, x[o + 0], y, 3614090360), w = h(w, t, u, v, x[o + 1], z, 3905402710), v = h(v, w, t, u, x[o + 2], A, 606105819), u = h(u, v, w, t, x[o + 3], B, 3250441966), t = h(t, u, v, w, x[o + 4], y, 4118548399), w = h(w, t, u, v, x[o + 5], z, 1200080426), v = h(v, w, t, u, x[o + 6], A, 2821735955), u = h(u, v, w, t, x[o + 7], B, 4249261313), t = h(t, u, v, w, x[o + 8], y, 1770035416), w = h(w, t, u, v, x[o + 9], z, 2336552879), v = h(v, w, t, u, x[o + 10], A, 4294925233), u = h(u, v, w, t, x[o + 11], B, 2304563134), t = h(t, u, v, w, x[o + 12], y, 1804603682), w = h(w, t, u, v, x[o + 13], z, 4254626195), v = h(v, w, t, u, x[o + 14], A, 2792965006), u = h(u, v, w, t, x[o + 15], B, 1236535329), t = i(t, u, v, w, x[o + 1], C, 4129170786), w = i(w, t, u, v, x[o + 6], D, 3225465664), v = i(v, w, t, u, x[o + 11], E, 643717713), u = i(u, v, w, t, x[o + 0], F, 3921069994), t = i(t, u, v, w, x[o + 5], C, 3593408605), w = i(w, t, u, v, x[o + 10], D, 38016083), v = i(v, w, t, u, x[o + 15], E, 3634488961), u = i(u, v, w, t, x[o + 4], F, 3889429448), t = i(t, u, v, w, x[o + 9], C, 568446438), w = i(w, t, u, v, x[o + 14], D, 3275163606), v = i(v, w, t, u, x[o + 3], E, 4107603335), u = i(u, v, w, t, x[o + 8], F, 1163531501), t = i(t, u, v, w, x[o + 13], C, 2850285829), w = i(w, t, u, v, x[o + 2], D, 4243563512), v = i(v, w, t, u, x[o + 7], E, 1735328473), u = i(u, v, w, t, x[o + 12], F, 2368359562), t = j(t, u, v, w, x[o + 5], G, 4294588738), w = j(w, t, u, v, x[o + 8], H, 2272392833), v = j(v, w, t, u, x[o + 11], I, 1839030562), u = j(u, v, w, t, x[o + 14], J, 4259657740), t = j(t, u, v, w, x[o + 1], G, 2763975236), w = j(w, t, u, v, x[o + 4], H, 1272893353), v = j(v, w, t, u, x[o + 7], I, 4139469664), u = j(u, v, w, t, x[o + 10], J, 3200236656), t = j(t, u, v, w, x[o + 13], G, 681279174), w = j(w, t, u, v, x[o + 0], H, 3936430074), v = j(v, w, t, u, x[o + 3], I, 3572445317), u = j(u, v, w, t, x[o + 6], J, 76029189), t = j(t, u, v, w, x[o + 9], G, 3654602809), w = j(w, t, u, v, x[o + 12], H, 3873151461), v = j(v, w, t, u, x[o + 15], I, 530742520), u = j(u, v, w, t, x[o + 2], J, 3299628645), t = k(t, u, v, w, x[o + 0], K, 4096336452), w = k(w, t, u, v, x[o + 7], L, 1126891415), v = k(v, w, t, u, x[o + 14], M, 2878612391), u = k(u, v, w, t, x[o + 5], N, 4237533241), t = k(t, u, v, w, x[o + 12], K, 1700485571), w = k(w, t, u, v, x[o + 3], L, 2399980690), v = k(v, w, t, u, x[o + 10], M, 4293915773), u = k(u, v, w, t, x[o + 1], N, 2240044497), t = k(t, u, v, w, x[o + 8], K, 1873313359), w = k(w, t, u, v, x[o + 15], L, 4264355552), v = k(v, w, t, u, x[o + 6], M, 2734768916), u = k(u, v, w, t, x[o + 13], N, 1309151649), t = k(t, u, v, w, x[o + 4], K, 4149444226), w = k(w, t, u, v, x[o + 11], L, 3174756917), v = k(v, w, t, u, x[o + 2], M, 718787259), u = k(u, v, w, t, x[o + 9], N, 3951481745), t = c(t, p), u = c(u, q), v = c(v, r), w = c(w, s); var O = m(t) + m(u) + m(v) + m(w); return O.toLowerCase() }
// 完整 Env
function Env(t, e) { "undefined" != typeof process && JSON.stringify(process.env).indexOf("GITHUB") > -1 && process.exit(0); class s { constructor(t) { this.env = t } send(t, e = "GET") { t = "string" == typeof t ? { url: t } : t; let s = this.get; return "POST" === e && (s = this.post), new Promise((e, i) => { s.call(this, t, (t, s, r) => { t ? i(t) : e(s) }) }) } get(t) { return this.send.call(this.env, t) } post(t) { return this.send.call(this.env, t, "POST") } } return new class { constructor(t, e) { this.name = t, this.http = new s(this), this.data = null, this.dataFile = "box.dat", this.logs = [], this.isMute = !1, this.isNeedRewrite = !1, this.logSeparator = "\n", this.startTime = (new Date).getTime(), Object.assign(this, e), this.log("", `🔔${this.name}, 开始!`) } isNode() { return "undefined" != typeof module && !!module.exports } isQuanX() { return "undefined" != typeof $task } isSurge() { return "undefined" != typeof $httpClient && "undefined" == typeof $loon } isLoon() { return "undefined" != typeof $loon } toObj(t, e = null) { try { return JSON.parse(t) } catch { return e } } toStr(t, e = null) { try { return JSON.stringify(t) } catch { return e } } getjson(t, e) { let s = e; const i = this.getdata(t); if (i) try { s = JSON.parse(this.getdata(t)) } catch { } return s } setjson(t, e) { try { return this.setdata(JSON.stringify(t), e) } catch { return !1 } } getScript(t) { return new Promise(e => { this.get({ url: t }, (t, s, i) => e(i)) }) } runScript(t, e) { return new Promise(s => { let i = this.getdata("@chavy_boxjs_userCfgs.httpapi"); i = i ? i.replace(/\n/g, "").trim() : i; let r = this.getdata("@chavy_boxjs_userCfgs.httpapi_timeout"); r = r ? 1 * r : 20, r = e && e.timeout ? e.timeout : r; const [o, h] = i.split("@"), n = { url: `http://${h}/v1/scripting/evaluate`, body: { script_text: t, mock_type: "cron", timeout: r }, headers: { "X-Key": o, Accept: "*/*" } }; this.post(n, (t, e, i) => s(i)) }).catch(t => this.logErr(t)) } loaddata() { if (!this.isNode()) return {}; { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e); if (!s && !i) return {}; { const i = s ? t : e; try { return JSON.parse(this.fs.readFileSync(i)) } catch (t) { return {} } } } } writedata() { if (this.isNode()) { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e), r = JSON.stringify(this.data); s ? this.fs.writeFileSync(t, r) : i ? this.fs.writeFileSync(e, r) : this.fs.writeFileSync(t, r) } } lodash_get(t, e, s) { const i = e.replace(/\[(\d+)\]/g, ".$1").split("."); let r = t; for (const t of i) if (r = Object(r)[t], void 0 === r) return s; return r } lodash_set(t, e, s) { return Object(t) !== t ? t : (Array.isArray(e) || (e = e.toString().match(/[^.[\]]+/g) || []), e.slice(0, -1).reduce((t, s, i) => Object(t[s]) === t[s] ? t[s] : t[s] = Math.abs(e[i + 1]) >> 0 == +e[i + 1] ? [] : {}, t)[e[e.length - 1]] = s, t) } getdata(t) { let e = this.getval(t); if (/^@/.test(t)) { const [, s, i] = /^@(.*?)\.(.*?)$/.exec(t), r = s ? this.getval(s) : ""; if (r) try { const t = JSON.parse(r); e = t ? this.lodash_get(t, i, "") : e } catch (t) { e = "" } } return e } setdata(t, e) { let s = !1; if (/^@/.test(e)) { const [, i, r] = /^@(.*?)\.(.*?)$/.exec(e), o = this.getval(i), h = i ? "null" === o ? null : o || "{}" : "{}"; try { const e = JSON.parse(h); this.lodash_set(e, r, t), s = this.setval(JSON.stringify(e), i) } catch (e) { const o = {}; this.lodash_set(o, r, t), s = this.setval(JSON.stringify(o), i) } } else s = this.setval(t, e); return s } getval(t) { return this.isSurge() || this.isLoon() ? $persistentStore.read(t) : this.isQuanX() ? $prefs.valueForKey(t) : this.isNode() ? (this.data = this.loaddata(), this.data[t]) : this.data && this.data[t] || null } setval(t, e) { return this.isSurge() || this.isLoon() ? $persistentStore.write(t, e) : this.isQuanX() ? $prefs.setValueForKey(t, e) : this.isNode() ? (this.data = this.loaddata(), this.data[e] = t, this.writedata(), !0) : this.data && this.data[e] || null } initGotEnv(t) { this.got = this.got ? this.got : require("got"), this.cktough = this.cktough ? this.cktough : require("tough-cookie"), this.ckjar = this.ckjar ? this.ckjar : new this.cktough.CookieJar, t && (t.headers = t.headers ? t.headers : {}, void 0 === t.headers.Cookie && void 0 === t.cookieJar && (t.cookieJar = this.ckjar)) } get(t, e = (() => { })) { t.headers && (delete t.headers["Content-Type"], delete t.headers["Content-Length"]), this.isSurge() || this.isLoon() ? (this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.get(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) })) : this.isQuanX() ? (this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t))) : this.isNode() && (this.initGotEnv(t), this.got(t).on("redirect", (t, e) => { try { if (t.headers["set-cookie"]) { const s = t.headers["set-cookie"].map(this.cktough.Cookie.parse).toString(); s && this.ckjar.setCookieSync(s, null), e.cookieJar = this.ckjar } } catch (t) { this.logErr(t) } }).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) })) } post(t, e = (() => { })) { if (t.body && t.headers && !t.headers["Content-Type"] && (t.headers["Content-Type"] = "application/x-www-form-urlencoded"), t.headers && delete t.headers["Content-Length"], this.isSurge() || this.isLoon()) this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.post(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) }); else if (this.isQuanX()) t.method = "POST", this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t)); else if (this.isNode()) { this.initGotEnv(t); const { url: s, ...i } = t; this.got.post(s, i).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) }) } } time(t, e = null) { const s = e ? new Date(e) : new Date; let i = { "M+": s.getMonth() + 1, "d+": s.getDate(), "H+": s.getHours(), "m+": s.getMinutes(), "s+": s.getSeconds(), "q+": Math.floor((s.getMonth() + 3) / 3), S: s.getMilliseconds() }; /(y+)/.test(t) && (t = t.replace(RegExp.$1, (s.getFullYear() + "").substr(4 - RegExp.$1.length))); for (let e in i) new RegExp("(" + e + ")").test(t) && (t = t.replace(RegExp.$1, 1 == RegExp.$1.length ? i[e] : ("00" + i[e]).substr(("" + i[e]).length))); return t } msg(e = t, s = "", i = "", r) { const o = t => { if (!t) return t; if ("string" == typeof t) return this.isLoon() ? t : this.isQuanX() ? { "open-url": t } : this.isSurge() ? { url: t } : void 0; if ("object" == typeof t) { if (this.isLoon()) { let e = t.openUrl || t.url || t["open-url"], s = t.mediaUrl || t["media-url"]; return { openUrl: e, mediaUrl: s } } if (this.isQuanX()) { let e = t["open-url"] || t.url || t.openUrl, s = t["media-url"] || t.mediaUrl; return { "open-url": e, "media-url": s } } if (this.isSurge()) { let e = t.url || t.openUrl || t["open-url"]; return { url: e } } } }; if (this.isMute || (this.isSurge() || this.isLoon() ? $notification.post(e, s, i, o(r)) : this.isQuanX() && $notify(e, s, i, o(r))), !this.isMuteLog) { let t = ["", "==============📣系统通知📣=============="]; t.push(e), s && t.push(s), i && t.push(i), console.log(t.join("\n")), this.logs = this.logs.concat(t) } } log(...t) { t.length > 0 && (this.logs = [...this.logs, ...t]), console.log(t.join(this.logSeparator)) } logErr(t, e) { const s = !this.isSurge() && !this.isQuanX() && !this.isLoon(); s ? this.log("", `❗️${this.name}, 错误!`, t.stack) : this.log("", `❗️${this.name}, 错误!`, t) } wait(t) { return new Promise(e => setTimeout(e, t)) } done(t = {}) { const e = (new Date).getTime(), s = (e - this.startTime) / 1e3; this.log("", `🔔${this.name}, 结束! 🕛 ${s} 秒`), this.log(), (this.isSurge() || this.isQuanX() || this.isLoon()) && $done(t) } }(t, e) }
