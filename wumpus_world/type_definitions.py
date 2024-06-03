import enum

class ActionType(enum.Enum):
    move_forward = 1
    turn_left = 2
    turn_right = 3
    grab = 4
    shoot = 5
    climb = 6

class DirectionType(enum.Enum):
    #상하좌우순
    north = 1
    south = 2
    west = 3
    east = 4

class StateType(enum.Enum):
    #unknown = 1#미개척지
    ground = 2#안전한 땅
    wall = 3#벽
    gold = 4#금
    wumpus = 5#괴물
    pit = 6#구덩이

class PerceptType(enum.Enum):
    stench = 11#Wumpus가 인접한 캉에 있을 때 느껴지는 악취
    breeze = 12#구덩이가 인접한 칸에 있을 때 느껴지는 바람
    glitter = 13#금이 있는 칸에 있을 때 느껴지는 반짝임
    bump = 14#벽에 닿을 경우 느껴지는 충돌감
    scream = 15#Wumpus가 죽을 때 내는 소리