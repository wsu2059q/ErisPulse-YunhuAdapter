
class Main:
    def __init__(self, sdk):
        self.sdk = sdk
        self.logger = sdk.logger
        self.yhToken = sdk.YunhuMessageBase.yhToken
        self.apiUrl = (
            "https://chat-go.jwzhd.com/open-apis/v1/bot/send?token=" + self.yhToken
        )
        self.NetJsonPost = sdk.YunhuMessageBase.NetJsonPost
        self.NetFileUpload = sdk.YunhuMessageBase.NetFileUpload

    def _gen_body(
        self,
        recvId: str,
        recvType: str,
        contentType: str,
        content: dict[str, any],
        parentId: str,
    ) -> dict[str, any]:
        return {
            "recvId": recvId,
            "recvType": recvType,
            "contentType": contentType,
            "content": content,
            "parentId": parentId,
        }

    async def Text(
        self,
        recvId: str,
        recvType: str,
        content: str,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        self.logger.info(f"准备发送文本消息给 {recvType}:{recvId}")
        self.logger.debug(f"消息内容: {content} | 按钮数量: {len(buttons)}")
        result = await self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvId,
                recvType,
                "text",
                {"text": content, "buttons": buttons},
                parentId,
            ),
        )

    async def Markdown(
        self,
        recvId: str,
        recvType: str,
        content: str,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        self.logger.info(f"准备发送Markdown消息给 {recvType}:{recvId}")
        self.logger.debug(f"Markdown内容: {content} | 按钮数量: {len(buttons)}")
        result = await self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvId,
                recvType,
                "markdown",
                {"text": content, "buttons": buttons},
                parentId,
            ),
        )

    async def Html(
        self,
        recvId: str,
        recvType: str,
        content: str,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        self.logger.info(f"准备发送HTML消息给 {recvType}:{recvId}")
        self.logger.debug(f"HTML内容: {content} | 按钮数量: {len(buttons)}")
        result = await self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvId,
                recvType,
                "html",
                {"text": content, "buttons": buttons},
                parentId,
            ),
        )

    async def Image(
        self,
        recvId: str,
        recvType: str,
        content: bytes,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        self.logger.info(f"准备发送图片给 {recvType}:{recvId} 图片大小: {len(content)/1024:.2f}KB")
        upload_result = await self.NetFileUpload(
            "https://chat-go.jwzhd.com/open-apis/v1/image/upload?token="
            + self.yhToken,
            "image",
            content,
        )
        self.logger.debug(f"图片上传成功! Key: {upload_result['data']['imageKey']}")
        result = await self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvId,
                recvType,
                "image",
                {"imageKey": upload_result["data"]["imageKey"], "buttons": buttons},
                parentId,
            ),
        )

    async def Video(
        self,
        recvId: str,
        recvType: str,
        content: bytes,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        self.logger.info(f"准备发送视频给 {recvType}:{recvId} 视频大小: {len(content)/1024:.2f}KB")
        upload_result = await self.NetFileUpload(
            "https://chat-go.jwzhd.com/open-apis/v1/video/upload?token=" + self.yhToken,
            "video",
            content,
        )
        self.logger.debug(f"视频上传结果: {upload_result}")
        if "data" not in upload_result or "videoKey" not in upload_result["data"]:
            self.logger.error("视频上传失败啦 (╥﹏╥) 返回结构无效!")
            raise ValueError("Invalid upload_result structure:", upload_result)
        self.logger.info(f"视频上传成功! Key: {upload_result['data']['videoKey']}")
        result = await self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvId,
                recvType,
                "video",
                {"videoKey": upload_result["data"]["videoKey"], "buttons": buttons},
                parentId,
            ),
        )

    async def File(
        self,
        recvId: str,
        recvType: str,
        content: bytes,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        self.logger.info(f"准备发送文件给 {recvType}:{recvId} 文件大小: {len(content)/1024:.2f}KB")
        upload_result = await self.NetFileUpload(
            "https://chat-go.jwzhd.com/open-apis/v1/file/upload?token="
            + self.yhToken,
            "file",
            content,
        )
        self.logger.debug(f"文件上传成功! Key: {upload_result['data']['fileKey']}")
        result = await self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvId,
                recvType,
                "file",
                {"fileKey": upload_result["data"]["fileKey"], "buttons": buttons},
                parentId,
            ),
        )
