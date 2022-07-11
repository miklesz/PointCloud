import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
# from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
import time

# Add some text
# bk_text = "This is my Demo"
# textObject = OnscreenText(text=bk_text, pos=(0.95, -0.95), scale=0.07,
#                           fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter,
#                           mayChange=1)

# Callback function to set text
# def incBar(arg):
#     bar['value'] += arg
#     text = "Progress is:" + str(bar['value']) + '%'
#     textObject.setText(text)

# Create a frame
# frame = DirectFrame(text="main", scale=0.001)
# Add button
# bar = DirectWaitBar(text="ABC", value=50, pos=(0, .4, .4))
# bar = DirectWaitBar(value=50, pos=(0, 0, 0))
# bar = DirectWaitBar(value=50)
# base = ShowBase()
bar = DirectWaitBar()
# bar['value'] = 75
# bar.destroy()

# Create 4 buttons
# button_1 = DirectButton(text="+1", scale=0.05, pos=(-.3, .6, 0),
#                         command=incBar, extraArgs=[1])
# button_10 = DirectButton(text="+10", scale=0.05, pos=(0, .6, 0),
#                          command=incBar, extraArgs=[10])
# button_m1 = DirectButton(text="-1", scale=0.05, pos=(0.3, .6, 0),
#                          command=incBar, extraArgs=[-1])
# button_m10 = DirectButton(text="-10", scale=0.05, pos=(0.6, .6, 0),
#                           command=incBar, extraArgs=[-10])

# Run the tutorial
base.taskMgr.step(), base.taskMgr.step()
time.sleep(1)
bar['value'] = 50
base.taskMgr.step(), base.taskMgr.step()
time.sleep(1)
bar['value'] = 75
base.taskMgr.step(), base.taskMgr.step()
time.sleep(1)

# base.run()