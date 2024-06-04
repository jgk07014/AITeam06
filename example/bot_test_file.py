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
        'total_action_count': 0
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

def test_q_learing_bot():
    wumpus_world = World(WorldConfig.COL, WorldConfig.ROW, WorldConfig.START_POINT, WorldConfig.INIT_DIRECTION,
                         WorldConfig.ARROW_COUNT, WorldConfig.WUMPUS_COUNT, WorldConfig.PIT_COUNT,
                         WorldConfig.GOLD_COUNT)
    wumpus_world.initialize()
    q_agent = agents.QLearingAgent()

    # 에이전트 학습
    episodes = 10000 # 총 학습 횟수
    for episode in range(episodes):
        wumpus_world.reset()
        total_reward = 0
        state = q_agent.get_state(wumpus_world)

        while not wumpus_world.is_over():
            action = q_agent.select_action(wumpus_world)
            next_world, reward = q_agent.reward_policy(wumpus_world, action)
            next_state = q_agent.get_state(next_world)
            q_agent.learn(state, action, reward, next_state)
            state = next_state
            total_reward += reward
            wumpus_world.apply_action(action)

        if episode % 1000 == 0:
            print(f"Episode {episode}: Total Reward: {total_reward}")

    # 에이전트 실습
    wumpus_world.reset()
    analysis_data = {
        'total_action_count': 0
    }

    while not wumpus_world.is_over():
        time.sleep(DELAY_TIME)
        print(chr(27) + "[2J")#화면 초기화

        print_board(wumpus_world)
        action_type = q_agent.select_action(wumpus_world)

        analysis_data['total_action_count'] += 1
        print_action(action_type, analysis_data)
        wumpus_world.apply_action(action_type)

    print_result(wumpus_world, analysis_data)

if __name__ == '__main__':
    #test_random_bot()
    test_q_learing_bot()