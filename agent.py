from mineblock import *
import random
import itertools
from itertools import combinations

class Agent:
    def __init__(self):
        self._opended = {}
        self._step_order =[]
        self._flag_count = 0
        self._bomb_count = 0

    def no_mine_record(self, node):
        self._opended[node] = "no_mine"
        self._step_order.append(node)

    def flag_record(self, node):
        self._opended[node] = "flag"
        self._step_order.append(node)
        self._flag_count +=1

    def bomb_record(self, node):
        self._opended[node] = "bomb"
        self._step_order.append(node)
        self._bomb_count +=1

    def Solver(self, MineBlock):
        start_node = MineBlock.getStart()
        self.no_mine_record(start_node)
        frontier =[start_node]
        solver_step = 0
        while frontier:
            simple_next_step = False
            for node in frontier:
                x, y = node
                no_click_pairs, all_empty, all_mine, current_count = MineBlock.double_check(x, y)
                if no_click_pairs:
                    if all_empty:
                        simple_next_step = True
                        frontier.remove(node)
                        for neighbor in no_click_pairs:
                            MineBlock.open_node(neighbor)
                            self.no_mine_record(neighbor)
                            frontier.append(neighbor)
                    if all_mine:
                        simple_next_step = True
                        frontier.remove(node)
                        for neighbor in no_click_pairs:
                            MineBlock.flag_node(neighbor)
                            self.flag_record(neighbor)
                else:
                    frontier.remove(node)
            if not simple_next_step:
                solver_step +=1
                print("The length of frontier is:", len(frontier), "and this is the ", solver_step,"th guess")
                if not self.pattern_determine(frontier, MineBlock):
                    remains = MINE_COUNT - self._flag_count - self._bomb_count
                    if remains >4 or len(frontier) >4:
                        self.simple_guess(frontier , MineBlock)
                    else:
                        self.ending_guess(frontier, MineBlock, remains)

    def ending_guess(self, frontier, MineBlock, remains):
        if frontier:
            remain_set = []
            for node in frontier:
                x, y = node
                around, Allempty, Allmine, current_num = MineBlock.double_check(x, y)
                remain_set.append(set(around))
            inter = comb = remain_set.pop()
            for arou in remain_set:
                comb = comb | arou
                inter = inter & arou
            sub = comb - inter

            if inter and len(inter) == remains:
                for node in list(inter):
                    MineBlock.flag_node(node)
                    self.flag_record(node)
            elif sub and len(sub) == remains:
                for node in list(inter):
                    MineBlock.flag_node(node)
                    self.flag_record(node)
            else:
                self.simple_guess(frontier, MineBlock)

    def simple_guess(self, frontier, MineBlock):
        if frontier:
            pre_next = random.choice(frontier)
            next_step, trial = MineBlock.random_open(pre_next)
            if trial == "bomb":
                self.bomb_record(next_step)
            elif trial == "no_mine":
                self.no_mine_record(next_step)
                frontier.append(next_step)

    def pattern_determine(self, frontier, MineBlock):
        List32 = []
        List31 = []
        List21 = []
        ListN1 = []
        find = False
        if frontier:
            count = len(frontier)
            for pair in frontier:
                x, y = pair
                around, Allempty, Allflag, current_count = MineBlock.double_check(x, y)
                if around:
                    if len(around) == 3 and current_count == 2:
                        List32.append(set(around))
                    elif len(around) ==3 and current_count ==1:
                        List31.append(set(around))
                    elif len(around) == 2 and current_count ==1:
                        List21.append(set(around))
                    elif current_count ==1:
                        ListN1.append(set(around))

            for two_mine_tuple in List32:
                for one_mine_tuple in List31:
                    inter_1 = two_mine_tuple & one_mine_tuple
                    if inter_1 and len(inter_1) == 2:
                        item_mine = (two_mine_tuple - inter_1).pop()
                        MineBlock.flag_node(item_mine)
                        self.flag_record(item_mine)

                        item_normal = (one_mine_tuple - inter_1).pop()
                        MineBlock.open_node(item_normal)
                        self.no_mine_record(item_normal)
                        frontier.append(item_normal)

                        List32.remove(two_mine_tuple)
                        List31.remove(one_mine_tuple)
                        List21.append(inter_1)
                        break

            for three_tuple in List31:
                for two_tuple in List21:
                    inter_2 = three_tuple & two_tuple
                    if inter_2 and len(inter_2) == 2:
                        item_normal = (three_tuple - inter_2).pop()
                        MineBlock.open_node(item_normal)
                        self.no_mine_record(item_normal)
                        frontier.append(item_normal)

                        List31.remove(three_tuple)
                        break

            for three_two_tuple in List32:
                for two_tuple in List21:
                    inter_3 = three_two_tuple & two_tuple
                    if inter_3 and len(inter_3) == 2:
                        item_mine = (three_two_tuple - inter_3).pop()
                        MineBlock.flag_node(item_mine)
                        self.flag_record(item_mine)

                        List32.remove(three_two_tuple)
                        break

            for N_tuple in ListN1:
                for two_tuple in List21:
                    inter_4 = N_tuple & two_tuple
                    if inter_4 == two_tuple:
                        item_empty = list(N_tuple - inter_4)
                        for node in item_empty:
                            MineBlock.open_node(node)
                            self.no_mine_record(node)
                            frontier.append(node)

                        ListN1.remove(N_tuple)
                        break

            if len(frontier) - count:
                find = True
        return find

# This is for force cracking
'''
    def force_crack_prepare(self, frontier, MineBlock, influence_len):
        Dict_inf = {}
        inf = []
        Comb_inf =[]
        if frontier:
            for pair in frontier:
                x, y = pair
                around, Allempty, Allmine, around_count = MineBlock.double_check(x, y)
                if around:
                    Dict_inf[around] = around_count
                    inf.append(around)
            for node in inf:
                i = inf.index(node)
                if i+influence_len<len(inf):
                    tmp = copy.deepcopy(inf[i:i+influence_len])
                else:
                    tmp = copy.deepcopy(inf[i:])
                Comb_inf.append(tmp)

        return Dict_inf, Comb_inf

    def force_crack(self, Dict_inf, Comb_inf):
        for five_list in Comb_inf:
            combine = set()
            for influence in five_list:
                combine = combine | set(influence)
            combine_list = list(combine)
            num = len(combine_list)
            Dict_value = {}
            for node in combine_list:
                Dict_value[node] = 0
            possible = []
            for i in range(2**num):
                binary = list(str(bin(i))[2:])
                for node in reversed(combine_list):
                    Dict_value[node] = int(binary.pop())
                if self.condition_figure(Dict_value, five_list, Dict_inf):
                    one_possible = []
                    for node in Dict_value:
                        if Dict_value[node]:
                            one_possible.append(node)
                    possible.append(one_possible)
            inter = set(possible.pop())
            for poss in possible:
                inter = inter & set(poss)
            if inter:
                return inter

    def condition_figure(self, Dict_value, five_list, Dict_inf):
        cond = True
        for influence in five_list:
            sum = 0
            for node in influence:
                sum = sum + Dict_value[node]
            if sum != Dict_inf[influence]:
                cond = False
                break
        return cond
'''
