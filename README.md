# YunhuAdapter - 云湖协议适配器

## 模块介绍

### AsyncServer（Webhook Server）
提供异步 HTTP 服务，用于接收来自云湖 App 的 Webhook 推送事件。适用于云湖开放平台的消息回调机制。

> 说明：该模块只实现 Server 模式，即被动接收 Webhook 请求，不支持主动连接。

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

# 定义消息处理函数
async def on_normal_message(data):
    print(f"收到普通消息: {data}")

async def on_group_join(data):
    print(f"有人加入群组: {data}")

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
    sdk.AsyncServer.AddTrigger(sdk.MessageHandler)        # 注册普通消息触发器
    sdk.AsyncServer.AddTrigger(sdk.NoticeHandler)         # 注册通知触发器
    sdk.AsyncServer.AddTrigger(sdk.BotFollowed)           # 注册关注事件
    sdk.AsyncServer.AddTrigger(sdk.BotUnfollowed)         # 注册取消关注事件
    sdk.AsyncServer.AddTrigger(sdk.CommandHandler)        # 注册指令消息触发器

    # 添加具体处理器
    sdk.MessageHandler.AddHandle(on_normal_message)
    sdk.NoticeHandler.AddHandle(on_group_join)
    sdk.BotFollowed.AddHandle(on_followed)
    sdk.BotUnfollowed.AddHandle(on_unfollowed)
    sdk.CommandHandler.AddHandle(on_command)

    # 添加带指令ID的处理器
    sdk.CommandHandler.AddHandle(handle_start, "114")
    sdk.CommandHandler.AddHandle(handle_stop, "514")

    # 启动 Webhook 服务
    await sdk.AsyncServer.Run()

# 运行主程序
asyncio.run(main())
```

---

## 配置说明

在 `env.py` 中进行以下配置：

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

## CommandHandler 特别说明

`CommandHandler` 是处理带有指令 ID 的命令类消息的专用模块，支持按 `instructionId` 或 `commandId` 分类处理。

### AddHandle 方法：
```python
sdk.CommandHandler.AddHandle(handle, cmdid="ALL")
```

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `handle` | async function | ✅ | 异步处理函数，参数为接收到的数据 `data` |
| `cmdid` | str | ❌ | 要监听的指令 ID，默认 `"ALL"` 表示所有未单独匹配的指令 |

> 示例：
> ```python
> async def handle_cmd1(data):
>     print("收到指令 CMD1", data)
>
> sdk.CommandHandler.AddHandle(handle_cmd1, "CMD1")
> ```

---

## 其他通用处理器模块（合并说明）

以下模块结构相似，均提供统一的 `AddHandle` 接口来注册事件处理逻辑：

| 模块名              | 事件类型         | 功能描述                           |
|---------------------|------------------|------------------------------------|
| NormalHandler       | `message.receive.normal` | 处理普通文本/富文本消息             |
| JoinGroupHandler, LeaveGroupHandler    | `group.join`, `group.leave` 等 | 处理加入群聊，离开群聊事件                     |
| BotFollowed, BotUnfollowed         | `bot.followed`, `unfollowed`  | 处理用户 关注/取消关注 机器人事件               |

### AddHandle 方法（通用）：
```python
sdk.<Module>.AddHandle(handle)
```

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `handle` | async function | ✅ | 异步处理函数，接受一个参数 `data`（即事件数据） |

---

## 消息发送与操作模块

以下模块提供了发送不同类型消息和执行相关操作的功能：

| 模块名            | 功能说明                         |
|-------------------|----------------------------------|
| `MessageSender`   | 发送一对一消息                   |
| `MessageBatch`    | 批量发送消息                     |
| `MessageEditor`   | 编辑已发送消息                   |
| `MessageHistory`  | 查询历史消息及撤回               |
| `MessageBoard`    | 发布看板消息（含全局和局部）     |

### ✅ `MessageSender` 模块
#### 功能：一对一发送消息给用户或群组

##### 主要方法：
- `Text(recvId, recvType, content, buttons=[], parentId="")`
- `Markdown(recvId, recvType, content, buttons=[], parentId="")`
- `Html(recvId, recvType, content, buttons=[], parentId="")`
- `Image(recvId, recvType, content_bytes, buttons=[], parentId="")`
- `Video(recvId, recvType, content_bytes, buttons=[], parentId="")`
- `File(recvId, recvType, content_bytes, buttons=[], parentId="")`

##### 示例：
```python
await sdk.MessageSender.Text(
    recvId="user123",
    recvType="user",
    content="你好！",
    buttons=[{"text": "点击我", "value": "click"}]
)
```

---

### ✅ `MessageBatch` 模块
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
await sdk.MessageBatch.Text(
    recvIds=["user1", "user2"],
    recvType="user",
    content="这是一条批量消息"
)
```

---

### `MessageBoard` 模块
#### 功能：发布或撤销看板消息（指定会话或全局）

##### 主要方法：
- **本地看板**
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
await sdk.MessageBoard.GlobalText("这是全局公告！", expireTime=86400)

# 撤销某个用户的局部看板
await sdk.MessageBoard.LocalDismiss(chatId="group123", chatType="group", memberId="user1")
```

---

### `MessageEditor` 模块
#### 功能：编辑已发送的消息内容（支持文本/Markdown）

##### 主要方法：
- `Text(msgId, recvId, recvType, content, buttons=[])`
- `Markdown(msgId, recvId, recvType, content, buttons=[])`

##### 示例：
```python
await sdk.MessageEditor.Text(
    msgId="msg_abc123",
    recvId="user123",
    recvType="user",
    content="修改后的消息内容"
)
```

---

### `MessageHistory` 模块
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
await sdk.MessageHistory.Recall(msgId="msg_abc123", recvId="user123", recvType="user")

# 查询某会话前5条历史消息
result = await sdk.MessageHistory.HistoryBefore(chatId="group123", chatType="group", before=5)
```

---

### 模块功能对比表：

| 模块名         | 接收者类型     | 是否支持批量 | 是否支持编辑 | 是否支持看板 | 是否支持文件上传 |
|----------------|----------------|---------------|----------------|----------------|--------------------|
| `MessageSender` | 单个用户/群组   | ❌            | ❌             | ❌             | ✅                 |
| `MessageBatch`  | 多个用户/群组   | ✅            | ❌             | ❌             | ✅                 |
| `MessageBoard`  | 用户/群组       | ❌            | ❌             | ✅             | ❌                 |
| `MessageEditor` | 单个用户/群组   | ❌            | ✅             | ❌             | ❌                 |
| `MessageHistory`| 用户/群组       | ❌            | ❌             | ❌             | ❌                 |

---

## 参考链接

- [ErisPulse 主库](https://github.com/ErisPulse/ErisPulse/)
- [ErisPulse 模块开发指南](https://github.com/ErisPulse/ErisPulse/tree/main/docs/DEVELOPMENT.md)
- [云湖官方 API 文档](https://www.yhchat.com/document/1-3)