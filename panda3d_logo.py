from direct.showbase.ShowBase import ShowBase
from panda3d_logos.splashes import RainbowSplash
# from panda3d_logos.splashes import WindowSplash

base = ShowBase()

splash = RainbowSplash()
# splash = WindowSplash()
interval = splash.setup()  # This'll change the scene graph, in
                           # particular reparent the cam!
# interval is a Panda3D interval you can .start() it now
interval.start()
# splash.teardown()          # To de-litter your state.

base.run()
