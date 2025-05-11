from aiohttp import web
import asyncio
import socket

class Main:
    def __init__(self, sdk):
        self.sdk = sdk
        self.logger = sdk.logger
        self.triggers: dict[str, list[object]] = {}
        self.app = web.Application()
        self.runner = None
        self.site = None

        self.YunhuAdapterConfig = sdk.env.get("YunhuAdapter", {}).get("Server", {})
        if not self.YunhuAdapterConfig:
            self.logger.error("未找到 YunhuAdapterConfig 配置项，将使用默认配置")
            self.logger.warning("""您可以通过env.py或程序入库进行以下设置:
            sdk.env.set('YunhuAdapter',{
                "Server":{
                    "host": "127.0.0.1",
                    "port": 8080,
                    "path": "/"
                },
                "token": ""
            })
            """)

        self.host = self.YunhuAdapterConfig.get("host", "127.0.0.1")
        self.port = self.YunhuAdapterConfig.get("port", 8080)
        self.path = self.YunhuAdapterConfig.get("path", "/")
        self.app.router.add_post(self.path, self.Handle)

    def AddTrigger(self, trigger: object):
        t_names = getattr(trigger, "on", None)
        if isinstance(t_names, list):
            for t_name in t_names:
                if t_name not in self.triggers:
                    self.triggers[t_name] = []
                self.triggers[t_name].append(trigger)
                self.logger.debug(f"成功注册触发器: 事件类型={t_name}, 触发器={trigger}")
        else:
            if t_names not in self.triggers:
                self.triggers[t_names] = []
            self.triggers[t_names].append(trigger)
            self.logger.debug(f"成功注册触发器: 事件类型={t_names}, 触发器={trigger}")

    async def Handle(self, request: web.Request) -> web.Response:
        try:
            data = await request.json()
            self.logger.debug(f"收到数据， 数据内容: {data}")
            self.logger.info(f"收到请求类型: {data['header']['eventType']}")
            
            t_name = data["header"]["eventType"]
            if t_name not in self.triggers or len(self.triggers[t_name]) == 0:
                self.logger.warning(f"没有找到 {t_name} 事件的触发器哦")
                return web.Response(text="IGNORE", status=200)

            self.logger.debug(f"开始处理事件: {t_name} | 触发器数量: {len(self.triggers[t_name])} 个")
            for trigger in self.triggers[t_name]:
                await trigger.OnRecv(data)

            return web.Response(text="OK", status=200)
        except Exception as e:
            self.logger.error(f"处理请求时出错啦 (╥﹏╥): {str(e)} | 请求数据: {data if 'data' in locals() else '无数据'}")
            return web.Response(text=f"ERROR: {str(e)}", status=500)

    async def Start(self):
        if not self.is_port_available(self.host, self.port):
            self.logger.error(f"端口被占用啦: {self.host}:{self.port}")
            return
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, host=self.host, port=self.port)
        await self.site.start()
        start_msg = f"Server started at http://{self.host}:{self.port}{self.path}"
        self.logger.info(f"服务器启动成功! | 地址: {start_msg}")
        trigger_info = "\n".join(
            f"  事件类型: {event_type}, "
            f"触发器: {[f'{t.__module__}.{t.__class__.__name__}' for t in triggers]}"
            for event_type, triggers in self.triggers.items()
        )
        self.logger.debug(f"触发器列表:\n{trigger_info}")

    async def Stop(self):
        if self.site:
            await self.site.stop()
            self.logger.info("服务器站点已停止 zzz")
        if self.runner:
            await self.runner.cleanup()
            self.logger.debug("服务器运行器已清理干净啦")

    async def Run(self):
        try:
            self.logger.info("正在启动服务器... 请稍等")
            asyncio.create_task(self.Start())
            while True:
                try:
                    await asyncio.sleep(1)
                except asyncio.CancelledError:
                    break
        except (KeyboardInterrupt, SystemExit):
            self.logger.info("收到停止信号啦! 正在关闭服务器...")
            self.logger.debug(f"最后状态检查: 触发器数量 - {sum(len(v) for v in self.triggers.values())}")
        finally:
            await self.Stop()

    @staticmethod
    def is_port_available(host: str, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                return True
            except OSError:
                return False
