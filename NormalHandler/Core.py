class Main:
    def __init__(self, sdk, logger):
        self.on = "message.receive.normal"
        self.handles: list[object] = []

    def AddHandle(self, handle):
        self.handles.append(handle)

    async def OnRecv(self, data):
        for handle in self.handles:
            await handle(data)