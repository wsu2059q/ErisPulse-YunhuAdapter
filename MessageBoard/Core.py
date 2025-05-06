class Main:
    def __init__(self, sdk, logger):
        self.yhToken = sdk.MessageBase.yhToken
        self.NetJsonPost = sdk.MessageBase.NetJsonPost
        self.local_board_api = (
            "https://chat-go.jwzhd.com/open-apis/v1/bot/board?token=" + self.yhToken
        )
        self.global_board_api = (
            "https://chat-go.jwzhd.com/open-apis/v1/bot/board-all?token=" + self.yhToken
        )
        self.logger = logger

    def _gen_local_body(
        self,
        chatId: str,
        chatType: str,
        contentType: str,
        content: str,
        memberId: str,
        expireTime: int,
    ) -> dict[str, str]:
        return {
            "chatId": chatId,
            "chatType": chatType,
            "contentType": contentType,
            "content": content,
            "memberId": memberId,
            "expireTime": expireTime,
        }

    def _gen_global_body(
        self, contentType: str, content: str, expireTime: int
    ) -> dict[str, str]:
        return {
            "contentType": contentType,
            "content": content,
            "expireTime": expireTime,
        }

    async def LocalText(
        self,
        chatId: str,
        chatType: str,
        content: str,
        memberId: str = "",
        expireTime: int = 0,
    ) -> dict[str, any]:
        self.logger.info(f"发布文本指定看板 会话:{chatType}:{chatId}")
        self.logger.debug(f"发布的文本内容: {content}")
        return await self.NetJsonPost(
            self.local_board_api,
            self._gen_local_body(
                chatId, chatType, "text", content, memberId, expireTime
            ),
        )

    async def LocalMarkdown(
        self,
        chatId: str,
        chatType: str,
        content: str,
        memberId: str = "",
        expireTime: int = 0,
    ) -> dict[str, any]:
        self.logger.info(f"发布Markdown指定看板 会话:{chatType}:{chatId}")
        self.logger.debug(f"发布的Markdown内容: {content}")
        return await self.NetJsonPost(
            self.local_board_api,
            self._gen_local_body(
                chatId, chatType, "markdown", content, memberId, expireTime
            ),
        )

    async def LocalHtml(
        self,
        chatId: str,
        chatType: str,
        content: str,
        memberId: str = "",
        expireTime: int = 0,
    ) -> dict[str, any]:
        self.logger.info(f"发布Html指定看板 会话:{chatType}:{chatId}")
        self.logger.debug(f"发布的Html内容: {content}")
        return await self.NetJsonPost(
            self.local_board_api,
            self._gen_local_body(
                chatId, chatType, "html", content, memberId, expireTime
            ),
        )

    async def LocalDismiss(
        self, chatId: str, chatType: str, memberId: str = ""
    ) -> dict[str, any]:
        self.logger.info(f"撤销指定看板 会话:{chatType}:{chatId}")
        return await self.NetJsonPost(
            "https://chat-go.jwzhd.com/open-apis/v1/bot/board-dismiss?token="
            + self.yhToken,
            {"chatId": chatId, "chatType": chatType, "memberId": memberId},
        )

    async def GlobalText(self, content: str, expireTime: int = 0) -> dict[str, any]:
        self.logger.info(f"发布文公共看板 过期时间:{expireTime}")
        self.logger.debug(f"发布的文本内容: {content}")
        return await self.NetJsonPost(
            self.global_board_api, self._gen_global_body("text", content, expireTime)
        )

    async def GlobalMarkdown(self, content: str, expireTime: int = 0) -> dict[str, any]:
        self.logger.info(f"发布Markdown公共看板 过期时间:{expireTime}")
        self.logger.debug(f"发布的Markdown内容: {content}")
        return await self.NetJsonPost(
            self.global_board_api,
            self._gen_global_body("markdown", content, expireTime),
        )

    async def GlobalHtml(self, content: str, expireTime: int = 0) -> dict[str, any]:
        self.logger.info(f"发布Html公共看板 过期时间:{expireTime}")
        self.logger.debug(f"发布的Html内容: {content}")
        return await self.NetJsonPost(
            self.global_board_api, self._gen_global_body("html", content, expireTime)
        )

    async def GlobalDismiss(self) -> dict[str, any]:
        self.logger.info("撤销所有公共看板")
        return await self.NetJsonPost(
            "https://chat-go.jwzhd.com/open-apis/v1/bot/board-all-dismiss?token="
            + self.yhToken,
            {},
        )
