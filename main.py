from direct.showbase.ShowBase import ShowBase


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.model = self.loader.loadModel("models/room.ply")
        # self.model = self.loader.loadModel("models/panda-model")
        self.model.showTightBounds()
        self.model.reparentTo(self.render)
        self.model.ls()
        print("\nself.model.getTightBounds():")
        print(self.model.getTightBounds())
        print("\nself.model.analyze():")
        self.model.analyze()

app = MyApp()
app.run()
