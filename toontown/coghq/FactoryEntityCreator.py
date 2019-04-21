from otp.level import EntityCreator
from . import FactoryLevelMgr
from . import PlatformEntity
from . import ConveyorBelt
from . import GearEntity
from . import PaintMixer
from . import GoonClipPlane
from . import MintProduct
from . import MintProductPallet
from . import MintShelf
from . import PathMasterEntity
from . import RenderingEntity

class FactoryEntityCreator(EntityCreator.EntityCreator):

    def __init__(self, level):
        EntityCreator.EntityCreator.__init__(self, level)
        nothing = EntityCreator.nothing
        factorynonlocal = EntityCreator.entitynonlocal
        self.privRegisterTypes({'activeCell': factorynonlocal,
         'crusherCell': factorynonlocal,
         'battleBlocker': factorynonlocal,
         'beanBarrel': factorynonlocal,
         'button': factorynonlocal,
         'conveyorBelt': ConveyorBelt.ConveyorBelt,
         'crate': factorynonlocal,
         'door': factorynonlocal,
         'directionalCell': factorynonlocal,
         'gagBarrel': factorynonlocal,
         'gear': GearEntity.GearEntity,
         'goon': factorynonlocal,
         'gridGoon': factorynonlocal,
         'golfGreenGame': factorynonlocal,
         'goonClipPlane': GoonClipPlane.GoonClipPlane,
         'grid': factorynonlocal,
         'healBarrel': factorynonlocal,
         'levelMgr': FactoryLevelMgr.FactoryLevelMgr,
         'lift': factorynonlocal,
         'mintProduct': MintProduct.MintProduct,
         'mintProductPallet': MintProductPallet.MintProductPallet,
         'mintShelf': MintShelf.MintShelf,
         'mover': factorynonlocal,
         'paintMixer': PaintMixer.PaintMixer,
         'pathMaster': PathMasterEntity.PathMasterEntity,
         'rendering': RenderingEntity.RenderingEntity,
         'platform': PlatformEntity.PlatformEntity,
         'sinkingPlatform': factorynonlocal,
         'stomper': factorynonlocal,
         'stomperPair': factorynonlocal,
         'laserField': factorynonlocal,
         'securityCamera': factorynonlocal,
         'elevatorMarker': factorynonlocal,
         'trigger': factorynonlocal,
         'moleField': factorynonlocal,
         'maze': factorynonlocal})
