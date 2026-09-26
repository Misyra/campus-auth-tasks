# Campus-Auth 任务仓库

Campus-Auth 的校园网登录任务共享仓库。

## 索引文件

**浏览器任务与直连任务各有一份索引**，分别对应 Campus-Auth 任务页的「浏览器任务」「直连任务」两个子页——两类任务的**任务文件结构完全不同**（前者是浏览器步骤，后者是 HTTP 请求形状），故分开收录、不混装：

| 索引 | 内容 | GitHub（主） | Gitee（镜像） |
|------|------|--------------|---------------|
| `index.json` | 浏览器任务 | `https://raw.githubusercontent.com/Misyra/campus-auth-tasks/master/index.json` | `index.gitee.json` |
| `index.http.json` | 直连任务 | `https://raw.githubusercontent.com/Misyra/campus-auth-tasks/master/index.http.json` | `index.http.gitee.json` |

Gitee 镜像索引是主索引的副本，条目内容相同，仅把 `url`（以及 `screenshot`）换成 Gitee raw 地址；**每份索引各有自己的镜像文件**，两份都要同步维护。

## 使用方式

在 Campus-Auth 的任务管理页面，点击 **从仓库导入** 即可浏览和安装任务：「浏览器任务」子页读 `index.json`，「直连任务」子页读 `index.http.json`。

> 国内用户如访问 GitHub 不稳定，可在导入弹窗把「来源」切到 **Gitee**（读上面两份镜像索引），或直接打开：
> ```
> https://raw.giteeusercontent.com/Misyra/campus-auth-tasks/raw/master/index.gitee.json
> https://raw.giteeusercontent.com/Misyra/campus-auth-tasks/raw/master/index.http.gitee.json
> ```

## 任务列表

### 浏览器任务（`index.json`）

| 任务 | 说明 |
|------|------|
| **通用登录** | 语义识别表单，兼容大多数认证页面 |
| **华中科技大学校园网登录** | 需先点击密码占位元素激活真实输入框 |
| **南京师范大学中北学院校园网登录** | 丹阳校区 Dr.COM 认证，支持运营商选择、自动重试一次 |
| **四川大学校园网登录** | HK Posi 认证，支持运营商选择 |
| **大连大学校园网登录** | 通用账号密码登录流程 |
| **信阳师范大学校园网登录** | 锐捷 Ruijie ePortal，无需选择运营商 |
| **广东电信天翼校园网登录** | 字母数字混合验证码（OCR 识别），附门户截图 |
| **四川旅游学院校园网登录** | 隐藏输入框自动填充，支持服务选择、条件验证码识别，附门户截图 |

### 直连任务（`index.http.json`）

| 任务 | 说明 |
|------|------|
| **河南科技大学校园网直连（大学掌体系）** | 大学掌 / 裕达 Portal：先取 CSRF 令牌再 POST 登录，令牌绑定连接 |
| **景德镇陶瓷大学校园网直连（Dr.COM eportal）** | dr1003 XOR 加密：密钥由本机 IP 逐字符异或推导，运营商后缀（@cmcc 等）直接写在账号里 |

> **条目只能放进对应类型的索引**：直连任务进 `index.http.json`（条目必须带 `"type": "http"`），浏览器任务进 `index.json`（条目不带 `type`，缺省即浏览器任务）。放错文件会出现「列表里看不见」或「看得见但导入被拒」。

> 部分**浏览器任务**在索引中附带 `screenshot` 字段（门户截图，便于确认是否为同一认证页面）。提供门户截图**非必需**，有截图时放入 `snap/` 目录（须为 WebP 格式：Gitee 对 AVIF 的 MIME 会导致无法显示，WebP 已实测正常）并在 `index.json` / `index.gitee.json` 中引用即可。直连任务没有浏览器登录页可截，不要给它加这个字段。

> 索引条目还有两个可选字段：`type`（直连任务必须写 `"http"`，浏览器任务不写）与 `source`（**来源仓库地址**，任务改编自他人脚本/项目时标注出处，导入弹窗的详情区会渲染成可点开的链接；仅接受 http/https）。

## 贡献

欢迎提交 PR 添加你学校的登录任务！

### 快速分享（Issue）

不熟悉 Git 操作？可以通过 Issue 提交：

1. 在 Campus-Auth 的任务管理页面点击**导出**，下载任务 `.json` 文件
2. 打开 [Issues 页面](https://github.com/Misyra/campus-auth-tasks/issues/new)，选择"提交任务"模板
3. 填写学校名称、认证系统型号等信息，上传任务 JSON 文件
4. 提交后由维护者审核并合并到仓库

### 使用 AI 自动提交（推荐）

如果你是 AI 编程助手（如 Claude Code、Cursor 等），可以直接参考 [submit-task.md](submit-task.md) 中的流程，AI 会自动完成安全审查、格式修正、文件移动和索引更新。

### 手动提交 Pull Request

**第一步：Fork 仓库**

1. 点击本仓库右上角的 **Fork** 按钮，将仓库复制到你的 GitHub 账号下

**第二步：添加任务文件**

1. 克隆你 Fork 的仓库到本地：
   ```bash
   git clone https://github.com/你的用户名/campus-auth-tasks.git
   cd campus-auth-tasks
   ```
2. 将导出的任务 JSON 文件放入 `temp/` 目录（未审核），文件名建议使用小写字母和下划线（如 `xxx_university.json`），且须与任务内 `id` 字段一致
3. 确认任务安全无风险后，从 `temp/` 移入 `tasks/` 目录
4. 编辑**对应的索引文件**，在数组末尾添加你的任务条目——浏览器任务进 `index.json`，直连任务进 `index.http.json`：
   ```json
   {
     "id": "xxx_university",
     "name": "XXX大学登录",
     "description": "适用于 XXX 大学校园网认证页面",
     "tags": ["你的学校名", "认证系统型号"],
     "author": "你的GitHub用户名",
     "version": "1.0.0",
     "url": "https://raw.githubusercontent.com/Misyra/campus-auth-tasks/master/tasks/xxx_university.json"
   }
   ```
   直连任务的条目额外带 `type`（固定 `"http"`）与 `source`（改编来源，没有可省）：
   ```json
   {
     "id": "xxx_university",
     "name": "XXX大学直连登录",
     "description": "直连渠道：先取令牌再 POST 登录，适用于 XXX 大学（设备型号）",
     "tags": ["你的学校名", "直连"],
     "author": "你的GitHub用户名",
     "version": "1.0.0",
     "type": "http",
     "source": "https://github.com/原作者/原项目",
     "url": "https://raw.githubusercontent.com/Misyra/campus-auth-tasks/master/tasks/xxx_university.json"
   }
   ```
5. 同步更新对应的**镜像索引**（`index.json` → `index.gitee.json`；`index.http.json` → `index.http.gitee.json`），条目内容相同、仅 `url` 换成 Gitee raw 地址
6. （可选，非必需，仅浏览器任务）如需提供门户截图：将截图转为 WebP 后放入 `snap/` 目录（如 `snap/xxx_university.webp`，截图前请遮挡账号、密码等个人信息），并在两份**浏览器**索引的对应条目中添加 `screenshot` 字段引用该图片

**第三步：提交并创建 PR**

```bash
git add tasks/xxx_university.json index.json index.gitee.json
git commit -m "feat: 添加 XXX 大学登录任务"
git push origin master
```

> 直连任务一行改成 `git add tasks/xxx_university.json index.http.json index.http.gitee.json`。如提供了门户截图，一并 `git add snap/xxx_university.webp`。`temp/` 下的待审核文件不随 PR 提交（审核通过后已移至 `tasks/`）。

然后在 GitHub 上打开你的 Fork 页面，点击 **Contribute → Open pull request**，填写说明后提交。

**第四步：等待审核**

维护者会审核任务内容，确认无误后合并到主仓库。审核期间可能需要你修改任务描述或补充信息。

### 任务 JSON 格式（浏览器任务）

任务 JSON 以 Campus-Auth 导出的结构为准，常见字段如下（`metadata` 用于记录作者、学校、设备型号等信息）：

```json
{
  "name": "XXX大学登录",
  "description": "适用于 XXX 大学校园网认证页面",
  "metadata": {
    "author": "your-name",
    "school": "XXX大学",
    "device": "认证设备型号"
  },
  "url": "{{LOGIN_URL}}",
  "timeout": 20000,
  "variables": {
    "username": "{{USERNAME}}",
    "password": "{{PASSWORD}}",
    "isp": "{{ISP}}"
  },
  "steps": [
    {
      "id": "s1",
      "type": "input",
      "description": "填写账号",
      "selector": "#username",
      "value": "{{username}}"
    }
  ],
  "success_conditions": [],
  "on_success": { "message": "登录成功" },
  "on_failure": { "message": "登录失败", "screenshot": true },
  "id": "xxx_university"
}
```

> 说明：
> - 提交/分享任务时，`url` 请留空或设为 `"{{LOGIN_URL}}"`，不要硬编码认证地址。
> - 成功判断由系统在步骤完成后统一做网络连通性检测，`success_conditions` 等字段仅保留兼容，不再参与判断，无需新增。
> - `reveal_hidden`（隐藏输入框场景）、`step_delay`（步骤间延时）等顶层字段按需保留；`id` 须与文件名一致。
> - **直连任务的任务文件不是这套结构**：它是 HTTP 请求形状（`method` / `url` / `headers` / `body` / 成败关键字 / 可选的凭据变换脚本、前置请求、退出登录请求），字段说明见 [直连登录指南](https://github.com/Misyra/Campus-Auth-rs/blob/master/docs/guides/http-login-guide.md)。最省事的做法是在 Campus-Auth 里配好一条直连任务、用「发送测试请求」验证通过后再「导出」，把导出的 JSON 直接放进 `tasks/`。

### 步骤类型（浏览器任务）

| 类型 | 说明 |
|------|------|
| `input` | 填写输入框 |
| `click` | 点击元素 |
| `select` | 选择下拉框 |
| `click_select` | 点击式自定义下拉框 |
| `wait` | 等待元素出现 |
| `wait_url` | 等待 URL 变化 |
| `eval` | 执行 JavaScript 并可选存储结果（`code` 为已废弃别名，`custom_js` 已合并到此类型） |
| `screenshot` | 截图 |
| `sleep` | 等待指定时间 |
| `ocr` | 验证码识别 |

> `navigate` 类型已废弃（改用任务的 `url` 字段），旧任务中的残留会被自动跳过。

### 任务录制器

推荐使用 [Campus-Auth 任务录制器](https://github.com/Misyra/Campus-Auth-rs/blob/master/resources/tools/task-recorder.user.js)（油猴脚本）可视化选取元素并生成任务 JSON。

### 任务编写指南

详细的步骤类型说明、变量系统、选择器建议等请参考仓库内的 [任务编写指南](doc/task-writing-guide.md)。

## License

MIT
