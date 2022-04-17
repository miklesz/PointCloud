import direct.directbase.DirectStart
from direct.showutil.Rope import Rope

r = Rope()
r.setup(4, [(None, (-10, 0, 0)),
            (None, (0, 0, 15)),
            (None, (6, 100, -12)),
            (None, (10, 0, 0))])
r.setPos(0, 30, 0)
r.reparentTo(base.render)
r.ropeNode.setNumSubdiv(30)

base.run()
