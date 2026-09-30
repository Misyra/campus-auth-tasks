# Campus-Auth 任务仓库

Campus-Auth 的校园网登录任务共享仓库。

## 索引文件

浏览器、HTTP 登录、脚本任务共用 `index.json`，每个条目必须显式填写 `"type": "browser" | "http" | "script"`。应用在三个子页按类型筛选。

| 索引 | 内容 | GitHub（主） | Gitee（镜像） |
|------|------|--------------|---------------|
| `index.json` | 三类任务的唯一编辑入口 | `https://raw.githubusercontent.com/Misyra/campus-auth-tasks/master/index.json` | `index.gitee.json` |
| `index.http.json` | 旧版应用的直连兼容索引（生成文件） | `https://raw.githubusercontent.com/Misyra/campus-auth-tasks/master/index.http.json` | `index.http.gitee.json` |

只编辑 `index.json`。运行 `python tools/build-index.py` 校验类型、ID 和任务文件，并生成 Gitee 镜像与旧版 HTTP 兼容索引；`python tools/build-index.py --check` 可检查是否同步。

## 使用方式

在 Campus-Auth 的浏览器、HTTP 登录或脚本任务子页点击 **从仓库导入**。三个子页读取同一份索引，仅展示当前类型。脚本任务导入前会展示完整代码；导入后不会自动执行，使用前还需在方案中绑定。

> 国内用户如访问 GitHub 不稳定，可在导入弹窗把「来源」切到 **Gitee**，或直接打开：
> ```
> https://raw.giteeusercontent.com/Misyra/campus-auth-tasks/raw/master/index.gitee.json
> ```

## 任务列表

### 浏览器任务（`type: browser`）

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

### HTTP 登录任务（`type: http`）

| 任务 | 说明 |
|------|------|
| **河南科技大学校园网直连（大学掌体系）** | 大学掌 / 裕达 Portal：先取 CSRF 令牌再 POST 登录，令牌绑定连接；支持方案的运营商字段（local / wcmcc / unicom / wtelecom，映射在凭据变换脚本里可改） |
| **景德镇陶瓷大学校园网直连（Dr.COM eportal）** | dr1003 XOR 加密：密钥由本机 IP 逐字符异或推导；方案的运营商字段经凭据变换脚本映射为账号后缀（映射表写在脚本开头，可改） |
| **深澜 SRUN BX1 登录模板** | challenge + HMAC-MD5 + srun_info + SHA1；导入后必须改网关并核对本校参数，尚未针对具体学校验证 |
| **上海大学锐捷 ePortal 模板** | 从页面提取 queryString/MAC，按来源部署的固定公钥加密密码；需校验当前门户，尚未在校园网环境实测 |

#### 社区仓库改编批次（2026-09）

46 个任务改编自 GitHub 公开的校园网认证脚本，覆盖深澜 SRUN、Dr.COM eportal/经典表单、锐捷 ePortal、H3C ac_portal 等门户类型（北京理工大学、清华大学、武汉大学、中国科学院大学、电子科技大学等 40 余所学校）。每条任务保留原作者署名与来源仓库（任务 `metadata` 的 `author` / `source` / `license`），并经模拟门户差分测试核对请求与原版一致；**未在对应校园网环境实测**，导入后请先用测试账号核对。完整学校列表、网关参数与来源见[改造统计](doc/改造统计-2026-09-29.md)。

### 脚本任务（`type: script`）

目前尚无经过审核的共享脚本任务。首批条目须使用内嵌 Python `content`，不依赖作者机器上的执行程序、工作目录或外部脚本路径；维护者需要核查凭据与网络请求的去向。

更多接入方法见[认证协议接入示例](doc/认证协议接入示例.md)：GIWIFI 多段请求、锐捷/ePortal 加密变体、802.1X、PPPoE 与私有 UDP 的边界。

> 部分**浏览器任务**在索引中附带 `screenshot` 字段（门户截图，便于确认是否为同一认证页面）。提供门户截图**非必需**，有截图时放入 `snap/` 目录（须为 WebP 格式：Gitee 对 AVIF 的 MIME 会导致无法显示，WebP 已实测正常）并在 `index.json` / `index.gitee.json` 中引用即可。直连任务没有浏览器登录页可截，不要给它加这个字段。

> 索引条目必须写 `type`。可选的 `source` 是改编来源仓库地址，导入弹窗会渲染为链接（仅接受 http/https）。

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
4. 编辑唯一的 `index.json`，在数组末尾添加任务条目并写明 `type`：
   ```json
   {
     "id": "xxx_university",
     "name": "XXX大学登录",
     "description": "适用于 XXX 大学校园网认证页面",
     "tags": ["你的学校名", "学校缩写", "认证系统型号"],
     "author": "你的GitHub用户名",
     "version": "1.0.0",
     "type": "browser",
     "url": "https://raw.githubusercontent.com/Misyra/campus-auth-tasks/master/tasks/xxx_university.json"
   }
   ```
   直连任务改用 `"type": "http"`；脚本任务改用 `"type": "script"`。改编任务可加 `source`：
   ```json
   {
     "id": "xxx_university",
     "name": "XXX大学直连登录",
     "description": "直连渠道：先取令牌再 POST 登录，适用于 XXX 大学（设备型号）",
     "tags": ["你的学校名", "学校缩写"],
     "author": "你的GitHub用户名",
     "version": "1.0.0",
     "type": "http",
     "source": "https://github.com/原作者/原项目",
     "url": "https://raw.githubusercontent.com/Misyra/campus-auth-tasks/master/tasks/xxx_university.json"
   }
   ```
   tags 约定：不要写「直连」「浏览器」等类型标签（类型由 `type` 字段表达），首个为中文校名，第二个为学校英文缩写（如 BUAA、HUST），其后为认证系统或厂商。
5. 运行 `python tools/build-index.py` 生成镜像与兼容索引，再运行 `python tools/build-index.py --check` 校验
6. （可选，仅浏览器任务）如需提供门户截图：将截图转为 WebP 后放入 `snap/` 目录，遮挡个人信息，并在 `index.json` 添加 GitHub raw `screenshot`；生成工具会转换镜像地址

**第三步：提交并创建 PR**

```bash
git add tasks/xxx_university.json index.json index.gitee.json index.http.json index.http.gitee.json
git commit -m "feat: 添加 XXX 大学登录任务"
git push origin master
```

> 如提供了门户截图，一并 `git add snap/xxx_university.webp`。`temp/` 下的待审核文件不随 PR 提交。

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
> - **HTTP 登录任务文件使用另一套结构**：新版格式为 `type: "http"`、`schema_version: 2`、有序 `steps` 与 `result_step_id`。请求步骤可取值，计算步骤可生成后续请求变量；成败关键字与检测方式位于顶层。旧版固定请求字段继续兼容读取。字段说明见 [HTTP 登录指南](https://github.com/Misyra/Campus-Auth-rs/blob/master/docs/guides/http-login-guide.md)。建议在 Campus-Auth 里配置、测试并「导出」后再放入 `tasks/`；新版流程仅供支持 `schema_version: 2` 的应用使用。

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

## 许可证

本仓库以 [AGPL-3.0](LICENSE) 分发，与主程序 [Campus-Auth-rs](https://github.com/Misyra/Campus-Auth-rs) 一致。任务改编遵循以下口径：

- **宽松许可证来源**（MIT / Apache-2.0 / BSD / WTFPL / 木兰-PSL-2.0 等）：按原条款改编收录，任务 `metadata` 保留原作者、来源仓库与许可证；
- **copyleft 来源**（GPL / LGPL / AGPL）：改编随本仓库以 AGPL-3.0 分发，同样保留来源署名与上游许可证标注；
- **无许可证来源**：不做代码级改编，仅提取协议事实参数（网关、ac_id、运营商后缀等），登录流程由本仓库自有模板实现，任务中注明参数来源。
