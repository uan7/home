/**
 * 下载链接：  http://www.mofamoli.com/h5/reg.html?invite_code=6L1ZGR
 * cron 10 7 * * *  
 * 
 * ========= 青龙--配置文件 ===========
 * # 项目名称:智慧地球
 * export LiHua_zhdq='账号&密码'
 * 
 * 多账号用 换行 或 @ 分割
 * 
 * ====================================
 *   
 */


//--------------------   自定义变量区域 -------------------------------------
const Notify = 1;		 //0为关闭通知,1为打开通知,默认为1


//-------------------- 一般不动变量区域 -------------------------------------
const $ = new Env("智慧地球");
const ckName = "LiHua_zhdq";
//let utils = require("./utils");
const notify = $.isNode() ? require("./sendNotify") : "";
let debug = 0;           //Debug调试   0关闭  1开启
let envSplitor = ["@", "\n"]; //多账号分隔符
let ck = msg = '';       //let ck,msg
let host, hostname;
let userCookie = ($.isNode() ? process.env[ckName] : $.getdata(ckName)) || '';
let userList = [];
let userIdx = 0;
let userCount = 0;
//---------------------- 自定义变量区域 -----------------------------------
//---------------------------------------------------------
async function start() {
    console.log('================== 执行脚本 ==================');
    taskall = [];
    for (let user of userList) {
        console.log(`------------------ 账号${user.index} ------------------`);
        taskall.push(await user.user_login('登录'));
        await wait(1); //延迟
        taskall.push(await user.user_mining('启动'));
    }
    await Promise.all(taskall);
    
}


class UserInfo {
    constructor(str) {
        this.index = ++userIdx;
        this.ck = str.split('&'); //单账号多变量分隔符
        //let ck = str.split('&')
        //this.data1 = ck[0]
        this.host = "www.zhihuidiqiu.com.cn";
        this.hostname = "http://" + this.host;

    }

    async user_login(name) { // 登录
        try {
            let options = {
                method: "Post",
                url: `${this.hostname}/api/v2/auth/login`,
                headers: {
                    'os': 'android',
                    'appVersionCode': '3',
                    'appVersionName': '1.0.2',
                    'Accept': 'application/json',
                    'Local': '1',
                    'Host': 'www.zhihuidiqiu.com.cn',
                    'Connection': 'Keep-Alive',
                    'User-Agent': 'okhttp/4.10.0',
                    'Content-Type': 'application/x-www-form-urlencoded'
                 },
                 body : `account_type=phone&login=${this.ck[0]}&type=2&verifiable_code=&password=${this.ck[1]}`
            };
            //console.log(options);
            let result = await httpRequest(options, name);
            //console.log(result);
            if (result.code == 0) {
                this.token = result.token;
                await this.user_info(),
                await wait(1);
                console.log(`账号[${this.index}]   【${this.name}】登录成功！`);
            } else {
                console.log(`账号[${this.index}]   ${result.message}`);
                //console.log(result);
            }
        } catch (error) {
            console.log(error);
        }
    }
    async user_start(name) { // 启动
        try {
            let options = {
                method: "Post",
                url: `${this.hostname}/api/v2/mining/start`,
                headers: {
                    'os': 'android',
                    'appVersionCode': '3',
                    'appVersionName': '1.0.2',
                    'Accept': 'application/json',
                    'Authorization':`Bearer ` + this.token,
                    'Local': '1',
                    'Host': 'www.zhihuidiqiu.com.cn',
                    'Connection': 'Keep-Alive',
                    'User-Agent': 'okhttp/4.10.0'
                    },
            };
            //console.log(options);
            let result = await httpRequest(options, name);
            //console.log(result);
            console.log(`账号[${this.index}]  智慧地球: 启动！`);
            this.token = result.token;
        } catch (error) {
            console.log(error);
        }
    }
    async user_info() { // 用户信息
        try {
            let options = {
                method: "Get",
                url: `${this.hostname}/api/v2/user`,
                headers: {
                    'os': 'android',
                    'appVersionCode': '3',
                    'appVersionName': '1.0.2',
                    'Accept': 'application/json',
                    'Authorization':`Bearer ` + this.token,
                    'Local': '1',
                    'Host': 'www.zhihuidiqiu.com.cn',
                    'Connection': 'Keep-Alive',
                    'User-Agent': 'okhttp/4.10.0'
                    },
            };
            //console.log(options);
            let result = await httpRequest(options);
            //console.log(result);
            this.name = result.name;
        } catch (error) {
            console.log(error);
        }
    }
    async user_mining(name) { // 启动时间
        try {
            let options = {
                method: "Get",
                url: `${this.hostname}/api/v2/mining`,
                headers: {
                    'os': 'android',
                    'appVersionCode': '3',
                    'appVersionName': '1.0.2',
                    'Accept': 'application/json',
                    'Authorization':`Bearer ` + this.token,
                    'Local': '1',
                    'Host': 'www.zhihuidiqiu.com.cn',
                    'Connection': 'Keep-Alive',
                    'User-Agent': 'okhttp/4.10.0'
                    },
            };
            //console.log(options);
            let result = await httpRequest(options, name);
            //console.log(result);
            this.time = result.count_down;
            if(this.time > 180){
                let Time = secondsToTimeFormat(this.time);
                console.log(`账号[${this.index}]  智慧地球:距离下次爆炸还有${Time}`);
            }else{
                console.log(`账号[${this.index}]  智慧地球:等待${this.time}秒后爆炸！`);
                await wait(this.time + 5);
                await this.user_start('启动');
            }
        } catch (error) {
            console.log(error);
        }
    }

}

!(async () => {
    if (!(await checkEnv())) return;
    if (userList.length > 0) {
        await start();
    }
    await SendMsg(msg);
})()
    .catch((e) => console.log(e))
    .finally(() => $.done());


// #region ********************************************************  固定代码  ********************************************************

// 变量检查与处理
async function checkEnv() {
    if (userCookie) {
        // console.log(userCookie);
        let e = envSplitor[0];
        for (let o of envSplitor)
            if (userCookie.indexOf(o) > -1) {
                e = o;
                break;
            }
            for (let n of userCookie.split(e)) n && userList.push(new UserInfo(n));
        userCount = userList.length;
    } else {
        console.log("未找到CK");
        return;
    }

function randomNum(min, max) {
	if (arguments.length === 0) return Math.random()
	if (!max) max = 10 ** (Math.log(min) * Math.LOG10E + 1 | 0) - 1
	return Math.floor(Math.random() * (max - min + 1) + min);
}

    return console.log('智慧地球注册下载链接：\nhttp://www.mofamoli.com/h5/reg.html?invite_code=6L1ZGR\n'),
    console.log(`================ 共找到${userCount}个账号 ================`), 
    console.log(`脚本执行✌北京时间(UTC+8)：${new Date(new Date().getTime() + new Date().getTimezoneOffset() * 60 * 1000 + 8 * 60 * 60 * 1000).toLocaleString()}`), true;//true == !0
}
// =========================================== 不懂不要动 =========================================================
//秒时间转换
function secondsToTimeFormat(time) {
  let days = parseInt(time / 60 / 60 / 24)
  let hours = parseInt(time / 60 / 60 % 24)
  let minutes = parseInt(time / 60 % 60)
  let seconds = parseInt(time % 60)
  return `${!!days ? days + '天' : ''}${!!hours ? hours + '小时' : ''}${!!minutes ? minutes + '分钟' : ''}${!!seconds ? seconds + '秒' : ''}`
}

//取随机字符串
function getstr(n) {
    let chars = 'qwertyuiopasdfghjklzxcvb1234567890';
    let v = "";
    for(let R = 0; R < n ; R ++) {
        let R_id = Math.ceil(Math.random()*chars.length-1);
        v += chars[R_id];
    }
    return v;
}
function getnum(n) {
    let chars = '1234567890';
    let v = "";
    for(let R = 0; R < n ; R ++) {
        let R_id = Math.ceil(Math.random()*chars.length-1);
        v += chars[R_id];
    }
    return v;
}
//时间戳转时间
function Format_time(){
    //num:0 YYYY-MM-DD  num:1  YYYY-MM-DD hh:mm:ss // timestamp:时间戳
    //将时间戳转换成正常时间格式
    //var date = new Date(timestamp*1000); //时间戳为10位需*1000，时间戳为13位的话不需乘1000
    var date = new Date(new Date().getTime())
    var Y = date.getFullYear() + "-";
    var M =(date.getMonth() + 1 < 10 ? "0" + (date.getMonth() + 1) : date.getMonth() + 1) + "-";
    var D = (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) + " ";
    var h = (date.getHours() < 10 ? "0" + date.getHours() : date.getHours()) + ":" ;
    var m = (date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes()) + ":";
    var s = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds()
    //console.log(Y + M + D + h + m + s)
    let t_time = Y + M + D + h + m + s + '.'+getnum(3)
    return t_time //Y + M + D + h + m + s;
}
// 网络请求 (get, post等)
async function httpRequest(options, name) { var request = require("request"); return new Promise((resolve) => { if (!name) { let tmp = arguments.callee.toString(); let re = /function\s*(\w*)/i; let matches = re.exec(tmp); name = matches[1] } if (debug) { console.log(`\n【debug】===============这是${name}请求信息===============`); console.log(options) } request(options, function (error, response) { if (error) throw new Error(error); let data = response.body; try { if (debug) { console.log(`\n\n【debug】===============这是${name}返回数据==============`); console.log(data) } if (typeof data == "string") { if (isJsonString(data)) { let result = JSON.parse(data); if (debug) { console.log(`\n【debug】=============这是${name}json解析后数据============`); console.log(result) } resolve(result) } else { let result = data; resolve(result) } function isJsonString(str) { if (typeof str == "string") { try { if (typeof JSON.parse(str) == "object") { return true } } catch (e) { return false } } return false } } else { let result = data; resolve(result) } } catch (e) { console.log(error, response); console.log(`\n ${name}失败了!请稍后尝试!!`) } finally { resolve() } }) }) }
// 等待 X 秒
function wait(n) { return new Promise(function (resolve) { setTimeout(resolve, n * 1000) }) }
// 双平台log输出
function DoubleLog(data) { if ($.isNode()) { if (data) { console.log(`${data}`); msg += `${data}` } } else { console.log(`${data}`); msg += `${data}` } }
// 发送消息
async function SendMsg(message) { if (!message) return; if (Notify > 0) { if ($.isNode()) { var notify = require("./sendNotify"); await notify.sendNotify($.name, message) } else { $.msg($.name, '', message) } } else { console.log(message) } }
// 完整 Env
function Env(t, e) { "undefined" != typeof process && JSON.stringify(process.env).indexOf("GITHUB") > -1 && process.exit(0); class s { constructor(t) { this.env = t } send(t, e = "GET") { t = "string" == typeof t ? { url: t } : t; let s = this.get; return "POST" === e && (s = this.post), new Promise((e, i) => { s.call(this, t, (t, s, r) => { t ? i(t) : e(s) }) }) } get(t) { return this.send.call(this.env, t) } post(t) { return this.send.call(this.env, t, "POST") } } return new class { constructor(t, e) { this.name = t, this.http = new s(this), this.data = null, this.dataFile = "box.dat", this.logs = [], this.isMute = !1, this.isNeedRewrite = !1, this.logSeparator = "\n", this.startTime = (new Date).getTime(), Object.assign(this, e), this.log("", `🔔${this.name}, 开始!`) } isNode() { return "undefined" != typeof module && !!module.exports } isQuanX() { return "undefined" != typeof $task } isSurge() { return "undefined" != typeof $httpClient && "undefined" == typeof $loon } isLoon() { return "undefined" != typeof $loon } toObj(t, e = null) { try { return JSON.parse(t) } catch { return e } } toStr(t, e = null) { try { return JSON.stringify(t) } catch { return e } } getjson(t, e) { let s = e; const i = this.getdata(t); if (i) try { s = JSON.parse(this.getdata(t)) } catch { } return s } setjson(t, e) { try { return this.setdata(JSON.stringify(t), e) } catch { return !1 } } getScript(t) { return new Promise(e => { this.get({ url: t }, (t, s, i) => e(i)) }) } runScript(t, e) { return new Promise(s => { let i = this.getdata("@chavy_boxjs_userCfgs.httpapi"); i = i ? i.replace(/\n/g, "").trim() : i; let r = this.getdata("@chavy_boxjs_userCfgs.httpapi_timeout"); r = r ? 1 * r : 20, r = e && e.timeout ? e.timeout : r; const [o, h] = i.split("@"), n = { url: `http://${h}/v1/scripting/evaluate`, body: { script_text: t, mock_type: "cron", timeout: r }, headers: { "X-Key": o, Accept: "*/*" } }; this.post(n, (t, e, i) => s(i)) }).catch(t => this.logErr(t)) } loaddata() { if (!this.isNode()) return {}; { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e); if (!s && !i) return {}; { const i = s ? t : e; try { return JSON.parse(this.fs.readFileSync(i)) } catch (t) { return {} } } } } writedata() { if (this.isNode()) { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e), r = JSON.stringify(this.data); s ? this.fs.writeFileSync(t, r) : i ? this.fs.writeFileSync(e, r) : this.fs.writeFileSync(t, r) } } lodash_get(t, e, s) { const i = e.replace(/\[(\d+)\]/g, ".$1").split("."); let r = t; for (const t of i) if (r = Object(r)[t], void 0 === r) return s; return r } lodash_set(t, e, s) { return Object(t) !== t ? t : (Array.isArray(e) || (e = e.toString().match(/[^.[\]]+/g) || []), e.slice(0, -1).reduce((t, s, i) => Object(t[s]) === t[s] ? t[s] : t[s] = Math.abs(e[i + 1]) >> 0 == +e[i + 1] ? [] : {}, t)[e[e.length - 1]] = s, t) } getdata(t) { let e = this.getval(t); if (/^@/.test(t)) { const [, s, i] = /^@(.*?)\.(.*?)$/.exec(t), r = s ? this.getval(s) : ""; if (r) try { const t = JSON.parse(r); e = t ? this.lodash_get(t, i, "") : e } catch (t) { e = "" } } return e } setdata(t, e) { let s = !1; if (/^@/.test(e)) { const [, i, r] = /^@(.*?)\.(.*?)$/.exec(e), o = this.getval(i), h = i ? "null" === o ? null : o || "{}" : "{}"; try { const e = JSON.parse(h); this.lodash_set(e, r, t), s = this.setval(JSON.stringify(e), i) } catch (e) { const o = {}; this.lodash_set(o, r, t), s = this.setval(JSON.stringify(o), i) } } else s = this.setval(t, e); return s } getval(t) { return this.isSurge() || this.isLoon() ? $persistentStore.read(t) : this.isQuanX() ? $prefs.valueForKey(t) : this.isNode() ? (this.data = this.loaddata(), this.data[t]) : this.data && this.data[t] || null } setval(t, e) { return this.isSurge() || this.isLoon() ? $persistentStore.write(t, e) : this.isQuanX() ? $prefs.setValueForKey(t, e) : this.isNode() ? (this.data = this.loaddata(), this.data[e] = t, this.writedata(), !0) : this.data && this.data[e] || null } initGotEnv(t) { this.got = this.got ? this.got : require("got"), this.cktough = this.cktough ? this.cktough : require("tough-cookie"), this.ckjar = this.ckjar ? this.ckjar : new this.cktough.CookieJar, t && (t.headers = t.headers ? t.headers : {}, void 0 === t.headers.Cookie && void 0 === t.cookieJar && (t.cookieJar = this.ckjar)) } get(t, e = (() => { })) { t.headers && (delete t.headers["Content-Type"], delete t.headers["Content-Length"]), this.isSurge() || this.isLoon() ? (this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.get(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) })) : this.isQuanX() ? (this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t))) : this.isNode() && (this.initGotEnv(t), this.got(t).on("redirect", (t, e) => { try { if (t.headers["set-cookie"]) { const s = t.headers["set-cookie"].map(this.cktough.Cookie.parse).toString(); s && this.ckjar.setCookieSync(s, null), e.cookieJar = this.ckjar } } catch (t) { this.logErr(t) } }).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) })) } post(t, e = (() => { })) { if (t.body && t.headers && !t.headers["Content-Type"] && (t.headers["Content-Type"] = "application/x-www-form-urlencoded"), t.headers && delete t.headers["Content-Length"], this.isSurge() || this.isLoon()) this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.post(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) }); else if (this.isQuanX()) t.method = "POST", this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t)); else if (this.isNode()) { this.initGotEnv(t); const { url: s, ...i } = t; this.got.post(s, i).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) }) } } time(t, e = null) { const s = e ? new Date(e) : new Date; let i = { "M+": s.getMonth() + 1, "d+": s.getDate(), "H+": s.getHours(), "m+": s.getMinutes(), "s+": s.getSeconds(), "q+": Math.floor((s.getMonth() + 3) / 3), S: s.getMilliseconds() }; /(y+)/.test(t) && (t = t.replace(RegExp.$1, (s.getFullYear() + "").substr(4 - RegExp.$1.length))); for (let e in i) new RegExp("(" + e + ")").test(t) && (t = t.replace(RegExp.$1, 1 == RegExp.$1.length ? i[e] : ("00" + i[e]).substr(("" + i[e]).length))); return t } msg(e = t, s = "", i = "", r) { const o = t => { if (!t) return t; if ("string" == typeof t) return this.isLoon() ? t : this.isQuanX() ? { "open-url": t } : this.isSurge() ? { url: t } : void 0; if ("object" == typeof t) { if (this.isLoon()) { let e = t.openUrl || t.url || t["open-url"], s = t.mediaUrl || t["media-url"]; return { openUrl: e, mediaUrl: s } } if (this.isQuanX()) { let e = t["open-url"] || t.url || t.openUrl, s = t["media-url"] || t.mediaUrl; return { "open-url": e, "media-url": s } } if (this.isSurge()) { let e = t.url || t.openUrl || t["open-url"]; return { url: e } } } }; if (this.isMute || (this.isSurge() || this.isLoon() ? $notification.post(e, s, i, o(r)) : this.isQuanX() && $notify(e, s, i, o(r))), !this.isMuteLog) { let t = ["", "==============📣系统通知📣=============="]; t.push(e), s && t.push(s), i && t.push(i), console.log(t.join("\n")), this.logs = this.logs.concat(t) } } log(...t) { t.length > 0 && (this.logs = [...this.logs, ...t]), console.log(t.join(this.logSeparator)) } logErr(t, e) { const s = !this.isSurge() && !this.isQuanX() && !this.isLoon(); s ? this.log("", `❗️${this.name}, 错误!`, t.stack) : this.log("", `❗️${this.name}, 错误!`, t) } wait(t) { return new Promise(e => setTimeout(e, t)) } done(t = {}) { const e = (new Date).getTime(), s = (e - this.startTime) / 1e3; this.log("", `🔔${this.name}, 结束! 🕛 ${s} 秒`), this.log(), (this.isSurge() || this.isQuanX() || this.isLoon()) && $done(t) } }(t, e) }
