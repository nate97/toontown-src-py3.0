import TTLocalizer
from otp.otpbase.OTPGlobals import *
from direct.showbase.PythonUtil import Enum, invertDict
from panda3d.core import BitMask32, Vec4

from toontown.toonbase.HolidayGlobals import *

MapHotkeyOn = 'alt'
MapHotkeyOff = 'alt-up'
MapHotkey = 'alt'
AccountDatabaseChannelId = 4008
ToonDatabaseChannelId = 4021
DoodleDatabaseChannelId = 4023
DefaultDatabaseChannelId = AccountDatabaseChannelId
DatabaseIdFromClassName = {'Account': AccountDatabaseChannelId}
CogHQCameraFov = 60.0
BossBattleCameraFov = 72.0
MakeAToonCameraFov = 48.0
VPElevatorFov = 53.0
CFOElevatorFov = 43.0
CJElevatorFov = 59.0
CEOElevatorFov = 59.0
CBElevatorFov = 42.0
WantPromotion = 0
PendingPromotion = 1
CeilingBitmask = BitMask32(256)
FloorEventBitmask = BitMask32(16)
PieBitmask = BitMask32(256)
PetBitmask = BitMask32(8)
CatchGameBitmask = BitMask32(16)
CashbotBossObjectBitmask = BitMask32(16)
FurnitureSideBitmask = BitMask32(32)
FurnitureTopBitmask = BitMask32(64)
FurnitureDragBitmask = BitMask32(128)
PetLookatPetBitmask = BitMask32(256)
PetLookatNonPetBitmask = BitMask32(512)
BanquetTableBitmask = BitMask32(1024)
FullPies = 65535
CogHQCameraFar = 900.0
CogHQCameraNear = 1.0
CashbotHQCameraFar = 2000.0
CashbotHQCameraNear = 1.0
LawbotHQCameraFar = 3000.0
LawbotHQCameraNear = 1.0
BossbotHQCameraFar = 3000.0
BossbotHQCameraNear = 1.0
SpeedwayCameraFar = 8000.0
SpeedwayCameraNear = 1.0
MaxMailboxContents = 30
MaxHouseItems = 45
MaxAccessories = 50
ExtraDeletedItems = 5
DeletedItemLifetime = 7 * 24 * 60
CatalogNumWeeksPerSeries = 13
CatalogNumWeeks = 78
PetFloorCollPriority = 5
PetPanelProximityPriority = 6
P_NoTrunk = -28
P_AlreadyOwnBiggerCloset = -27
P_ItemAlreadyRented = -26
P_OnAwardOrderListFull = -25
P_AwardMailboxFull = -24
P_ItemInPetTricks = -23
P_ItemInMyPhrases = -22
P_ItemOnAwardOrder = -21
P_ItemInAwardMailbox = -20
P_ItemAlreadyWorn = -19
P_ItemInCloset = -18
P_ItemOnGiftOrder = -17
P_ItemOnOrder = -16
P_ItemInMailbox = -15
P_PartyNotFound = 14
P_WillNotFit = -13
P_NotAGift = -12
P_OnOrderListFull = -11
P_MailboxFull = -10
P_NoPurchaseMethod = -9
P_ReachedPurchaseLimit = -8
P_NoRoomForItem = -7
P_NotShopping = -6
P_NotAtMailbox = -5
P_NotInCatalog = -4
P_NotEnoughMoney = -3
P_InvalidIndex = -2
P_UserCancelled = -1
P_ItemAvailable = 1
P_ItemOnOrder = 2
P_ItemUnneeded = 3
GIFT_user = 0
GIFT_admin = 1
GIFT_RAT = 2
GIFT_mobile = 3
GIFT_cogs = 4
GIFT_partyrefund = 5
FM_InvalidItem = -7
FM_NondeletableItem = -6
FM_InvalidIndex = -5
FM_NotOwner = -4
FM_NotDirector = -3
FM_RoomFull = -2
FM_HouseFull = -1
FM_MovedItem = 1
FM_SwappedItem = 2
FM_DeletedItem = 3
FM_RecoveredItem = 4
SPDonaldsBoat = 3
SPMinniesPiano = 4
CEVirtual = 14
MaxHpLimit = 137
MaxCarryLimit = 80
MaxQuestCarryLimit = 4
GravityValue = 32.174
MaxCogSuitLevel = 12 - 1
setInterfaceFont(TTLocalizer.InterfaceFont)
setSignFont(TTLocalizer.SignFont)
from toontown.toontowngui import TTDialog
setDialogClasses(TTDialog.TTDialog, TTDialog.TTGlobalDialog)
ToonFont = None
BuildingNametagFont = None
MinnieFont = None
SuitFont = None

def getToonFont():
    global ToonFont
    if ToonFont == None:
        ToonFont = loader.loadFont(TTLocalizer.ToonFont, lineHeight=1.0)
    return ToonFont


def getBuildingNametagFont():
    global BuildingNametagFont
    if BuildingNametagFont == None:
        BuildingNametagFont = loader.loadFont(TTLocalizer.BuildingNametagFont)
    return BuildingNametagFont


def getMinnieFont():
    global MinnieFont
    if MinnieFont == None:
        MinnieFont = loader.loadFont(TTLocalizer.MinnieFont)
    return MinnieFont


def getSuitFont():
    global SuitFont
    if SuitFont == None:
        SuitFont = loader.loadFont(TTLocalizer.SuitFont, pixelsPerUnit=40, spaceAdvance=0.25, lineHeight=1.0)
    return SuitFont


DonaldsDock = 1000
ToontownCentral = 2000
TheBrrrgh = 3000
MinniesMelodyland = 4000
DaisyGardens = 5000
OutdoorZone = 6000
FunnyFarm = 7000
GoofySpeedway = 8000
DonaldsDreamland = 9000
BarnacleBoulevard = 1100
SeaweedStreet = 1200
LighthouseLane = 1300
SillyStreet = 2100
LoopyLane = 2200
PunchlinePlace = 2300
WalrusWay = 3100
SleetStreet = 3200
PolarPlace = 3300
AltoAvenue = 4100
BaritoneBoulevard = 4200
TenorTerrace = 4300
ElmStreet = 5100
MapleStreet = 5200
OakStreet = 5300
LullabyLane = 9100
PajamaPlace = 9200
ToonHall = 2513
HoodHierarchy = {ToontownCentral: (SillyStreet, LoopyLane, PunchlinePlace),
 DonaldsDock: (BarnacleBoulevard, SeaweedStreet, LighthouseLane),
 TheBrrrgh: (WalrusWay, SleetStreet, PolarPlace),
 MinniesMelodyland: (AltoAvenue, BaritoneBoulevard, TenorTerrace),
 DaisyGardens: (ElmStreet, MapleStreet, OakStreet),
 DonaldsDreamland: (LullabyLane, PajamaPlace),
 GoofySpeedway: ()}
WelcomeValleyToken = 0
BossbotHQ = 10000
BossbotLobby = 10100
BossbotCountryClubIntA = 10500
BossbotCountryClubIntB = 10600
BossbotCountryClubIntC = 10700
SellbotHQ = 11000
SellbotLobby = 11100
SellbotFactoryExt = 11200
SellbotFactoryInt = 11500
CashbotHQ = 12000
CashbotLobby = 12100
CashbotMintIntA = 12500
CashbotMintIntB = 12600
CashbotMintIntC = 12700
LawbotHQ = 13000
LawbotLobby = 13100
LawbotOfficeExt = 13200
LawbotOfficeInt = 13300
LawbotStageIntA = 13300
LawbotStageIntB = 13400
LawbotStageIntC = 13500
LawbotStageIntD = 13600
Tutorial = 15000
MyEstate = 16000
GolfZone = 17000
PartyHood = 18000
HoodsAlwaysVisited = [17000, 18000]
WelcomeValleyBegin = 22000
WelcomeValleyEnd = 61000
DynamicZonesBegin = 61000
DynamicZonesEnd = 1 << 20
cogDept2index = {'c': 0,
 'l': 1,
 'm': 2,
 's': 3}
cogIndex2dept = invertDict(cogDept2index)
HQToSafezone = {SellbotHQ: DaisyGardens,
 CashbotHQ: DonaldsDreamland,
 LawbotHQ: TheBrrrgh,
 BossbotHQ: DonaldsDock}
CogDeptNames = [TTLocalizer.Bossbot,
 TTLocalizer.Lawbot,
 TTLocalizer.Cashbot,
 TTLocalizer.Sellbot]

def cogHQZoneId2deptIndex(zone):
    if zone >= 13000 and zone <= 13999:
        return 1
    elif zone >= 12000:
        return 2
    elif zone >= 11000:
        return 3
    else:
        return 0


def cogHQZoneId2dept(zone):
    return cogIndex2dept[cogHQZoneId2deptIndex(zone)]


def dept2cogHQ(dept):
    dept2hq = {'c': BossbotHQ,
     'l': LawbotHQ,
     'm': CashbotHQ,
     's': SellbotHQ}
    return dept2hq[dept]


MockupFactoryId = 0
MintNumFloors = {CashbotMintIntA: 20,
 CashbotMintIntB: 20,
 CashbotMintIntC: 20}
CashbotMintCogLevel = 10
CashbotMintSkelecogLevel = 11
CashbotMintBossLevel = 12
MintNumBattles = {CashbotMintIntA: 4,
 CashbotMintIntB: 6,
 CashbotMintIntC: 8}
MintCogBuckRewards = {CashbotMintIntA: 8,
 CashbotMintIntB: 14,
 CashbotMintIntC: 20}
MintNumRooms = {CashbotMintIntA: 2 * (6,) + 5 * (7,) + 5 * (8,) + 5 * (9,) + 3 * (10,),
 CashbotMintIntB: 3 * (8,) + 6 * (9,) + 6 * (10,) + 5 * (11,),
 CashbotMintIntC: 4 * (10,) + 10 * (11,) + 6 * (12,)}
BossbotCountryClubCogLevel = 11
BossbotCountryClubSkelecogLevel = 12
BossbotCountryClubBossLevel = 12
CountryClubNumRooms = {BossbotCountryClubIntA: (4,),
 BossbotCountryClubIntB: 3 * (8,) + 6 * (9,) + 6 * (10,) + 5 * (11,),
 BossbotCountryClubIntC: 4 * (10,) + 10 * (11,) + 6 * (12,)}
CountryClubNumBattles = {BossbotCountryClubIntA: 3,
 BossbotCountryClubIntB: 2,
 BossbotCountryClubIntC: 3}
CountryClubCogBuckRewards = {BossbotCountryClubIntA: 8,
 BossbotCountryClubIntB: 14,
 BossbotCountryClubIntC: 20}
LawbotStageCogLevel = 10
LawbotStageSkelecogLevel = 11
LawbotStageBossLevel = 12
StageNumBattles = {LawbotStageIntA: 0,
 LawbotStageIntB: 0,
 LawbotStageIntC: 0,
 LawbotStageIntD: 0}
StageNoticeRewards = {LawbotStageIntA: 75,
 LawbotStageIntB: 150,
 LawbotStageIntC: 225,
 LawbotStageIntD: 300}
StageNumRooms = {LawbotStageIntA: 2 * (6,) + 5 * (7,) + 5 * (8,) + 5 * (9,) + 3 * (10,),
 LawbotStageIntB: 3 * (8,) + 6 * (9,) + 6 * (10,) + 5 * (11,),
 LawbotStageIntC: 4 * (10,) + 10 * (11,) + 6 * (12,),
 LawbotStageIntD: 4 * (10,) + 10 * (11,) + 6 * (12,)}
FT_FullSuit = 'fullSuit'
FT_Leg = 'leg'
FT_Arm = 'arm'
FT_Torso = 'torso'
factoryId2factoryType = {MockupFactoryId: FT_FullSuit,
 SellbotFactoryInt: FT_FullSuit,
 LawbotOfficeInt: FT_FullSuit}
StreetNames = TTLocalizer.GlobalStreetNames
StreetBranchZones = StreetNames.keys()
Hoods = (DonaldsDock,
 ToontownCentral,
 TheBrrrgh,
 MinniesMelodyland,
 DaisyGardens,
 OutdoorZone,
 FunnyFarm,
 GoofySpeedway,
 DonaldsDreamland,
 BossbotHQ,
 SellbotHQ,
 CashbotHQ,
 LawbotHQ,
 GolfZone)
HoodsForTeleportAll = (DonaldsDock,
 ToontownCentral,
 TheBrrrgh,
 MinniesMelodyland,
 DaisyGardens,
 OutdoorZone,
 GoofySpeedway,
 DonaldsDreamland,
 BossbotHQ,
 SellbotHQ,
 CashbotHQ,
 LawbotHQ,
 GolfZone)
BingoCardNames = {'normal': 0,
'corners': 1,
'diagonal': 2,
'threeway': 3,
'blockout': 4}
NoPreviousGameId = 0
RaceGameId = 1
CannonGameId = 2
TagGameId = 3
PatternGameId = 4
RingGameId = 5
MazeGameId = 6
TugOfWarGameId = 7
CatchGameId = 8
DivingGameId = 9
TargetGameId = 10
PairingGameId = 11
VineGameId = 12
IceGameId = 13
CogThiefGameId = 14
TwoDGameId = 15
PhotoGameId = 16
TravelGameId = 100
MinigameNames = {'race': RaceGameId,
 'cannon': CannonGameId,
 'tag': TagGameId,
 'pattern': PatternGameId,
 'minnie': PatternGameId,
 'match': PatternGameId,
 'matching': PatternGameId,
 'ring': RingGameId,
 'maze': MazeGameId,
 'tug': TugOfWarGameId,
 'catch': CatchGameId,
 'diving': DivingGameId,
 'target': TargetGameId,
 'pairing': PairingGameId,
 'vine': VineGameId,
 'ice': IceGameId,
 'thief': CogThiefGameId,
 '2d': TwoDGameId,
 'photo': PhotoGameId,
 'travel': TravelGameId}
MinigameTemplateId = -1
MinigameIDs = (RaceGameId,
 CannonGameId,
 TagGameId,
 PatternGameId,
 RingGameId,
 MazeGameId,
 TugOfWarGameId,
 CatchGameId,
 DivingGameId,
 TargetGameId,
 PairingGameId,
 VineGameId,
 IceGameId,
 CogThiefGameId,
 TwoDGameId,
 PhotoGameId,
 TravelGameId)
MinigamePlayerMatrix = {
    1: (CannonGameId, MazeGameId, TugOfWarGameId, RingGameId, VineGameId, CogThiefGameId, TwoDGameId, DivingGameId, PairingGameId, CatchGameId, TargetGameId, PhotoGameId),
    2: (CannonGameId, MazeGameId, TugOfWarGameId, PatternGameId, TagGameId, RingGameId, VineGameId, IceGameId, CogThiefGameId, TwoDGameId, DivingGameId, PairingGameId, CatchGameId, TargetGameId, PhotoGameId),
    3: (CannonGameId, MazeGameId, TugOfWarGameId, PatternGameId, RaceGameId, TagGameId, VineGameId, RingGameId, IceGameId, CogThiefGameId, TwoDGameId, DivingGameId, PairingGameId, CatchGameId, TargetGameId, PhotoGameId),
    4: (CannonGameId, MazeGameId, TugOfWarGameId, PatternGameId, RaceGameId, TagGameId, VineGameId, RingGameId, IceGameId, CogThiefGameId, TwoDGameId, DivingGameId, PairingGameId, CatchGameId, TargetGameId, PhotoGameId),
}
MinigameReleaseDates = {IceGameId: (2008, 8, 5),
 PhotoGameId: (2008, 8, 13),
 TwoDGameId: (2008, 8, 20),
 CogThiefGameId: (2008, 8, 27)}
KeyboardTimeout = 300
phaseMap = {Tutorial: 4,
 ToontownCentral: 4,
 MyEstate: 5.5,
 DonaldsDock: 6,
 MinniesMelodyland: 6,
 GoofySpeedway: 6,
 TheBrrrgh: 8,
 DaisyGardens: 8,
 FunnyFarm: 8,
 DonaldsDreamland: 8,
 OutdoorZone: 6,
 BossbotHQ: 12,
 SellbotHQ: 9,
 CashbotHQ: 10,
 LawbotHQ: 11,
 GolfZone: 6,
 PartyHood: 13}
streetPhaseMap = {ToontownCentral: 5,
 DonaldsDock: 6,
 MinniesMelodyland: 6,
 GoofySpeedway: 6,
 TheBrrrgh: 8,
 DaisyGardens: 8,
 FunnyFarm: 8,
 DonaldsDreamland: 8,
 OutdoorZone: 8,
 BossbotHQ: 12,
 SellbotHQ: 9,
 CashbotHQ: 10,
 LawbotHQ: 11,
 PartyHood: 13}
dnaMap = {Tutorial: 'toontown_central',
 ToontownCentral: 'toontown_central',
 DonaldsDock: 'donalds_dock',
 MinniesMelodyland: 'minnies_melody_land',
 GoofySpeedway: 'goofy_speedway',
 TheBrrrgh: 'the_burrrgh',
 DaisyGardens: 'daisys_garden',
 FunnyFarm: 'not done yet',
 DonaldsDreamland: 'donalds_dreamland',
 OutdoorZone: 'outdoor_zone',
 BossbotHQ: 'cog_hq_bossbot',
 SellbotHQ: 'cog_hq_sellbot',
 CashbotHQ: 'cog_hq_cashbot',
 LawbotHQ: 'cog_hq_lawbot',
 GolfZone: 'golf_zone'}
hoodNameMap = {DonaldsDock: TTLocalizer.DonaldsDock,
 ToontownCentral: TTLocalizer.ToontownCentral,
 TheBrrrgh: TTLocalizer.TheBrrrgh,
 MinniesMelodyland: TTLocalizer.MinniesMelodyland,
 DaisyGardens: TTLocalizer.DaisyGardens,
 OutdoorZone: TTLocalizer.OutdoorZone,
 FunnyFarm: TTLocalizer.FunnyFarm,
 GoofySpeedway: TTLocalizer.GoofySpeedway,
 DonaldsDreamland: TTLocalizer.DonaldsDreamland,
 BossbotHQ: TTLocalizer.BossbotHQ,
 SellbotHQ: TTLocalizer.SellbotHQ,
 CashbotHQ: TTLocalizer.CashbotHQ,
 LawbotHQ: TTLocalizer.LawbotHQ,
 Tutorial: TTLocalizer.Tutorial,
 MyEstate: TTLocalizer.MyEstate,
 GolfZone: TTLocalizer.GolfZone,
 PartyHood: TTLocalizer.PartyHood}
safeZoneCountMap = {MyEstate: 8,
 Tutorial: 6,
 ToontownCentral: 6,
 DonaldsDock: 10,
 MinniesMelodyland: 5,
 GoofySpeedway: 500,
 TheBrrrgh: 8,
 DaisyGardens: 9,
 FunnyFarm: 500,
 DonaldsDreamland: 5,
 OutdoorZone: 500,
 GolfZone: 500,
 PartyHood: 500}
townCountMap = {MyEstate: 8,
 Tutorial: 40,
 ToontownCentral: 37,
 DonaldsDock: 40,
 MinniesMelodyland: 40,
 GoofySpeedway: 40,
 TheBrrrgh: 40,
 DaisyGardens: 40,
 FunnyFarm: 40,
 DonaldsDreamland: 40,
 OutdoorZone: 40,
 PartyHood: 20}
hoodCountMap = {MyEstate: 2,
 Tutorial: 2,
 ToontownCentral: 2,
 DonaldsDock: 2,
 MinniesMelodyland: 2,
 GoofySpeedway: 2,
 TheBrrrgh: 2,
 DaisyGardens: 2,
 FunnyFarm: 2,
 DonaldsDreamland: 2,
 OutdoorZone: 2,
 BossbotHQ: 2,
 SellbotHQ: 43,
 CashbotHQ: 2,
 LawbotHQ: 2,
 GolfZone: 2,
 PartyHood: 2}
TrophyStarLevels = (10,
 20,
 30,
 50,
 75,
 100)
TrophyStarColors = (Vec4(0.9, 0.6, 0.2, 1),
 Vec4(0.9, 0.6, 0.2, 1),
 Vec4(0.8, 0.8, 0.8, 1),
 Vec4(0.8, 0.8, 0.8, 1),
 Vec4(1, 1, 0, 1),
 Vec4(1, 1, 0, 1))
MickeySpeed = 5.0
VampireMickeySpeed = 1.15
MinnieSpeed = 3.2
WitchMinnieSpeed = 1.8
DonaldSpeed = 3.68
FrankenDonaldSpeed = 0.9
DaisySpeed = 2.3
GoofySpeed = 5.2
SuperGoofySpeed = 1.6
PlutoSpeed = 5.5
WesternPlutoSpeed = 3.2
ChipSpeed = 3
DaleSpeed = 3.5
DaleOrbitDistance = 3
SuitWalkSpeed = 4.8
PieThrowArc = 0
PieThrowLinear = 1
PieCodeBossCog = 1
PieCodeNotBossCog = 2
PieCodeToon = 3
PieCodeBossInsides = 4
PieCodeDefensePan = 5
PieCodeProsecutionPan = 6
PieCodeLawyer = 7
PieCodeInvasionSuit = 8
PieCodeColors = {PieCodeBossCog: None,
 PieCodeNotBossCog: (0.8,
                     0.8,
                     0.8,
                     1),
 PieCodeToon: None}
suitIndex = {
'f' : 0,
'p' : 1,
'ym' : 2,
'mm' : 3,
'ds' : 4,
'hh' : 5,
'cr' : 6,
'tbc' : 7,
'bf' : 8,
'b' : 9,
'dt' : 10,
'ac' : 11,
'bs' : 12,
'sd' : 13,
'le' : 14,
'bw' : 15,
'sc' : 16,
'pp' : 17,
'tw' : 18,
'bc' : 19,
'nc' : 20,
'mb' : 21,
'ls' : 22,
'rb' : 23,
'cc' : 24,
'tm' : 25,
'nd' : 26,
'gh' : 27,
'ms' : 28,
'tf' : 29,
'm' : 30,
'mh' : 31
}
BossCogRollSpeed = 7.5
BossCogTurnSpeed = 20
BossCogTreadSpeed = 3.5
BossCogDizzy = 0
BossCogElectricFence = 1
BossCogSwatLeft = 2
BossCogSwatRight = 3
BossCogAreaAttack = 4
BossCogFrontAttack = 5
BossCogRecoverDizzyAttack = 6
BossCogDirectedAttack = 7
BossCogStrafeAttack = 8
BossCogNoAttack = 9
BossCogGoonZap = 10
BossCogSlowDirectedAttack = 11
BossCogDizzyNow = 12
BossCogGavelStomp = 13
BossCogGavelHandle = 14
BossCogLawyerAttack = 15
BossCogMoveAttack = 16
BossCogGolfAttack = 17
BossCogGolfAreaAttack = 18
BossCogGearDirectedAttack = 19
BossCogOvertimeAttack = 20
BossCogAttackTimes = {BossCogElectricFence: 0,
 BossCogSwatLeft: 5.5,
 BossCogSwatRight: 5.5,
 BossCogAreaAttack: 4.21,
 BossCogFrontAttack: 2.65,
 BossCogRecoverDizzyAttack: 5.1,
 BossCogDirectedAttack: 4.84,
 BossCogNoAttack: 6,
 BossCogSlowDirectedAttack: 7.84,
 BossCogMoveAttack: 3,
 BossCogGolfAttack: 6,
 BossCogGolfAreaAttack: 7,
 BossCogGearDirectedAttack: 4.84,
 BossCogOvertimeAttack: 5}
BossCogDamageLevels = {BossCogElectricFence: 1,
 BossCogSwatLeft: 5,
 BossCogSwatRight: 5,
 BossCogAreaAttack: 10,
 BossCogFrontAttack: 3,
 BossCogRecoverDizzyAttack: 3,
 BossCogDirectedAttack: 3,
 BossCogStrafeAttack: 2,
 BossCogGoonZap: 5,
 BossCogSlowDirectedAttack: 10,
 BossCogGavelStomp: 20,
 BossCogGavelHandle: 2,
 BossCogLawyerAttack: 5,
 BossCogMoveAttack: 20,
 BossCogGolfAttack: 15,
 BossCogGolfAreaAttack: 15,
 BossCogGearDirectedAttack: 15,
 BossCogOvertimeAttack: 10}
BossCogBattleAPosHpr = (0,
 -25,
 0,
 0,
 0,
 0)
BossCogBattleBPosHpr = (0,
 25,
 0,
 180,
 0,
 0)
SellbotBossMaxDamage = 100
SellbotBossMaxDamageNerfed = 100
SellbotBossBattleOnePosHpr = (0,
 -35,
 0,
 -90,
 0,
 0)
SellbotBossBattleTwoPosHpr = (0,
 60,
 18,
 -90,
 0,
 0)
SellbotBossBattleThreeHpr = (180, 0, 0)
SellbotBossBottomPos = (0, -110, -6.5)
SellbotBossDeathPos = (0, -175, -6.5)
SellbotBossDooberTurnPosA = (-20, -50, 0)
SellbotBossDooberTurnPosB = (20, -50, 0)
SellbotBossDooberTurnPosDown = (0, -50, 0)
SellbotBossDooberFlyPos = (0, -135, -6.5)
SellbotBossTopRampPosA = (-80, -35, 18)
SellbotBossTopRampTurnPosA = (-80, 10, 18)
SellbotBossP3PosA = (-50, 40, 18)
SellbotBossTopRampPosB = (80, -35, 18)
SellbotBossTopRampTurnPosB = (80, 10, 18)
SellbotBossP3PosB = (50, 60, 18)
CashbotBossMaxDamage = 500
CashbotBossOffstagePosHpr = (120,
 -195,
 0,
 0,
 0,
 0)
CashbotBossBattleOnePosHpr = (120,
 -230,
 0,
 90,
 0,
 0)
CashbotRTBattleOneStartPosHpr = (94,
 -220,
 0,
 110,
 0,
 0)
CashbotBossBattleThreePosHpr = (120,
 -315,
 0,
 180,
 0,
 0)
CashbotToonsBattleThreeStartPosHpr = [(105,
  -285,
  0,
  208,
  0,
  0),
 (136,
  -342,
  0,
  398,
  0,
  0),
 (105,
  -342,
  0,
  333,
  0,
  0),
 (135,
  -292,
  0,
  146,
  0,
  0),
 (93,
  -303,
  0,
  242,
  0,
  0),
 (144,
  -327,
  0,
  64,
  0,
  0),
 (145,
  -302,
  0,
  117,
  0,
  0),
 (93,
  -327,
  0,
  -65,
  0,
  0)]
CashbotBossSafePosHprs = [(120,
  -315,
  30,
  0,
  0,
  0),
 (77.2,
  -329.3,
  0,
  -90,
  0,
  0),
 (77.1,
  -302.7,
  0,
  -90,
  0,
  0),
 (165.7,
  -326.4,
  0,
  90,
  0,
  0),
 (165.5,
  -302.4,
  0,
  90,
  0,
  0),
 (107.8,
  -359.1,
  0,
  0,
  0,
  0),
 (133.9,
  -359.1,
  0,
  0,
  0,
  0),
 (107.0,
  -274.7,
  0,
  180,
  0,
  0),
 (134.2,
  -274.7,
  0,
  180,
  0,
  0)]
CashbotBossCranePosHprs = [(97.4,
  -337.6,
  0,
  -45,
  0,
  0),
 (97.4,
  -292.4,
  0,
  -135,
  0,
  0),
 (142.6,
  -292.4,
  0,
  135,
  0,
  0),
 (142.6,
  -337.6,
  0,
  45,
  0,
  0)]
CashbotBossToMagnetTime = 0.2
CashbotBossFromMagnetTime = 1
CashbotBossSafeKnockImpact = 0.5
CashbotBossSafeNewImpact = 0.0
CashbotBossGoonImpact = 0.1
CashbotBossKnockoutDamage = 15
TTWakeWaterHeight = -4.79
DDWakeWaterHeight = 1.669
EstateWakeWaterHeight = -.3
OZWakeWaterHeight = -0.5
WakeRunDelta = 0.1
WakeWalkDelta = 0.2
NoItems = 0
NewItems = 1
OldItems = 2
SuitInvasionBegin = 0
SuitInvasionEnd = 1
SuitInvasionUpdate = 2
SuitInvasionBulletin = 3
SkelecogInvasionBegin = 4
SkelecogInvasionEnd = 5
SkelecogInvasionBulletin = 6
WaiterInvasionBegin = 7
WaiterInvasionEnd = 8
WaiterInvasionBulletin = 9
V2InvasionBegin = 10
V2InvasionEnd = 11
V2InvasionBulletin = 12

TOT_REWARD_JELLYBEAN_AMOUNT = 100
TOT_REWARD_END_OFFSET_AMOUNT = 0
LawbotBossMaxDamage = 2700
LawbotBossWinningTilt = 40
LawbotBossInitialDamage = 1350
LawbotBossBattleOnePosHpr = (-2.798,
 -60,
 0,
 0,
 0,
 0)
LawbotBossBattleTwoPosHpr = (-2.798,
 89,
 19.145,
 0,
 0,
 0)
LawbotBossTopRampPosA = (-80, -35, 18)
LawbotBossTopRampTurnPosA = (-80, 10, 18)
LawbotBossP3PosA = (55, -9, 0)
LawbotBossTopRampPosB = (80, -35, 18)
LawbotBossTopRampTurnPosB = (80, 10, 18)
LawbotBossP3PosB = (55, -9, 0)
LawbotBossBattleThreePosHpr = LawbotBossBattleTwoPosHpr
LawbotBossBottomPos = (50, 39, 0)
LawbotBossDeathPos = (50, 40, 0)
LawbotBossGavelPosHprs = [(35,
  78.328,
  0,
  -135,
  0,
  0),
 (68.5,
  78.328,
  0,
  135,
  0,
  0),
 (47,
  -33,
  0,
  45,
  0,
  0),
 (-50,
  -39,
  0,
  -45,
  0,
  0),
 (-9,
  -37,
  0,
  0,
  0,
  0),
 (-9,
  49,
  0,
  -180,
  0,
  0),
 (32,
  0,
  0,
  45,
  0,
  0),
 (33,
  56,
  0,
  135,
  0,
  0)]
LawbotBossGavelTimes = [(0.2, 0.9, 0.6),
 (0.25, 1, 0.5),
 (1.0, 6, 0.5),
 (0.3, 3, 1),
 (0.26, 0.9, 0.45),
 (0.24, 1.1, 0.65),
 (0.27, 1.2, 0.45),
 (0.25, 0.95, 0.5)]
LawbotBossGavelHeadings = [(0,
  -15,
  4,
  -70 - 45,
  5,
  45),
 (0,
  -45,
  -4,
  -35,
  -45,
  -16,
  32),
 (0,
  -8,
  19,
  -7,
  5,
  23),
 (0,
  -4,
  8,
  -16,
  32,
  -45,
  7,
  7,
  -30,
  19,
  -13,
  25),
 (0,
  -45,
  -90,
  45,
  90),
 (0,
  -45,
  -90,
  45,
  90),
 (0, -45, 45),
 (0, -45, 45)]
LawbotBossCogRelBattleAPosHpr = (-25,
 -10,
 0,
 0,
 0,
 0)
LawbotBossCogRelBattleBPosHpr = (-25,
 10,
 0,
 0,
 0,
 0)
LawbotBossCogAbsBattleAPosHpr = (-5,
 -2,
 0,
 0,
 0,
 0)
LawbotBossCogAbsBattleBPosHpr = (-5,
 0,
 0,
 0,
 0,
 0)
LawbotBossWitnessStandPosHpr = (54,
 100,
 0,
 -90,
 0,
 0)
LawbotBossInjusticePosHpr = (-3,
 12,
 0,
 90,
 0,
 0)
LawbotBossInjusticeScale = (1.75, 1.75, 1.5)
LawbotBossDefensePanDamage = 1
LawbotBossLawyerPosHprs = [(-57,
  -24,
  0,
  -90,
  0,
  0),
 (-57,
  -12,
  0,
  -90,
  0,
  0),
 (-57,
  0,
  0,
  -90,
  0,
  0),
 (-57,
  12,
  0,
  -90,
  0,
  0),
 (-57,
  24,
  0,
  -90,
  0,
  0),
 (-57,
  36,
  0,
  -90,
  0,
  0),
 (-57,
  48,
  0,
  -90,
  0,
  0),
 (-57,
  60,
  0,
  -90,
  0,
  0),
 (-3,
  -37.3,
  0,
  0,
  0,
  0),
 (-3,
  53,
  0,
  -180,
  0,
  0)]
LawbotBossLawyerCycleTime = 6
LawbotBossLawyerToPanTime = 2.5
LawbotBossLawyerChanceToAttack = 50
LawbotBossLawyerHeal = 2
LawbotBossLawyerStunTime = 5
LawbotBossDifficultySettings = [(38,
  4,
  8,
  1,
  0,
  0),
 (36,
  5,
  8,
  1,
  0,
  0),
 (34,
  5,
  8,
  1,
  0,
  0),
 (32,
  6,
  8,
  2,
  0,
  0),
 (30,
  6,
  8,
  2,
  0,
  0),
 (28,
  7,
  8,
  3,
  0,
  0),
 (26,
  7,
  9,
  3,
  1,
  1),
 (24,
  8,
  9,
  4,
  1,
  1),
 (22,
  8,
  10,
  4,
  1,
  0)]
LawbotBossCannonPosHprs = [(-40,
  -12,
  0,
  -90,
  0,
  0),
 (-40,
  0,
  0,
  -90,
  0,
  0),
 (-40,
  12,
  0,
  -90,
  0,
  0),
 (-40,
  24,
  0,
  -90,
  0,
  0),
 (-40,
  36,
  0,
  -90,
  0,
  0),
 (-40,
  48,
  0,
  -90,
  0,
  0),
 (-40,
  60,
  0,
  -90,
  0,
  0),
 (-40,
  72,
  0,
  -90,
  0,
  0)]
LawbotBossCannonPosA = (-80, -51.48, 0)
LawbotBossCannonPosB = (-80, 70.73, 0)
LawbotBossChairPosHprs = [(60,
  72,
  0,
  -90,
  0,
  0),
 (60,
  62,
  0,
  -90,
  0,
  0),
 (60,
  52,
  0,
  -90,
  0,
  0),
 (60,
  42,
  0,
  -90,
  0,
  0),
 (60,
  32,
  0,
  -90,
  0,
  0),
 (60,
  22,
  0,
  -90,
  0,
  0),
 (70,
  72,
  5,
  -90,
  0,
  0),
 (70,
  62,
  5,
  -90,
  0,
  0),
 (70,
  52,
  5,
  -90,
  0,
  0),
 (70,
  42,
  5,
  -90,
  0,
  0),
 (70,
  32,
  5,
  -90,
  0,
  0),
 (70,
  22,
  5,
  -90,
  0,
  0)]
LawbotBossChairRow1PosB = (59.3, 48, 14.05)
LawbotBossChairRow1PosA = (59.3, -18.2, 14.05)
LawbotBossChairRow2PosB = (75.1, 48, 28.2)
LawbotBossChairRow2PosA = (75.1, -18.2, 28.2)
LawbotBossCannonBallMax = 12
LawbotBossJuryBoxStartPos = (94, -8, 5)
LawbotBossJuryBoxRelativeEndPos = (30, 0, 12.645)
LawbotBossJuryBoxMoveTime = 70
LawbotBossJurorsForBalancedScale = 8
LawbotBossDamagePerJuror = 68
LawbotBossCogJurorFlightTime = 10
LawbotBossCogJurorDistance = 75
LawbotBossBaseJurorNpcId = 2001
LawbotBossWitnessEpiloguePosHpr = (-3,
 0,
 0,
 180,
 0,
 0)
LawbotBossChanceForTaunt = 25
LawbotBossBonusWaitTime = 60
LawbotBossBonusDuration = 20
LawbotBossBonusToonup = 10
LawbotBossBonusWeightMultiplier = 2
LawbotBossChanceToDoAreaAttack = 11
LOW_POP_JP = 0
MID_POP_JP = 100
HIGH_POP_JP = 200
LOW_POP_INTL = 399
MID_POP_INTL = 499
HIGH_POP_INTL = -1
LOW_POP = 100
MID_POP = 200
HIGH_POP = -1
PinballCannonBumper = 0
PinballCloudBumperLow = 1
PinballCloudBumperMed = 2
PinballCloudBumperHigh = 3
PinballTarget = 4
PinballRoof = 5
PinballHouse = 6
PinballFence = 7
PinballBridge = 8
PinballStatuary = 9
PinballScoring = [(100, 1),
 (150, 1),
 (200, 1),
 (250, 1),
 (350, 1),
 (100, 1),
 (50, 1),
 (25, 1),
 (100, 1),
 (10, 1)]
PinballCannonBumperInitialPos = (0, -20, 40)
RentalCop = 0
RentalCannon = 1
RentalGameTable = 2
GlitchKillerZones = [13300,
 13400,
 13500,
 13600]
ColorPlayer = (0.3,
 0.7,
 0.3,
 1)
ColorAvatar = (0.3,
 0.3,
 0.7,
 1)
ColorPet = (0.6,
 0.4,
 0.2,
 1)
ColorFreeChat = (0.3,
 0.3,
 0.8,
 1)
ColorSpeedChat = (0.2,
 0.6,
 0.4,
 1)
ColorNoChat = (0.8,
 0.5,
 0.1,
 1)
FactoryLaffMinimums = [(0, 31),
 (0, 66, 71),
 (0,
  81,
  86,
  96),
 (0, 101, 106)]
PICNIC_COUNTDOWN_TIME = 60
BossbotRTIntroStartPosHpr = (0,
 -64,
 0,
 180,
 0,
 0)
BossbotRTPreTwoPosHpr = (0,
 -20,
 0,
 180,
 0,
 0)
BossbotRTEpiloguePosHpr = (0,
 90,
 0,
 180,
 0,
 0)
BossbotBossBattleOnePosHpr = (0,
 355,
 0,
 0,
 0,
 0)
BossbotBossPreTwoPosHpr = (0,
 20,
 0,
 0,
 0,
 0)
BossbotElevCamPosHpr = (0,
 -100.544,
 7.18258,
 0,
 0,
 0)
BossbotFoodModelScale = 0.75
BossbotNumFoodToExplode = 3
BossbotBossServingDuration = 300
BossbotPrepareBattleThreeDuration = 20
WaiterBattleAPosHpr = (20,
 -400,
 0,
 0,
 0,
 0)
WaiterBattleBPosHpr = (-20,
 -400,
 0,
 0,
 0,
 0)
BossbotBossBattleThreePosHpr = (0,
 355,
 0,
 0,
 0,
 0)
DinerBattleAPosHpr = (20,
 -240,
 0,
 0,
 0,
 0)
DinerBattleBPosHpr = (-20,
 -240,
 0,
 0,
 0,
 0)
BossbotBossMaxDamage = 500
BossbotMaxSpeedDamage = 90
BossbotSpeedRecoverRate = 20
BossbotBossDifficultySettings = [(8,
  4,
  11,
  3,
  30,
  25),
 (9,
  5,
  12,
  6,
  28,
  26),
 (10,
  6,
  11,
  7,
  26,
  27),
 (8,
  8,
  12,
  8,
  24,
  28),
 (13,
  5,
  12,
  9,
  22,
  29)]
BossbotRollSpeedMax = 22
BossbotRollSpeedMin = 7.5
BossbotTurnSpeedMax = 60
BossbotTurnSpeedMin = 20
BossbotTreadSpeedMax = 10.5
BossbotTreadSpeedMin = 3.5
CalendarFilterShowAll = 0
CalendarFilterShowOnlyHolidays = 1
CalendarFilterShowOnlyParties = 2
TTC = 1
DD = 2
MM = 3
GS = 4
DG = 5
BR = 6
OZ = 7
DL = 8
DefaultWantNewsPageSetting = 0
gmMagicWordList = ['restock',
 'restockUber',
 'autoRestock',
 'resistanceRestock',
 'restockSummons',
 'uberDrop',
 'rich',
 'maxBankMoney',
 'toonUp',
 'rod',
 'cogPageFull',
 'pinkSlips',
 'Tickets',
 'newSummons',
 'who',
 'who all']
NewsPageScaleAdjust = 0.85
AnimPropTypes = Enum(('Unknown',
 'Hydrant',
 'Mailbox',
 'Trashcan'), start=-1)
EmblemTypes = Enum(('Silver', 'Gold'))
NumEmblemTypes = 2
MaxBankMoney = 15000
DefaultBankItemId = 1350
ToonAnimStates = set(['off',
 'neutral',
 'victory',
 'Happy',
 'Sad',
 'Catching',
 'CatchEating',
 'Sleep',
 'walk',
 'jumpSquat',
 'jump',
 'jumpAirborne',
 'jumpLand',
 'run',
 'swim',
 'swimhold',
 'dive',
 'cringe',
 'OpenBook',
 'ReadBook',
 'CloseBook',
 'TeleportOut',
 'Died',
 'TeleportedOut',
 'TeleportIn',
 'Emote',
 'SitStart',
 'Sit',
 'Push',
 'Squish',
 'FallDown',
 'GolfPuttLoop',
 'GolfRotateLeft',
 'GolfRotateRight',
 'GolfPuttSwing',
 'GolfGoodPutt',
 'GolfBadPutt',
 'Flattened',
 'CogThiefRunning',
 'ScientistJealous',
 'ScientistEmcee',
 'ScientistWork',
 'ScientistLessWork',
 'ScientistPlay'])
AV_FLAG_REASON_TOUCH = 1
AV_FLAG_HISTORY_LEN = 500
AV_TOUCH_CHECK_DELAY_AI = 3.0
AV_TOUCH_CHECK_DELAY_CL = 1.0
AV_TOUCH_CHECK_DIST = 2.0
AV_TOUCH_CHECK_DIST_Z = 5.0
AV_TOUCH_CHECK_TIMELIMIT_CL = 0.002
AV_TOUCH_COUNT_LIMIT = 5
AV_TOUCH_COUNT_TIME = 300

CommonDisplayResolutions = {
    (25, 16): ((1600, 1024),),
    (931, 524): ((1862, 1048),),
    (1707, 1067): ((1707, 1067),),
    (707, 397): ((1414, 794),),
    (16, 9): ((1280, 720), (1440, 810), (1536, 864), (1600, 900), (1680, 945),
              (1824, 1026), (1920, 1080), (2048, 1152), (2560, 1440),
              (3200, 1800), (3840, 2160)),
    (3, 2): ((1440, 960),),
    (569, 320): ((1707, 960),),
    (902, 507): ((1804, 1014),),
    (8, 5): ((1120, 700), (1152, 720), (1280, 800), (1344, 840), (1440, 900),
             (1536, 960), (1680, 1050), (1920, 1200), (2560, 1600),
             (2880, 1800)),
    (307, 171): ((1842, 1026),),
    (85, 64): ((1360, 1024),),
    (64, 27): ((2560, 1080),),
    (16, 3): ((5760, 1080),),
    (24, 5): ((5760, 1200),),
    (128, 75): ((1024, 600),),
    (222, 125): ((1776, 1000),),
    (5, 4): ((1280, 1024),),
    (147, 83): ((1176, 664),),
    (32, 15): ((1280, 600),),
    (1024, 819): ((1024, 819),),
    (43, 18): ((3440, 1440),),
    (5, 3): ((1280, 768),),
    (221, 124): ((1768, 992),),
    (1280, 853): ((1280, 853),),
    (921, 518): ((1842, 1036),),
    (683, 384): ((1366, 768),),
    (57, 32): ((1368, 768),),
    (85, 48): ((1360, 768),),
    (1067, 600): ((1067, 600),),
    (4, 3): ((800, 600), (1024, 768), (1152, 864), (1280, 960), (1400, 1050),
             (1600, 1200)),
}
