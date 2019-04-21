from otp.level import EntityCreatorAI
from direct.showbase.PythonUtil import Functor
from . import DistributedBeanBarrelAI
from . import DistributedButtonAI
from . import DistributedCrateAI
from . import DistributedLiftAI
from . import DistributedDoorEntityAI
from . import DistributedGagBarrelAI
from . import DistributedGridAI
from toontown.suit import DistributedGridGoonAI
from toontown.suit import DistributedGoonAI
from . import DistributedHealBarrelAI
from . import DistributedStomperPairAI
from . import DistributedTriggerAI
from . import DistributedStomperAI
from . import DistributedLaserFieldAI
from . import DistributedSecurityCameraAI
from . import DistributedMoverAI
from . import DistributedElevatorMarkerAI
from . import DistributedSinkingPlatformAI
from . import ActiveCellAI
from . import CrusherCellAI
from . import DirectionalCellAI
from . import FactoryLevelMgrAI
from . import BattleBlockerAI
from . import DistributedGolfGreenGameAI
from toontown.coghq import DistributedMoleFieldAI
from toontown.coghq import DistributedMazeAI

class FactoryEntityCreatorAI(EntityCreatorAI.EntityCreatorAI):

    def __init__(self, level):
        EntityCreatorAI.EntityCreatorAI.__init__(self, level)
        cDE = EntityCreatorAI.createDistributedEntity
        cLE = EntityCreatorAI.createLocalEntity
        nothing = EntityCreatorAI.nothing
        self.privRegisterTypes({'activeCell': Functor(cDE, ActiveCellAI.ActiveCellAI),
         'crusherCell': Functor(cDE, CrusherCellAI.CrusherCellAI),
         'battleBlocker': Functor(cDE, BattleBlockerAI.BattleBlockerAI),
         'beanBarrel': Functor(cDE, DistributedBeanBarrelAI.DistributedBeanBarrelAI),
         'button': DistributedButtonAI.DistributedButtonAI,
         'conveyorBelt': nothing,
         'crate': Functor(cDE, DistributedCrateAI.DistributedCrateAI),
         'directionalCell': Functor(cDE, DirectionalCellAI.DirectionalCellAI),
         'door': DistributedDoorEntityAI.DistributedDoorEntityAI,
         'gagBarrel': Functor(cDE, DistributedGagBarrelAI.DistributedGagBarrelAI),
         'gear': nothing,
         'goon': Functor(cDE, DistributedGoonAI.DistributedGoonAI),
         'gridGoon': Functor(cDE, DistributedGridGoonAI.DistributedGridGoonAI),
         'golfGreenGame': Functor(cDE, DistributedGolfGreenGameAI.DistributedGolfGreenGameAI),
         'goonClipPlane': nothing,
         'grid': Functor(cDE, DistributedGridAI.DistributedGridAI),
         'healBarrel': Functor(cDE, DistributedHealBarrelAI.DistributedHealBarrelAI),
         'levelMgr': Functor(cLE, FactoryLevelMgrAI.FactoryLevelMgrAI),
         'lift': Functor(cDE, DistributedLiftAI.DistributedLiftAI),
         'mintProduct': nothing,
         'mintProductPallet': nothing,
         'mintShelf': nothing,
         'mover': Functor(cDE, DistributedMoverAI.DistributedMoverAI),
         'paintMixer': nothing,
         'pathMaster': nothing,
         'rendering': nothing,
         'platform': nothing,
         'sinkingPlatform': Functor(cDE, DistributedSinkingPlatformAI.DistributedSinkingPlatformAI),
         'stomper': Functor(cDE, DistributedStomperAI.DistributedStomperAI),
         'stomperPair': Functor(cDE, DistributedStomperPairAI.DistributedStomperPairAI),
         'laserField': Functor(cDE, DistributedLaserFieldAI.DistributedLaserFieldAI),
         'securityCamera': Functor(cDE, DistributedSecurityCameraAI.DistributedSecurityCameraAI),
         'elevatorMarker': Functor(cDE, DistributedElevatorMarkerAI.DistributedElevatorMarkerAI),
         'trigger': DistributedTriggerAI.DistributedTriggerAI,
         'moleField': Functor(cDE, DistributedMoleFieldAI.DistributedMoleFieldAI),
         'maze': Functor(cDE, DistributedMazeAI.DistributedMazeAI)})
