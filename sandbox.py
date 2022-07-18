# Related third party imports
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.interval.IntervalGlobal import *

# Local application/library specific imports
from particles import *

# Constants
RING_START = 5.0
RING_STOP = 0.0

base = ShowBase()

base.setBackgroundColor(0, 0, 0)

local_props = WindowProperties()
local_props.setSize(base.pipe.getDisplayWidth(), base.pipe.getDisplayHeight())
local_props.setOrigin((-2, -2))
base.win.requestProperties(local_props)

base.enableParticles()

ring_intervals = []
ring_parents = []
for ring_i in range(13):
    ring_parents.append(base.render.attachNewNode(f'ring parent {ring_i}'))
    ring_y = (RING_STOP-RING_START)*(ring_i+1)/14+RING_START
    # print(ring_y)
    ring_parents[ring_i].setPosHpr(0, ring_y, 0, 0, 90, 0)
    ring_intervals.append(
        ParticleInterval(
            particleEffect=init_ring_particle_effect(
                point_size=10,
            ),
            parent=ring_parents[ring_i],
            worldRelative=False,
            duration=.34,
            # softStopT=-.5,
            cleanup=True,
            name=f'ring interval {ring_i}',
        )
    )

sequence = Sequence()
for ring_i in range(13):
    # sequence.append(Wait(.34))
    sequence.append(ring_intervals[12-ring_i])

#     Wait(1),
#     ring_interval,
# )
#
sequence.start()

base.run()
