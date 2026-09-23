# submit-task — 提交任务到 Campus-Auth 仓库

## 流程概览

安全审查 → 格式修正 → 放入 `temp/`（待审核）→ 确认后移至 `tasks/` → 更新**对应类型的索引**及其 Gitee 镜像（浏览器任务：`index.json` + `index.gitee.json`；直连任务：`index.http.json` + `index.http.gitee.json`，可选附门户截图）→ 提交

## 适用场景

- 你编写了一个校园网认证任务，想提交到本仓库
- 使用 AI 辅助完成提交流程，自动完成安全审查、格式修正、索引更新

## 提交流程

### Step 1: 准备任务 JSON

从 Campus-Auth 导出或自行编写任务 JSON 文件。

### Step 2: 安全审查（⚠️ 重点）

`eval` 类型的步骤会直接执行 JavaScript（`custom_js` 已合并到 `eval`，`code` 是 `script` 的已废弃别名）。审查每个 `script` 字段：

| 风险行为 | 说明 | 处理 |
|----------|------|------|
| 远程代码加载 | `fetch()`、`XMLHttpRequest`、`$.getScript()`、`import()`、动态创建 `<script>` 加载远程 JS | ❌ 拒绝 |
| 数据外传 | `navigator.sendBeacon()`、`fetch()`/`XMLHttpRequest` 向第三方域名发数据 | ❌ 拒绝 |
| 敏感泄露 | 读取 `localStorage`、`sessionStorage`、`document.cookie` 并外传 | ❌ 拒绝 |
| 页面跳转 | `window.open()`、`location.href=` 跳转到非认证域名 | ⚠️ 需说明 |
| 安全操作 | DOM 查询、表单填写、点击事件、文本匹配判断 | ✅ 通过 |

**安全脚本通常只做三件事：** 查找页面元素 → 填写值/触发事件 → 读取文本判断结果。

#### 审查后处理原则

| 审查结果 | 处理方式 |
|----------|----------|
| 存在风险脚本 | ❌ 拒绝提交，说明具体原因 |
| 无风险 | ✅ 不修改步骤，保持原有逻辑不变 |
| 有优化空间 | 📋 列出优化方案并等待确认，不直接修改 |

### Step 3: 格式修正

| 规则 | 说明 |
|------|------|
| 缩进 | 统一 2 空格 |
| `code` → `script` | 步骤中的 `code` 字段改名为 `script` |
| `custom_js` → `eval` | 步骤类型 `custom_js` 改为 `eval`（旧任务残留须迁移） |
| `url` 字段 | 必须为 `"{{LOGIN_URL}}"` 或省略，禁止硬编码地址 |
| `on_failure.screenshot` | 确保为 `true` |
| 成功判断字段 | 不要新增 `success_conditions`（系统统一用网络检测兜底）；任务自带的旧字段原样保留即可 |
| `id` 与文件名 | 任务内 `id` 字段须与文件名一致（如 `tasks/hust.json` 对应 `"id": "hust"`） |

#### 信息确认（⚠️ 必填）

完成格式修正后，如果以下信息缺失，**必须主动询问用户**确认：

| 信息 | 说明 | 询问方式 |
|------|------|----------|
| 学校名称 | 任务所属的学校/单位 | "这个任务是哪个学校的？" |
| 认证设备型号 | 如 Dr.COM、深澜、杭州康工 HK Posi 等 | "这个认证页面的设备型号是什么？" |
| `metadata.author` | 任务作者 | "作者怎么署名？" |

> ⚠️ **禁止无证据猜测**：不得根据页面 URL、页面内容或任务结构推测学校名称或设备型号，必须由用户明确提供。用户也无法确认的，在 `metadata` 和描述中标注为"未知"。

通过询问确认的信息，填写到任务 JSON 的 `metadata` 字段中：
```json
{
  "metadata": {
    "author": "用户提供的署名",
    "school": "用户确认的学校名称",
    "device": "用户确认的设备型号"
  }
}
```

具体字段定义遵循 [任务编写指南](doc/task-writing-guide.md) 中的 `metadata` 规范。

### Step 4: 放入 `temp/`（待审核状态）

生成文件名（小写 + 下划线），放入 `temp/` 目录：

```powershell
Move-Item -Path "task.json" -Destination "temp/hust.json"
```

`temp/` = 待审核，`tasks/` = 已收录。**一个任务只保留一份文件**，审核通过后会从 `temp/` 移至 `tasks/`。

**ID 命名规范：**
- 优先使用学校英文缩写，如 `hust`（华中科技大学）、`ncu`（南昌大学）、`pku`（北京大学）
- 无明确缩写的学校可用拼音或英文名，如 `beijing_university`
- 文件名须匹配 `id` 字段

**ID 冲突处理：**
- 如果 `id` 已存在于对应类型的索引（浏览器任务 `index.json`、直连任务 `index.http.json`）中，先读取已有任务文件对比内容
- **相同任务**（同一学校、同一认证系统）：更新现有文件，不创建新条目
- **不同任务**（不同学校或不同认证系统）：询问用户如何区分，建议修改 `id`（如加后缀 `_v2`、`_new` 或校区名）
- **无法判断**：向用户展示两个任务的差异，由用户决定

### Step 5: 移至 `tasks/`

确认审查通过后，从 `temp/` 移到 `tasks/`：

```powershell
Move-Item -Path "temp/hust.json" -Destination "tasks/hust.json"
```

### Step 6: 更新对应类型的索引

**浏览器任务写入 `index.json`，直连任务写入 `index.http.json`** —— 两类任务各有一份索引，放错文件会让条目在 App 里「列表里看不见」或「看得见但导入被拒」。

在对应索引的数组末尾添加条目，`url` 指向 `tasks/` 中的文件。如提供门户截图（非必需，仅浏览器任务），可附带 `screenshot` 字段：

```json
{
  "id": "hust",
  "name": "华中科技大学校园网登录",
  "description": "适用于华中科技大学 Dr.COM Portal 认证页面，需先点击密码占位元素激活密码输入框",
  "tags": ["华中科技大学", "Dr.COM"],
  "author": "your-github-username",
  "version": "1.0.0",
  "url": "https://raw.githubusercontent.com/Misyra/campus-auth-tasks/master/tasks/hust.json"
}
```

直连任务的条目额外带 `type`（固定 `"http"`）与 `source`（改编来源，没有可省）：

```json
{
  "id": "haust",
  "name": "河南科技大学校园网直连（大学掌体系）",
  "description": "直连渠道：先取 CSRF 令牌再 POST 登录，令牌绑定连接。适用于河南科技大学（裕达 / 大学掌 Portal）",
  "tags": ["河南科技大学", "大学掌", "直连"],
  "author": "heragehome",
  "version": "1.0.0",
  "type": "http",
  "source": "https://github.com/heragehome/haust-auto-login",
  "url": "https://raw.githubusercontent.com/Misyra/campus-auth-tasks/master/tasks/haust.json"
}
```

### Step 6a: 门户截图（可选，非必需，仅浏览器任务）

提供门户截图有助于他人确认是否为同一认证页面，但不是提交的必要条件。**直连任务没有浏览器登录页可截，不要给它加这个字段。** 要求如下：

- 截图须为 WebP 格式（Gitee 镜像对 AVIF 返回的 MIME 会导致图片无法显示，WebP 已实测双端正常）：提交前转换，如 `ffmpeg -y -i snap/hust.png -q:v 80 snap/hust.webp`，转完后删除源文件
- 截图前请遮挡账号、密码、验证码等个人信息
- 在 `index.json` / `index.gitee.json` 的对应条目中添加 `screenshot` 字段，分别指向 GitHub / Gitee raw 地址，例如：

```json
"screenshot": "https://raw.githubusercontent.com/Misyra/campus-auth-tasks/master/snap/hust.webp"
```

### Step 6b: 同步镜像索引

本仓库为**每份索引**各维护了一个 Gitee 镜像索引，供国内用户使用：`index.json` → `index.gitee.json`，`index.http.json` → `index.http.gitee.json`。在对应的镜像索引中添加相同条目，仅将 `url` 切换为 Gitee raw 地址：

```json
{
  "id": "hust",
  "name": "华中科技大学校园网登录",
  "description": "适用于华中科技大学 Dr.COM Portal 认证页面，需先点击密码占位元素激活密码输入框",
  "tags": ["华中科技大学", "Dr.COM"],
  "author": "your-github-username",
  "version": "1.0.0",
  "url": "https://raw.giteeusercontent.com/Misyra/campus-auth-tasks/raw/master/tasks/hust.json"
}
```

**描述优化原则：**
- 在不改变原意的前提下优化表述，使其更清晰、专业
- 增加适配学校信息，方便其他用户识别是否适用
- **禁止无证据猜测**：不要推测任务所属学校、认证系统型号（如 Dr.COM、深澜等），必须通过 Step 3 的信息确认步骤由用户明确提供
- 如果 Step 3 中用户也无法确认学校或设备信息，`name` 和 `description` 中不应包含具体的学校名称，应使用通用描述

### Step 7: 提交

```powershell
git add tasks/hust.json index.json index.gitee.json
git commit -m "feat: 添加华中科技大学校园网登录任务"
git push origin master && git push gitee master
```

> 直连任务把那两行索引文件名换成 `index.http.json` / `index.http.gitee.json`。
> **注意：** 提交中不需要包含 `temp/` 下的文件（已移至 `tasks/`），也不需要包含 `doc/`（编写指南不属于任务提交内容）。
> 镜像索引（`index.gitee.json` / `index.http.gitee.json`）需同步提交并在两边 remote 都推送。
> 如提供了门户截图，一并 `git add snap/hust.webp`（截图须与 `screenshot` 字段路径一致）。

## 验证清单

- [ ] JSON 语法正确
- [ ] 所有 `eval` 脚本已审查、无风险（`custom_js` 已合并到 `eval`，`code` 已改为 `script`）
- [ ] `url` 为 `"{{LOGIN_URL}}"` 或省略
- [ ] `index.json` / `index.http.json` 是合法 JSON，且条目放进了**对应类型**的那份
- [ ] 对应的镜像索引是合法 JSON（URL 为 Gitee raw 地址）
- [ ] 文件名、`id` 字段、索引里的 `url` 三者一致
- [ ] `tasks/` 下有对应文件，`temp/` 下无残留
- [ ] ID 命名使用学校缩写（如可用）
- [ ] 描述清晰且未包含无证据的猜测
- [ ] **已确认学校信息**：`metadata.school` 已通过用户确认（或标注为"未知"）
- [ ] **已确认设备型号**：`metadata.device` 已通过用户确认（或标注为"未知"）
- [ ] `metadata.author` 已填写（用户确认或"anonymous"）
- [ ] 直连任务：条目带 `"type": "http"`，且只出现在 `index.http.json` / `index.http.gitee.json`
- [ ] 如提供门户截图（非必需，仅浏览器任务）：已放入 `snap/` 且文件名与 `id` 一致，已遮挡个人信息，两份**浏览器**索引的 `screenshot` 字段均已添加且地址正确
