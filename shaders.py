from direct.showbase.ShowBase import ShowBase
import platform
base = ShowBase()
print('platform.machine:', platform.machine())
print('base.win.gsg.supports_basic_shaders:', base.win.gsg.supports_basic_shaders)
