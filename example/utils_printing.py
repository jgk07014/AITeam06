from wumpus_world.utils import Point
from wumpus_world.type_definitions import StateType, ActionType, DirectionType

STATE_TO_CHAR = {
    #StateType.unknown   : '땅',
    StateType.ground    : '땅',
    StateType.wall      : '벽',
    StateType.gold      : '금',
    StateType.wumpus    : '괴',
    StateType.pit       : '웅'
}

DIRECTION_TO_CHAR = {
    DirectionType.north : '↑',
    DirectionType.south : '↓',
    DirectionType.west  : '←',
    DirectionType.east  : '→'
}

ACTION_TO_CHAR = {
    ActionType.move_forward : '직진',
    ActionType.turn_right   : '오른쪽으로 방향 전환',
    ActionType.turn_left    : '왼쪽으로 방향 전환',
    ActionType.grab         : '그랩',
    ActionType.shoot        : '활 쏘기',
    ActionType.climb        : '등반'
}

def print_board(world):
    print('   ', end='')
    for i in range(0, world.rows, 1):
        print(str(i) + ' ', end='')
    print('')
    for row in range(0, world.rows, 1):
        line = []
        for col in range(0, world.cols, 1):
            curr_point = Point(row=row, col=col)
            state = world.get_state_type_on_point(curr_point)
            if curr_point == world.action.point:
                line.append(DIRECTION_TO_CHAR[world.action.direction])
            else:
                line.append(STATE_TO_CHAR[state])
        print('%2d %s' % (row, ''.join(line)))

def print_action(action_type, analysis_data):
    total_action_count = analysis_data['total_action_count']

    message = None
    if action_type == ActionType.move_forward:
        message = ACTION_TO_CHAR[ActionType.move_forward]
    elif action_type == ActionType.turn_right:
        message = ACTION_TO_CHAR[ActionType.turn_right]
    elif action_type == ActionType.turn_left:
        message = ACTION_TO_CHAR[ActionType.turn_left]
    elif action_type == ActionType.grab:
        message = ACTION_TO_CHAR[ActionType.grab]
    elif action_type == ActionType.shoot:
        message = ACTION_TO_CHAR[ActionType.shoot]
    elif action_type == ActionType.climb:
        message = ACTION_TO_CHAR[ActionType.climb]
    else:
        raise ValueError("undefined value of action type")
    print("%d번째 행동 : %s" %(total_action_count, message))

def print_result(world, analysis_data):
    total_action_count = analysis_data['total_action_count']

    print("==========<게임 종료>==========")
    if world.is_mission_completed():
        print("승리!!!")
    else:
        print("패배...")
    print("총 행동 횟수 : " + str(total_action_count))