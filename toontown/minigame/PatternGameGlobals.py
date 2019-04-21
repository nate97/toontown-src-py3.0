import MinigameGlobals


if config.GetBool('want-long-pattern-game', False):
    INITIAL_ROUND_LENGTH = 1
    ROUND_LENGTH_INCREMENT = 1
    NUM_ROUNDS = 100
    InputTime = 120
else:
    INITIAL_ROUND_LENGTH = 2
    ROUND_LENGTH_INCREMENT = 2
    NUM_ROUNDS = 4
    InputTime = 10

TOONTOWN_WORK = 1
ClientsReadyTimeout = 5 + MinigameGlobals.latencyTolerance
InputTimeout = InputTime + MinigameGlobals.latencyTolerance
