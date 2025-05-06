import io
import mimetypes
import aiohttp
import filetype


class Main:
    def __init__(self, sdk):
        self.sdk = sdk
        self.logger = sdk.logger
        self.yhToken = sdk.env.get("YunhuAdapter", {}).get("token", "0")
        if self.yhToken == "0":
            self.logger.warning(
                "未配置云湖令牌，可能会导致一些功能无法使用哦"
            )

    async def NetJsonGet(self, url) -> dict[str, any]:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                return await response.json()

    async def NetJsonPost(self, url, data) -> dict[str, any]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=url, headers={"Content-Type": "application/json"}, json=data
            ) as response:
                return await response.json()

    async def NetFileUpload(self, url, field_name, file_bytes) -> dict[str, any]:
        file_name = "file.{}".format(filetype.guess(file_bytes).extension)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=url,
                data={
                    field_name: (
                        file_name,
                        io.BufferedReader(io.BytesIO(file_bytes)),
                        mimetypes.guess_type(file_name)[0],
                    )
                },
            ) as response:
                return await response.json()