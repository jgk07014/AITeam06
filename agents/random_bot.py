import random
from agents.base import Agent
from wumpus_world.world_manager import Actions
from wumpus_world.type_definitions import ActionType

class RandomBot(Agent):
    def select_action(self, world):
        candidates = []

        if world.is_valid_action(ActionType.move_forward):
            candidates.append(ActionType.move_forward)
        if world.is_valid_action(ActionType.turn_left):
            candidates.append(ActionType.turn_left)
        if world.is_valid_action(ActionType.turn_right):
            candidates.append(ActionType.turn_right)
        if world.is_valid_action(ActionType.grab):
            candidates.append(ActionType.grab)
        if world.is_valid_action(ActionType.shoot):
            candidates.append(ActionType.shoot)
        if world.is_valid_action(ActionType.climb):
            candidates.append(ActionType.climb)

        return random.choice(candidates)