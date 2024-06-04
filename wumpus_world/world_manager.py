import random, copy
from wumpus_world.type_definitions import ActionType, DirectionType, StateType, PerceptType
from wumpus_world.utils import Point

class Actions():
    def __init__(self, point=None, direction=None):
       self.point = point
       self.direction = direction

    @classmethod
    def move_forward(cls, action):
        point = action.point
        direction = action.direction
        new_point = None
        if direction == DirectionType.north:
            new_point = point.move_north()
        elif direction == DirectionType.south:
            new_point = point.move_south()
        elif direction == DirectionType.west:
            new_point = point.move_west()
        elif direction == DirectionType.east:
            new_point = point.move_east()
        else:
            assert False, "invalid argument"
        return Actions(new_point, direction)

    @classmethod
    def turn_left(cls, action):
        point = action.point
        direction = action.direction
        new_direction = None
        if direction == DirectionType.north:
            new_direction = DirectionType.west
        elif direction == DirectionType.west:
            new_direction = DirectionType.south
        elif direction == DirectionType.south:
            new_direction = DirectionType.east
        elif direction == DirectionType.east:
            new_direction = DirectionType.north
        else:
            assert False, "invalid argument"
        return Actions(point, new_direction)

    @classmethod
    def turn_right(cls, action):
        point = action.point
        direction = action.direction
        new_direction = None
        if direction == DirectionType.north:
            new_direction = DirectionType.east
        elif direction == DirectionType.east:
            new_direction = DirectionType.south
        elif direction == DirectionType.south:
            new_direction = DirectionType.west
        elif direction == DirectionType.west:
            new_direction = DirectionType.north
        else:
            assert False, "invalid argument"
        return Actions(point, new_direction)

    @classmethod
    def shoot_arrow(cls, action):
        return action

    @classmethod
    def grab(cls, action):
        return action

    @classmethod
    def climb(cls, action):
        return action

class World():
    #초기설정
    def __init__(self, cols, rows, start_point, init_direction, arrow_count, wumpus_count, pit_count, gold_count):
        adj_start_point = Point(start_point[0], start_point[1])#tuple 이 아닌 namedtuple 을 사용
        self.cols = cols#grid 의 너비 설정
        self.rows = rows#grid 의 높이 설정
        self.start_point = adj_start_point#agent 출발 및 도착 지점 설정
        self.arrow_count = arrow_count#화살 개수 초기 설정 개수
        self.wumpus_count = wumpus_count#괴물의 개수 초기 설정 개수
        self.pit_count = pit_count#웅덩이의 개수 초기 설정 개수
        self.gold_count = gold_count#금의 개수 초기 설정 개수
        self.action = Actions(adj_start_point, init_direction)#초기 위치와 바라보고있는 방향 설정
        self.init_action = copy.deepcopy(self.action)#call by reference 가 아닌 call by value 를 활용해야하기 때문에 deepcopy 사용
        self.grid = None#맵
        self.init_grid = None#초기맵
        self.is_game_over = None#게임이 끝났는지 여부
        self.is_collected_gold = None#금 획득 여부

    def reset(self):
        # 상태 초기화
        self.is_game_over = False
        self.is_collected_gold = False
        self.action = copy.deepcopy(self.init_action)
        self.grid = copy.deepcopy(self.init_grid)

    def initialize(self):
        self.reset()

        # 그리드 초기화
        self.grid = [[StateType.ground] * self.cols for _ in range(self.rows)]

        # 모든 가장자리 좌표를 벽으로 설정
        for col in range(self.cols):
            self.grid[0][col] = StateType.wall
            self.grid[self.rows - 1][col] = StateType.wall
        for row in range(self.rows):
            self.grid[row][0] = StateType.wall
            self.grid[row][self.cols - 1] = StateType.wall

        # 시작 지점은 안전한 땅
        self.grid[self.start_point[0]][self.start_point[1]] = StateType.ground

        # 나머지 좌표 중에서 wumpus, pit, gold를 무작위로 배치
        for _ in range(self.wumpus_count):
            x, y = self.get_random_empty_location()
            self.grid[y][x] = StateType.wumpus

        for _ in range(self.pit_count):
            x, y = self.get_random_empty_location()
            self.grid[y][x] = StateType.pit

        for _ in range(self.gold_count):
            x, y = self.get_random_empty_location()
            self.grid[y][x] = StateType.gold

        # grid 백업
        self.init_grid = copy.deepcopy(self.grid)

    def get_random_empty_location(self):
        empty_locations = [(x, y) for y in range(0, self.rows) for x in range(0, self.cols)
                           if self.grid[y][x] == StateType.ground and (x, y) != self.start_point]
        if empty_locations:
            return random.choice(empty_locations)
        else:
            raise ValueError("not enough remain location")

    #해당 액션이 가능하다면 적용, 불가능하다면 에러 발생
    def apply_action(self, action_type):
        assert self.is_valid_action(action_type), "invalid action is " + str(action_type)
        new_action = None
        percept_list = set()

        if ActionType.move_forward == action_type:
            new_action = Actions.move_forward(self.action)
            #전진한 위치에 괴물(wumpus) 또는 구덩이(pit)가 존재할 경우 게임 종료
            if (StateType.wumpus == self.get_state_type_on_point(new_action.point)
                    or StateType.pit == self.get_state_type_on_point(new_action.point)):
                self.is_game_over = True
            percept_list.update(self.get_percept_type_list_on_point(new_action.point))
            #전진한 위치가 벽(wall)일 경우 전진한 행위 무효화
            if PerceptType.bump in percept_list:
                new_action = self.action
        elif ActionType.turn_left == action_type:
            new_action = Actions.turn_left(self.action)
        elif ActionType.turn_right == action_type:
            new_action = Actions.turn_right(self.action)
        elif ActionType.grab == action_type:
            new_action = Actions.grab(self.action)
            gold_point = new_action.point
            #현재 위치에 금이 존재할 경우 해당 지역에 금 제거 및 인벤토리에 금 추가
            if StateType.gold == self.get_state_type_on_point(gold_point):
                self.grid[gold_point.row][gold_point.col] = StateType.ground
                self.is_collected_gold = True
        elif ActionType.shoot == action_type:
            self.arrow_count -= 1
            new_action = Actions.shoot_arrow(self.action)
            arrow_point = Actions.move_forward(new_action).point
            #화살이 진행한 방향에 wumpus가 존재할 경우 wumpus 제거 및 scream 발생
            if self.is_valid_coordinate(arrow_point) and self.get_state_type_on_point(arrow_point) == StateType.wumpus:
                self.grid[arrow_point.row][arrow_point.col] = StateType.ground
                percept_list.add(PerceptType.scream)
        elif ActionType.climb == action_type:
            new_action = Actions.climb(self.action)
            #금을 확보했고 현재 위치가 시작지점일 경우 게임 종료[
            if self.is_collected_gold and new_action.point == self.start_point:
                self.is_game_over = True

        self.action = new_action

        return list(percept_list)

    def is_mission_completed(self):
        return self.is_game_over and self.is_collected_gold and self.action.point == self.start_point

    def is_valid_coordinate(self, point):
        if (0 <= point.col and point.col < self.cols) and (0 <= point.row and point.row < self.rows):
            return True
        else:
            return False

    #현재 상황에서 가능한 행동인지 확인해주는 메서드
    def is_valid_action(self, action_type):
        if self.is_game_over:
            return False

        result = None
        if ActionType.move_forward == action_type:
            new_action = Actions.move_forward(self.action)
            new_state = self.get_state_type_on_point(new_action.point)
            """ 버그 수정 : 직진의 가능 조건 수정
            #직진은 진행한 좌표에 벽이 없고 유효한 좌표일 때 가능한 행동이다.
            if new_state != StateType.wall and self.is_valid_coordinate(self.action.point):
                result = True
            else:
                result = False
            """
            #직진은 진행한 좌표가 유효한 좌표일 때 가능한 행동이다.
            if self.is_valid_coordinate(self.action.point):
                result = True
            else:
                result = False
        elif ActionType.turn_left == action_type or ActionType.turn_right == action_type:
            #방향전환은 어떤 상황에서든 무조건 가능한 행동이다.
            result = True
        elif ActionType.grab == action_type:
            #grap은 어떤 상황에서든 무조건 가능한 행동이다.
            result = True
        elif ActionType.shoot == action_type:
            #화살쏘기는 화살의 개수가 양수일 경우 가능한 행동이다.
            if self.arrow_count > 0:
                result = True
            else:
                result = False
        elif ActionType.climb == action_type:
            #등반은 어떤 상황에서든 무조건 가능한 행동이다.
            result = True
        else:
            raise ValueError("undefined value of action type")

        return result

    #게임이 끝났는지 여부를 확인하는 메서드
    def is_over(self):
        return self.is_game_over

    #해당 좌표에 목표 상태가 존재하는지 확인해주는 메서드
    def has_target_state_on_point(self, target_state_type, point):
        result = None
        if self.get_state_type_on_point(point) == target_state_type:
            result = True
        else:
            result = False
        return result

    #해당 좌표의 상태가 무엇인지 알려주는 메서드
    def get_state_type_on_point(self, point):
        state_type = self.grid[point.row][point.col]
        return state_type

    #해당 좌표의 정적인 상태의 집합을 반환하는 메서드
    def get_percept_type_list_on_point(self, point):
        percept_type_set = set() # 중복을 제거하기 위해 set을 사용

        neighbors = point.neighbors()
        for neighbor in neighbors:
            # 버그 수정 : 이웃 중에 맵 범위 밖을 넘어가는 경우 탐색 생략
            if not self.is_valid_coordinate(neighbor):
                continue
            # 주변에 괴물(wumpus)이 존재할 경우 악취(stench)를 인지
            if self.has_target_state_on_point(StateType.wumpus, neighbor):
                percept_type_set.add(PerceptType.stench)
            # 주변에 웅덩이(pit)가 존재할 경우 바람(breeze)을 인지
            if self.has_target_state_on_point(StateType.pit, neighbor):
                percept_type_set.add(PerceptType.breeze)
        # 해당 위치에 벽(wall)이 존재할 경우 충돌(bump)을 인지
        if self.has_target_state_on_point(StateType.wall, point):
            percept_type_set.add(PerceptType.bump)
        # 해당 위치에 금(gold)이 존재할 경우 반짝임(glitter)을 인지
        if self.has_target_state_on_point(StateType.gold, point):
            percept_type_set.add(PerceptType.glitter)
        # 비명(scream)은 정적인 상태가 아니므로 여기서 구현할 수 없음 -> 동적인 상태이므로 행동을 하는 즉시 발동되어야 함

        return list(percept_type_set)