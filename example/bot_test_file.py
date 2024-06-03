import agents, time
from wumpus_world.world_manager import World
from wumpus_world.config import WorldConfig
from example.utils_printing import print_board, print_action, print_result
from wumpus_world.type_definitions import ActionType

DELAY_TIME = 1 # 초단위, 출력 지연 시간 설정

def test_random_bot():
    wumpus_world = World(WorldConfig.COL, WorldConfig.ROW, WorldConfig.START_POINT, WorldConfig.INIT_DIRECTION,
                         WorldConfig.ARROW_COUNT, WorldConfig.WUMPUS_COUNT, WorldConfig.PIT_COUNT, WorldConfig.GOLD_COUNT)
    wumpus_world.initialize()
    random_bot = agents.RandomBot()
    analysis_data = {
        'total_action_count'  : 0
    }

    while not wumpus_world.is_over():
        time.sleep(DELAY_TIME)
        print(chr(27) + "[2J")#화면 초기화

        print_board(wumpus_world)
        action_type = random_bot.select_action(wumpus_world)

        analysis_data['total_action_count'] += 1
        print_action(action_type, analysis_data)
        wumpus_world.apply_action(action_type)

    print_result(wumpus_world, analysis_data)

if __name__ == '__main__':
    test_random_bot()