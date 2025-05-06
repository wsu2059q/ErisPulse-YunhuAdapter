class Main:
    def __init__(self, sdk, logger):
        self.on = "message.receive.instruction"
        self.handles: dict[list[object]] = {"ALL": []}
        self.logger = logger

    def AddHandle(self, handle, cmdid="ALL"):
        if cmdid not in self.handles:
            self.handles[cmdid] = []
            self.logger.debug(f"新增指令ID分类: {cmdid}")
        self.handles[cmdid].append(handle)
        self.logger.info(f"添加了新的指令处理器 ~ 指令ID: {cmdid}")

    async def OnRecv(self, data):
        try:
            if "instructionId" in data["event"]["message"]:
                cmdid = data["event"]["message"]["instructionId"]
                self.logger.debug(f"收到指令消息: {cmdid} | 类型: instruction")
            else:
                cmdid = data["event"]["message"]["commandId"]
                self.logger.debug(f"收到指令消息: {cmdid} | 类型: command")
            
            self.logger.info(f"开始处理指令: {cmdid}")
            
            specific_handles = self.handles.get(cmdid, [])
            all_handles = self.handles.get("ALL", [])
            
            for handle in specific_handles:
                await handle(data)

            for handle in all_handles:
                await handle(data)
        except Exception as e:
            self.logger.error(f"处理指令时出错啦 (╥﹏╥): {str(e)} | 指令ID: {cmdid}")
            raise
