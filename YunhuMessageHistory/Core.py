class Main:
    def __init__(self, sdk):
        self.sdk = sdk
        self.logger = sdk.logger
        self.yhToken = sdk.YunhuMessageBase.yhToken
        self.NetJsonPost = sdk.YunhuMessageBase.NetJsonPost
        self.NetJsonGet = sdk.YunhuMessageBase.NetJsonGet
        self.history_api = (
            "https://chat-go.jwzhd.com/open-apis/v1/bot/messages?token=" + self.yhToken
        )

    async def Recall(self, msgId: str, recvId: str, recvType: str) -> dict[str, any]:
        self.logger.info(f"准备撤回消息 {msgId} 来自 {recvType}:{recvId}")
        result = await self.NetJsonPost(
            "https://chat-go.jwzhd.com/open-apis/v1/bot/recall?token=" + self.yhToken,
            {"msgId": msgId, "chatId": recvId, "chatType": recvType},
        )

    async def HistoryBefore(
        self, chatId: str, chatType: str, before: int, msgId: str = None
    ) -> dict[str, any]:
        self.logger.info(f"查询历史消息 会话:{chatId} 类型:{chatType} 时间点:{before}")
        if msgId is not None:
            self.logger.debug(f"指定消息ID: {msgId}")
        api = (
            f"{self.history_api}&chat-id={chatId}&chat-type={chatType}&before={before}"
        )
        if msgId is not None:
            api += f"&message-id={msgId}"
        result = await self.NetJsonGet(api)
        self.logger.debug(f"获取到 {len(result.get('data', []))} 条历史消息")

    async def HistoryAfter(
        self, chatId: str, chatType: str, msgId: str, after: int, before: int = None
    ) -> dict[str, any]:
        self.logger.info(f"查询后续消息 会话:{chatId} 类型:{chatType} 起始消息:{msgId}")
        if before is not None:
            self.logger.debug(f"时间范围限制: after={after}, before={before}")
        api = f"{self.history_api}&chat-id={chatId}&chat-type={chatType}&message-id={msgId}&after={after}"
        if before is not None:
            api += f"&before={before}"
        result = await self.NetJsonGet(api)
        self.logger.debug(f"获取到 {len(result.get('data', []))} 条后续消息")
