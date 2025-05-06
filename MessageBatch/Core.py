class Main:
    def __init__(self, sdk):
        self.sdk = sdk
        self.logger = sdk.logger
        self.yhToken = sdk.MessageBase.yhToken
        self.apiUrl = (
            "https://chat-go.jwzhd.com/open-apis/v1/bot/batch_send?token="
            + self.yhToken
        )
        self.NetJsonPost = sdk.MessageBase.NetJsonPost
        self.NetFileUpload = sdk.MessageBase.NetFileUpload
    def _gen_body(
        self,
        recvIds: list[str],
        recvType: str,
        contentType: str,
        content: dict[str, any],
        parentId: str,
    ) -> dict[str, any]:
        return {
            "recvIds": recvIds,
            "recvType": recvType,
            "contentType": contentType,
            "content": content,
            "parentId": parentId,
        }

    async def Text(
        self,
        recvIds: list[str],
        recvType: str,
        content: str,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        self.logger.info(f"发送批量文本消息 接收类型:{recvType} 接收者数量:{len(recvIds)}")
        self.logger.debug(f"发送的文本内容: {content}")
        return await self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvIds,
                recvType,
                "text",
                {"text": content, "buttons": buttons},
                parentId,
            ),
        )

    async def Markdown(
        self,
        recvIds: list[str],
        recvType: str,
        content: str,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        self.logger.info(f"发送批量Markdown消息 接收类型:{recvType} 接收者数量:{len(recvIds)}")
        self.logger.debug(f"发送的Markdown内容: {content}")
        return await self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvIds,
                recvType,
                "markdown",
                {"text": content, "buttons": buttons},
                parentId,
            ),
        )

    async def Html(
        self,
        recvIds: list[str],
        recvType: str,
        content: str,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        self.logger.info(f"发送批量HTML消息 接收类型:{recvType} 接收者数量:{len(recvIds)}")
        self.logger.debug(f"发送的HTML内容: {content}")
        return await self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvIds,
                recvType,
                "html",
                {"text": content, "buttons": buttons},
                parentId,
            ),
        )

    async def Image(
        self,
        recvIds: list[str],
        recvType: str,
        content: bytes,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        self.logger.info(f"上传并发送批量图片 接收类型:{recvType} 接收者数量:{len(recvIds)} 图片大小:{len(content)/1024:.2f}KB")
        upload_result = await self.NetFileUpload(
            "https://chat-go.jwzhd.com/open-apis/v1/image/upload?token="
            + self.yhToken,
            "image",
            content,
        )
        return await self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvIds,
                recvType,
                "image",
                {"imageKey": upload_result["data"]["imageKey"], "buttons": buttons},
                parentId,
            ),
        )

    async def Video(
        self,
        recvIds: list[str],
        recvType: str,
        content: bytes,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        self.logger.info(f"上传并发送批量视频 接收类型:{recvType} 接收者数量:{len(recvIds)} 视频大小:{len(content)/1024:.2f}KB")
        upload_result = await self.NetFileUpload(
            "https://chat-go.jwzhd.com/open-apis/v1/video/upload?token="
            + self.yhToken,
            "video",
            content,
        )
        return await self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvIds,
                recvType,
                "video",
                {"videoKey": upload_result["data"]["videoKey"], "buttons": buttons},
                parentId,
            ),
        )

    async def File(
        self,
        recvIds: list[str],
        recvType: str,
        content: bytes,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        self.logger.info(f"上传并发送批量文件 接收类型:{recvType} 接收者数量:{len(recvIds)} 文件大小:{len(content)/1024:.2f}KB")
        upload_result = await self.NetFileUpload(
            "https://chat-go.jwzhd.com/open-apis/v1/file/upload?token="
            + self.yhToken,
            "file",
            content,
        )
        return await self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvIds,
                recvType,
                "file",
                {"fileKey": upload_result["data"]["fileKey"], "buttons": buttons},
                parentId,
            ),
        )
