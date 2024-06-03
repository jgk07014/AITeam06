import agents, time
from wumpus_world.world_manager import World
from wumpus_world.config import WorldConfig
from example.utils_printing import print_board, print_action, print_result
from wumpus_world.type_definitions import ActionType

DELAY_TIME = 0 # 초단위, 출력 지연 시간 설정

def simulation():
    wumpus_world = World(WorldConfig.COL, WorldConfig.ROW, WorldConfig.START_POINT, WorldConfig.INIT_DIRECTION,
                         WorldConfig.ARROW_COUNT, WorldConfig.WUMPUS_COUNT, WorldConfig.PIT_COUNT, WorldConfig.GOLD_COUNT)
    wumpus_world.initialize()

    analysis_data = {
        'total_action_count'  : 0
    }

    while not wumpus_world.is_over():
        time.sleep(DELAY_TIME)
        print(chr(27) + "[2J")#화면 초기화

        print_board(wumpus_world)
        action_type = select_action(wumpus_world)

        analysis_data['total_action_count'] += 1
        print_action(action_type, analysis_data)
        wumpus_world.apply_action(action_type)

    print_result(wumpus_world, analysis_data)

def select_action(world):
    action_type = None
    print("<<행동 선택(숫자 입력)>>")
    while action_type is None:
        print("1. 직진")
        print("2. 좌회전")
        print("3. 우회진")
        print("4. 줍기")
        print("5. 활 쏘기")
        print("6. 등반하기")
        input_data = int(input("입력:"))
        if input_data == 1 and world.is_valid_action(ActionType.move_forward):
            action_type = ActionType.move_forward
        elif input_data == 2 and world.is_valid_action(ActionType.turn_left):
            action_type = ActionType.turn_left
        elif input_data == 3 and world.is_valid_action(ActionType.turn_right):
            action_type = ActionType.turn_right
        elif input_data == 4 and world.is_valid_action(ActionType.grab):
            action_type = ActionType.grab
        elif input_data == 5 and world.is_valid_action(ActionType.shoot):
            action_type = ActionType.shoot
        elif input_data == 6 and world.is_valid_action(ActionType.climb):
            action_type = ActionType.climb
        else:
            print("불가능한 행동입니다. 다시 입력해주세요.")

    return action_type

if __name__ == '__main__':
    simulation()