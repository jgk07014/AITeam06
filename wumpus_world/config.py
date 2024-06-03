from wumpus_world.type_definitions import DirectionType

class WorldConfig():
    def __init__(self):
        pass

    ROW = 6
    COL = 6
    START_POINT = (1, 1)
    INIT_DIRECTION = DirectionType.east
    ARROW_COUNT = 3
    WUMPUS_COUNT = 1
    PIT_COUNT = 2
    GOLD_COUNT = 1
