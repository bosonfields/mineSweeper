import random
from enum import Enum
import copy

BLOCK_WIDTH = 30
BLOCK_HEIGHT = 16
SIZE = 20
MINE_COUNT = 99

class RevealStatus(Enum):
    cover = 1
    uncover = 2

class BlockStatus(Enum):
    no_click = 1
    no_mine = 2
    mine = 3
    flag = 4
    error = 5
    bomb = 6

class Mine:
    def __init__(self, x, y, value=0):
        self._x = x
        self._y = y
        self._value = 0
        self._around_mine_count = -1
        self._status = BlockStatus.no_click
        self.set_value(value)

    def __repr__(self):
        return str(self._value)

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    x = property(fget=get_x, fset=set_x)

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    y = property(fget=get_y, fset=set_y)

    def get_value(self):
        return self._value

    def set_value(self, value):
        if value:
            self._value = 1
        else:
            self._value = 0

    value = property(fget=get_value, fset=set_value)

    def get_around_mine_count(self):
        return self._around_mine_count

    def set_around_mine_count(self, around_mine_count):
        self._around_mine_count = around_mine_count

    around_mine_count = property(fget=get_around_mine_count, fset=set_around_mine_count)

    def get_status(self):
        return self._status

    def set_status(self, value):
        self._status = value

    status = property(fget=get_status, fset=set_status)


class MineBlock:
    def __init__(self):
        self._block = [[Mine(i, j) for i in range(BLOCK_WIDTH)] for j in range(BLOCK_HEIGHT)]
        self._mineList = []

        self._tmp_order = []
        self._back_memory= []

        for i in random.sample(range(BLOCK_WIDTH * BLOCK_HEIGHT), MINE_COUNT):
            self._block[i // BLOCK_WIDTH][i % BLOCK_WIDTH].value = 1
            self._mineList.append((i % BLOCK_WIDTH, i // BLOCK_WIDTH))
        self._mineSet = set(self._mineList)

    def get_block(self):
        return self._block

    block = property(fget=get_block)

    def getmine(self, x, y):
        return self._block[y][x]

    def getclue(self):
        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_HEIGHT):
                if self.getmine(x, y).value==0:
                    around =_get_around(x, y)
                    _sum = 0
                    for i, j in around:
                        if self.getmine(i, j).value:
                            _sum += 1
                    self.getmine(x, y).around_mine_count = _sum

    def read_agent(self, agent):
        self._tmp_order = copy.deepcopy(agent._step_order)

    def add_back(self):
        if self._tmp_order:
            self._back_memory.append(self._tmp_order.pop())

    def add_forward(self):
        if self._back_memory:
            self._tmp_order.append(self._back_memory.pop())
            print("This is step:", len(self._tmp_order))
            print(self._tmp_order)

    def reveal_agent(self, agent_tmp, reveal_status):
        for node in self._back_memory:
            i, j = node
            self.getmine(i, j).status = BlockStatus.no_click
        for node in self._tmp_order:
            i, j = node
            if agent_tmp._opended[node] == "flag":
                self.getmine(i, j).status = BlockStatus.flag
                if reveal_status == RevealStatus.uncover and self.getmine(i, j).value==0:
                    self.getmine(i, j).status = BlockStatus.error
            elif agent_tmp._opended[node] == "no_mine" and self.getmine(i, j).value == 0:
                self.getmine(i, j).status = BlockStatus.no_mine
            elif agent_tmp._opended[node] == "no_mine" and self.getmine(i, j).value == 1:
                self.getmine(i, j).status = BlockStatus.bomb
            else:
                self.getmine(i, j).status = BlockStatus.bomb


    def getStart(self):
        start_node=(random.randint(0, BLOCK_WIDTH-1), random.randint(0, BLOCK_HEIGHT-1))
        while start_node in self._mineSet:
            start_node = (random.randint(0, BLOCK_WIDTH - 1), random.randint(0, BLOCK_HEIGHT - 1))
        x, y = start_node
        self.getmine(x, y).status = BlockStatus.no_mine
        return start_node

    def double_check(self, x, y):
        sum_flaged = 0
        sum_bombed = 0
        sum_no_click = 0
        no_click_pairs = []
        around_count = self.getmine(x, y).around_mine_count
        around = _get_around(x, y)
        for node in around:
            i, j = node
            if self.getmine(i, j).status == BlockStatus.no_click:
                no_click_pairs.append(node)
                sum_no_click +=1
            elif self.getmine(i, j).status == BlockStatus.flag:
                sum_flaged +=1
            elif self.getmine(i, j).status == BlockStatus.bomb:
                sum_bombed +=1
        all_need_flag = around_count - sum_flaged - sum_bombed == sum_no_click
        all_need_open = around_count - sum_flaged - sum_bombed == 0

        unexplored = around_count - sum_flaged - sum_bombed

        return no_click_pairs, all_need_open, all_need_flag, unexplored

    def random_open(self, node):
        x, y = node
        candidates, open_status, flag_status, unexplored=self.double_check(x, y)
        if candidates:
            i, j = random.choice(candidates)
            if self.getmine(i, j).value == 1:
                self.getmine(i, j).status = BlockStatus.bomb
                return (i, j), "bomb"
            else:
                self.getmine(i, j).status = BlockStatus.no_mine
                return (i, j), "no_mine"
        else:
            return (x, y), "all_opened"

    def flag_node(self, node):
        x, y = node
        self.getmine(x, y).status = BlockStatus.flag

    def open_node(self, node):
        x, y = node
        self.getmine(x, y).status = BlockStatus.no_mine

    def bomb_node(self, node):
        x, y = node
        self.getmine(x, y).status = BlockStatus.bomb


def _get_around(x, y):
    return [(i, j) for i in range(max(0, x - 1), min(BLOCK_WIDTH - 1, x + 1) + 1)
            for j in range(max(0, y - 1), min(BLOCK_HEIGHT - 1, y + 1) + 1) if i != x or j != y]
