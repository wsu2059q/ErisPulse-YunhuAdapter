# ⚠️ 本仓库已归档！主要维护者已退出云湖平台 ⚠️

> **重要说明：**
>
> 本项目已于 2025 年 5 月 归档，主要维护者已退出云湖平台。未来本仓库将不再适配云湖协议的新特性，也不会响应 issue 或 PR。**请谨慎用于生产环境！**
>
> 云湖平台本身仍在运营，但我们作为一群开发者，因生态环境、社区氛围等多方面原因，选择离开。我们希望社区能持续关注 Bot 生态的健康发展。

---

## 为什么归档？我们想说些什么

- **生态混乱，缺乏有效治理**  
  云湖 Bot 生态长期存在质量参差不齐、滥用接口等问题。即便在全员群，部分管理人员也未能积极维护健康生态，甚至在面对开发者提出的谴责时，选择“比烂”而非推动改进。
- **开发者素质参差**  
  部分 Bot 开发者基础能力不足，代码中常见如未正确区分 `/` 开头的指令与普通消息、未判断 `eventType` 等低级错误，影响了平台整体体验。
- **我们希望的社区氛围**  
  我们希望看到的是一个鼓励高质量开发、共同维护生态、互相学习进步的社区，而不是推卸责任、互相指责、放任低质量代码泛滥的环境。

---

## 下面是原有文档内容

（以下为原有 YunhuAdapter 说明文档，供有需要的开发者参考）

---

# YunhuAdapter - 云湖协议适配器

## 模块介绍

### YunhuAdapter
提供异步 HTTP 服务，用于接收来自云湖 App 的 Webhook 推送事件。适用于云湖开放平台的消息回调机制。

#### 主要功能：
- 支持配置监听地址、端口和回调路径
- 提供统一的事件分发机制，将不同事件类型转发给对应的处理器

---

## 使用示例

以下是一个完整使用示例，展示如何初始化 SDK 并注册各类事件处理器：

```python
import asyncio
from ErisPulse import sdk

# 初始化SDK
sdk.init()

async def on_followed(data):
    print(f"被用户关注啦: {data}")

async def on_unfollowed(data):
    print(f"被用户取关了 T_T: {data}")

async def on_command(data):
    print(f"收到通用指令: {data}")

# 指令处理函数（指定 cmdid）
async def handle_start(data):
    print(f"收到指令 START: {data}")

async def handle_stop(data):
    print(f"收到指令 STOP: {data}")

async def main():
    # 添加触发器
    sdk.YunhuAdapter.AddTrigger(sdk.YunhuBotFollowed)           # 注册关注事件
    sdk.YunhuAdapter.AddTrigger(sdk.YunhuBotUnfollowed)         # 注册取消关注事件
    sdk.YunhuAdapter.AddTrigger(sdk.YunhuCommandHandler)        # 注册指令消息触发器

    # 添加具体处理器
    sdk.YunhuBotFollowed.AddHandle(on_followed)
    sdk.YunhuBotUnfollowed.AddHandle(on_unfollowed)
    sdk.YunhuCommandHandler.AddHandle(on_command)

    # 添加带指令ID的处理器
    sdk.YunhuCommandHandler.AddHandle(handle_start, "114")
    sdk.YunhuCommandHandler.AddHandle(handle_stop, "514")

    # 启动 Webhook 服务
    await sdk.YunhuAdapter.Run()

# 运行主程序
asyncio.run(main())
```

---

## 配置说明

在 `config.py` 中进行以下配置：

```python
from ErisPulse import sdk

sdk.env.set('YunhuAdapter',{
    "Server":{
        "host": "127.0.0.1",
        "port": 8080,
        "path": "/"
    },
    "token": ""
})
```

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `host` | string | Webhook 服务监听的主机地址 |
| `port` | int | 监听端口号 |
| `path` | string | Webhook 回调路径 |
| `token` | string | 可选，用于校验请求来源合法性 |

---
## 装饰器方式监听事件（v1.2.0+ 新增）

自 `YunhuAdapter v1.2.0` 起，你可以使用如下方式快速监听事件：

```python
@sdk.YunhuAdapter.on("bot.followed")
async def on_followed(data):
    print("有用户关注了机器人:", data)

@sdk.YunhuAdapter.on("message.receive.instruction").id("114514")
async def handle_calculator_a(data):
    print("用户输入了id为 114514 的命令:", data)

@sdk.YunhuAdapter.on("message.receive.instruction").name("计算器")
async def handle_calculator_b(data):
    print("用户输入了名称为 计算器 的命令:", data)
```

该方式语法简洁，适合快速开发或小型脚本。

---

## 模块化事件处理（推荐）

尽管装饰器方式非常方便，我们仍然建议使用独立模块进行事件处理，原因包括：

- 更好的职责分离与代码组织
- 支持多处理器、分类处理（如 `.AddHandle(handler)`）
- 插件系统兼容性更好
- 日志更清晰，便于调试维护
- 更易扩展未来功能（权限控制、中间件等）

---

## 📬 支持的事件类型

| 模块名              | 事件类型         | 功能描述                           |
|---------------------|------------------|------------------------------------|
| `YunhuBotFollowed`       | `bot.followed`           | 处理用户关注机器人事件               |
| `YunhuBotUnfollowed`     | `bot.unfollowed`         | 处理用户取消关注机器人事件             |
| `YunhuCommandHandler`    | `message.receive.instruction` | 处理带有指令 ID 的消息事件             |
| `YunhuNormalHandler`     | `message.receive.normal` | 处理普通文本/富文本消息               |
| `YunhuGroupJoin`         | `group.join`             | 处理用户加入群聊事件                 |
| `YunhuGroupLeave`        | `group.leave`            | 处理用户退出群聊事件                 |

### AddHandle 的通用使用方法：
```python
sdk.<Module>.AddHandle(handle)
```

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `handle` | async function | ✅ | 异步处理函数，接受一个参数 `data`（即事件数据） |

## YunhuCommandHandler 特别说明

`YunhuCommandHandler` 是处理带有指令 ID 的命令类消息的专用模块，支持按 `instructionId` 或 `commandId` 分类处理。

特别的 YunhuCommandHandler 的 AddHandle 方法支持传入 `cmdid` 以获取指定指令 ID 的处理回调
```python
sdk.YunhuCommandHandler.AddHandle(handle, cmdid="ALL")
```

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `handle` | async function | ✅ | 异步处理函数，参数为接收到的数据 `data` |
| `cmdid` | str | ❌ | 要监听的指令 ID，默认 `"ALL"` 表示所有未单独匹配的指令 |

---

## 消息发送与操作模块

以下模块提供了发送不同类型消息和执行相关操作的功能：

| 模块名            | 功能说明                         |
|-------------------|----------------------------------|
| `YunhuMessageSender`   | 发送消息                   |
| `YunhuMessageBatch`    | 批量发送消息                     |
| `YunhuMessageEditor`   | 编辑已发送消息                   |
| `YunhuMessageHistory`  | 查询历史消息及撤回               |
| `YunhuMessageBoard`    | 发布看板消息（含全局和局部）     |

### `YunhuMessageSender` 模块
#### 功能：发送消息给用户或群组

##### 主要方法：
- `Text(recvId, recvType, content, buttons=[], parentId="")`
- `Markdown(recvId, recvType, content, buttons=[], parentId="")`
- `Html(recvId, recvType, content, buttons=[], parentId="")`
- `Image(recvId, recvType, content_bytes, buttons=[], parentId="")`
- `Video(recvId, recvType, content_bytes, buttons=[], parentId="")`
- `File(recvId, recvType, content_bytes, buttons=[], parentId="")`

##### 示例：
```python
await sdk.YunhuMessageSender.Text(
    recvId="user123",
    recvType="user",
    content="你好！",
    buttons=[{"text": "点击我", "value": "click"}]
)
```

---

### `YunhuMessageBatch` 模块
#### 功能：向多个接收者批量发送消息

##### 主要方法：
- `Text(recvIds, recvType, content, buttons=[], parentId="")`
- `Markdown(recvIds, recvType, content, buttons=[], parentId="")`
- `Html(recvIds, recvType, content, buttons=[], parentId="")`
- `Image(recvIds, recvType, content_bytes, buttons=[], parentId="")`
- `Video(recvIds, recvType, content_bytes, buttons=[], parentId="")`
- `File(recvIds, recvType, content_bytes, buttons=[], parentId="")`

##### 示例：
```python
await sdk.YunhuMessageBatch.Text(
    recvIds=["user1", "user2"],
    recvType="user",
    content="这是一条批量消息"
)
```

---

### `YunhuMessageBoard` 模块
#### 功能：发布或撤销看板消息（指定用户会话看板或全局看板）

##### 主要方法：
- **指定用户看板**
  - `LocalText(chatId, chatType, content, memberId="", expireTime=0)`
  - `LocalMarkdown(chatId, chatType, content, memberId="", expireTime=0)`
  - `LocalHtml(chatId, chatType, content, memberId="", expireTime=0)`
  - `LocalDismiss(chatId, chatType, memberId="")`

- **全局看板**
  - `GlobalText(content, expireTime=0)`
  - `GlobalMarkdown(content, expireTime=0)`
  - `GlobalHtml(content, expireTime=0)`
  - `GlobalDismiss()`

##### 示例：
```python
# 发布全局文本看板
await sdk.YunhuMessageBoard.GlobalText("这是全局公告！", expireTime=86400)

# 撤销某个用户的局部看板
await sdk.YunhuMessageBoard.LocalDismiss(chatId="group123", chatType="group", memberId="user1")
```

---

### `YunhuMessageEditor` 模块
#### 功能：编辑已发送的消息内容（支持文本/Markdown）

##### 主要方法：
- `Text(msgId, recvId, recvType, content, buttons=[])`
- `Markdown(msgId, recvId, recvType, content, buttons=[])`

##### 示例：
```python
await sdk.YunhuMessageEditor.Text(
    msgId="msg_abc123",
    recvId="user123",
    recvType="user",
    content="修改后的消息内容"
)
```

---

### `YunhuMessageHistory` 模块
#### 功能：撤回消息 & 查询历史消息

##### 主要方法：
- `Recall(msgId, recvId, recvType)`
  > 撤回某条消息
- `HistoryBefore(chatId, chatType, before, msgId=None)`
  > 查询在某一时间点之前的历史消息
- `HistoryAfter(chatId, chatType, msgId, after, before=None)`  
  > 查询某条消息之后的历史消息

##### 示例：
```python
# 撤回一条消息
await sdk.YunhuMessageHistory.Recall(msgId="msg_abc123", recvId="user123", recvType="user")

# 查询某会话前5条历史消息
result = await sdk.YunhuMessageHistory.HistoryBefore(chatId="group123", chatType="group", before=5)
```

---

## 参考链接

- [ErisPulse 主库](https://github.com/ErisPulse/ErisPulse/)
- [ErisPulse 模块开发指南](https://github.com/ErisPulse/ErisPulse/tree/main/docs/DEVELOPMENT.md)
- [云湖官方 API 文档](https://www.yhchat.com/document/1-3)
