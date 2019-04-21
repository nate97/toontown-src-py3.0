from toontown.toonbase.ToontownGlobals import *

# [Holiday ID, Weekday]
DEFAULT_WEEKLY_HOLIDAYS = [
    [FISH_BINGO_NIGHT, 2],  # Wednesday
    [TROLLEY_HOLIDAY, 3],  # Thursday
    [SILLY_SATURDAY_BINGO, 5],  # Saturday
]


# [Holiday ID, START [Month, Day, Hour, Minute], END [Month, Day, Hour, Minute]]
DEFAULT_YEARLY_HOLIDAYS = [
    [TOP_TOONS_MARATHON, [1, 1, 12, 0], [1, 2, 0, 0]],
    [VALENTINES_DAY, [2, 8, 12, 0], [2, 24, 0, 0]],
    [IDES_OF_MARCH, [3, 14, 12, 0], [3, 16, 0, 0]],
    [APRIL_FOOLS_COSTUMES, [4, 1, 0, 0], [4, 8, 0, 0]],
    [JULY4_FIREWORKS, [6, 29, 12, 0], [7, 17, 0, 0]],


    [HALLOWEEN_COSTUMES, [10, 21, 12, 0], [11, 1, 0, 0]],

    [HALLOWEEN_PROPS, [10, 21, 12, 0], [11, 1, 0, 0]],
    [TRICK_OR_TREAT, [10, 21, 12, 0], [11, 1, 0, 0]],
    [HALLOWEEN, [10, 31, 12, 0], [11, 1, 0, 0]],

    [WINTER_DECORATIONS, [12, 14, 12, 0], [1, 4, 0, 0]],
    [WINTER_CAROLING, [12, 14, 12, 0], [1, 4, 0, 0]],
]

HOLIDAY_SHOPKEEPER_ZONES = {
    TRICK_OR_TREAT: {
        ToontownCentral: 2649,
        DonaldsDock: 1834,
        DaisyGardens: 5620,
        MinniesMelodyland: 4835,
        TheBrrrgh: 3707,
        DonaldsDreamland: 9619,
    },
    WINTER_CAROLING: {
        ToontownCentral: 2659,
        DonaldsDock: 1707,
        DaisyGardens: 5626,
        MinniesMelodyland: 4614,
        TheBrrrgh: 3828,
        DonaldsDreamland: 9720
    },
    IDES_OF_MARCH: {
        DaisyGardens: 5819
    }
}
