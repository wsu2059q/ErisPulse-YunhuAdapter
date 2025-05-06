class Main:
    def __init__(self, sdk):
        self.sdk = sdk
        self.logger = sdk.logger
        self.yhToken = sdk.MessageBase.yhToken
        self.apiUrl = (
            "https://chat-go.jwzhd.com/open-apis/v1/bot/edit?token=" + self.yhToken
        )
        self.NetJsonPost = sdk.MessageBase.NetJsonPost
    def _gen_body(
        self,
        msgId: str,
        recvId: str,
        recvType: str,
        contentType: str,
        content: dict[str, any],
    ) -> dict[str, any]:
        return {
            "msgId": msgId,
            "recvId": recvId,
            "recvType": recvType,
            "contentType": contentType,
            "content": content,
        }

    async def Text(
        self,
        msgId: str,
        recvId: str,
        recvType: str,
        content: str,
        buttons: list[list[dict[str, any]]] = [],
    ) -> dict[str, any]:
        self.logger.info(f"编辑文本消息 消息ID:{msgId}")
        self.logger.debug(f"编辑的文本内容: {content}")
        return await self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                msgId,
                recvId,
                recvType,
                "text",
                {"text": content, "buttons": buttons},
            ),
        )

    async def Markdown(
        self,
        msgId: str,
        recvId: str,
        recvType: str,
        content: str,
        buttons: list[list[dict[str, any]]] = [],
    ) -> dict[str, any]:
        self.logger.info(f"编辑Markdown消息 消息ID:{msgId}")
        self.logger.debug(f"编辑的Markdown内容: {content}")
        return await self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                msgId,
                recvId,
                recvType,
                "markdown",
                {"text": content, "buttons": buttons},
            ),
        )
