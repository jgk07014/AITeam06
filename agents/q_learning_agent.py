import copy, random
import numpy as np
from collections import defaultdict, namedtuple
from agents.random_bot import RandomBot
from wumpus_world.type_definitions import ActionType

class QLearingAgent(RandomBot):
    def __init__(self, learning_rate=0.1, discount_factor=0.99, epsilon=0.1):
        self.q_table = defaultdict(lambda: np.zeros(len(ActionType)))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.actions = list(ActionType)
        self.random_bot = RandomBot()

    def select_action(self, world):
        action_type = None
        state = self.get_state(world)

        if np.random.rand() < self.epsilon:
            action_type = self.random_bot.select_action(world)
        else:
            state_action = self.q_table[state]
            action_type = self.actions[np.argmax(state_action)]

            if not world.is_valid_action(action_type):
                action_type = self.random_bot.select_action(world)
        return action_type

    def learn(self, state, action, reward, next_state):
        action_index = self.actions.index(action)
        predict = self.q_table[state][action_index]
        if next_state is not None:
            target = reward + self.discount_factor * np.max(self.q_table[next_state])
        else:
            target = reward
        self.q_table[state][action_index] += self.learning_rate * (target - predict)

    def get_state(self, world):
        # (현재 좌표, 현재 방향, 현재 보유 화살 개수, 현재 금 보유 여부)을 상태공간으로 정의
        return (world.action.point.row, world.action.point.col, world.action.direction, world.arrow_count, world.is_collected_gold)

    def reward_policy(self, world, action_type):
        reward = -1 # 기본적으로 어떤 행동을 수행할 때는 감점을 시킴(행동을 최소화하기 위한 정책)
        next_world = copy.deepcopy(world)
        next_world.apply_action(action_type)

        if action_type == ActionType.grab:
            # 그랩 행동에 대한 보상 정책은 단순 감점
            reward += -10

        elif action_type == ActionType.shoot:
            # 화살쏘기 행동에 대한 보상 정책은 단순 감점
            reward += -10

        elif action_type == ActionType.climb:
            # 등반 행동에 대한 보상 정책은 단순 감점
            reward += -10

        if next_world.is_over():
            # 게임이 끝났을 경우 미션을 완료하였으면 최고의 점수 아니면 최악의 점수를 부여
            if next_world.is_mission_completed():
                reward += 100000000
            else:
                reward += -100000000

        return next_world, reward