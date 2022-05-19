"""
Fairly Allocating Many Goods with Few Queries (2019)

Authors: Hoon Oh, Ariel D. Procaccia, Warut Suksompong. See https://ojs.aaai.org/index.php/AAAI/article/view/4046/3924

Programmer: Aviem Hadar
Since: 2022
"""
import doctest
import sys
from copy import copy
from typing import List, Any

import fairpy
from fairpy import Agent
from fairpy.allocations import Allocation


def two_agents_ef1(agents: List[Agent], items: List[Any]) -> Allocation:
    """
    Algorithm No 1

    Allocates the given items(inside each agent) to the 2 given agents while satisfying EF1 condition.
    read more about EF1 here: https://en.wikipedia.org/wiki/Envy-free_item_allocation#EF1_-_envy-free_up_to_at_most_one_item

    :param agents: The agents who participate in the allocation.
    :param items: The items which are being allocated.
    :return: An allocation for each of the agents.


    >>> ### Using Agent objects:
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":1,"f":7,"g":15}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":1,"f":7,"g":15}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],["a", "b", "c", "d", "e", "f", "g"])
    >>> allocation
    Alice gets {g} with value 15.
    George gets {a,b,c,d,e,f} with value 20.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and George.is_EF1(allocation[1], allocation)
    True
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":4,"f":7,"g":15}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":4,"f":7,"g":15}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],["a", "b", "c", "d", "e", "f", "g"])
    >>> allocation
    Alice gets {f,g} with value 22.
    George gets {a,b,c,d,e} with value 16.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and George.is_EF1(allocation[1], allocation)
    True
    >>> ### ONLY ONE OBJECT
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 2}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({"a": 2}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],["a"])
    >>> allocation
    Alice gets {} with value 0.
    George gets {a} with value 2.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and George.is_EF1(allocation[1], allocation)
    True
    >>> ### nothing to allocate
    >>> Alice = fairpy.agents.AdditiveAgent({}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],[])
    >>> allocation
    Alice gets {} with value 0.
    George gets {} with value 0.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and George.is_EF1(allocation[1], allocation)
    True
    """
    items = agents[0].all_items()
    Lg_value = 0
    Rg_value = agents[0].total_value()
    rightmost = None
    for item in items:
        if Lg_value <= Rg_value:
            Lg_value += agents[0].value(item)
            Rg_value -= agents[0].value(item)
            rightmost = item
        else:
            break
    Lg = []
    Rg = []
    # partitioning the items
    rightmost_found = False
    if rightmost is not None and Lg_value - agents[0].value(rightmost) <= Rg_value:
        for item in items:
            if rightmost_found is False:
                Lg.append(item)
                if item == rightmost:
                    rightmost_found = True
            else:
                Rg.append(item)
    else:
        for item in items:
            if item == rightmost:
                rightmost_found = True
            if rightmost_found is False:
                Lg.append(item)
            else:
                Rg.append(item)
    allocation = Allocation(agents=agents, bundles={agents[0].name(): Rg, agents[1].name(): Lg})
    return allocation


def three_agents_IAV(agents: List[Agent], items: List[Any]) -> Allocation:
    """
    Algorithm No 2 - three agents with identical additive valuations
    Allocating the given items to three agents while satisfying EF1 condition
    >>> Alice = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d"])
    >>> allocation
    Alice gets {b} with value 3.
    Bob gets {c,d} with value 3.
    George gets {a} with value 4.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[2], allocation)
    True
    >>> Alice = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d","e","f","g"])
    >>> allocation
    Alice gets {a,b} with value 11.
    Bob gets {c,d,e} with value 5.
    George gets {f,g} with value 6.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[2], allocation)
    True
    >>> Alice = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4,"h":5,"i":0,"j":9,"k":8,"l":2,"m":8,"n":7}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4,"h":5,"i":0,"j":9,"k":8,"l":2,"m":8,"n":7}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4,"h":5,"i":0,"j":9,"k":8,"l":2,"m":8,"n":7}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d","e","f","g","h","i","j","k","l","m","n"])
    >>> allocation
    Alice gets {a,b,c,d,e,f} with value 18.
    Bob gets {g,h,i,j} with value 18.
    George gets {k,l,m,n} with value 25.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[2], allocation)
    True
    >>> ### TOTALLY UNFAIR CASE
    >>> Alice = fairpy.agents.AdditiveAgent({"a":30,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":1}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":30,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":1}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":30,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":1}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d","e","f","g","h"])
    >>> allocation
    Alice gets {b,c,d,e} with value 4.
    Bob gets {f,g,h} with value 3.
    George gets {a} with value 30.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[2], allocation)
    True
    >>> ### TOTALLY UNFAIR CASE
    >>> Alice = fairpy.agents.AdditiveAgent({"a":1,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":30}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":1,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":30}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":1,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":30}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d","e","f","g","h"])
    >>> allocation
    Alice gets {a,b,c,d} with value 4.
    Bob gets {e,f,g} with value 3.
    George gets {h} with value 30.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[2], allocation)
    True
    """
    Lg3_value = 0
    A = []
    Lg3 = []
    G = items.copy()
    g1, Lg1, Lg1_value = find_g1(agents[0], items)
    g2, Rg2, Rg2_value = find_g2(agents[0], items)
    # if u(Lg1) >= u(Rg2)
    rev = items.copy()
    rev.reverse()
    if Lg1_value < Rg2_value:
        g1, Lg1, Lg1_value = find_g1(agents[0], rev)
        g2, Rg2, Rg2_value = find_g2(agents[0], rev)
    # STEP 2 #
    if len(Lg1) != 0:
        for item in items:
            Lg3.append(item)
            g3 = item
            Lg3_value += agents[0].value(item)
            if Lg3_value >= Rg2_value:
                break
        A = Lg3
    C = Rg2
    B = G.copy()
    AuC = A.copy() + C  # A u C
    [B.remove(arg) for arg in AuC]  # B = G\(A u C)
    B_copy = B.copy()
    if B_copy.count(g2) != 0:
        B_copy.remove(g2)
    if agents[0].value(C) >= agents[0].value(B_copy):  # if u(C) >= u(B\{g2})
        allocation = Allocation(agents=agents, bundles={agents[0].name(): A, agents[1].name(): B, agents[2].name(): C})
    else:
        C_tag = copy(Rg2)  # C' = Rg2 u {g2}
        C_tag.append(g2)
        C_tag.sort()
        remaining_goods = G.copy()
        [remaining_goods.remove(arg) for arg in C_tag]  # G \ C'
        A_tag, B_tag = Lemma4_1(remaining_goods, agents[0])
        allocation = Allocation(agents=agents,
                                bundles={agents[0].name(): A_tag, agents[1].name(): B_tag, agents[2].name(): C_tag})
    return allocation


def find_g1(agent, items):
    g1 = ""
    Lg1 = []
    Lg1_value = 0
    uG = agent.value(agent.all_items())
    for item in items:
        if Lg1_value + agent.value(item) > uG / 3:
            g1 = item
            break
        Lg1.append(item)
        Lg1_value += agent.value(item)
    return g1, Lg1, Lg1_value


def find_g2(agent, items):
    g2 = ""
    uG = agent.value(agent.all_items())
    Rg2_value = uG
    Rg2 = items.copy()
    for item in items:
        if Rg2_value + agent.value(item) <= uG / 3:
            break
        g2 = item
        Rg2.remove(item)
        Rg2_value -= agent.value(item)
        if Rg2_value + agent.value(item) <= uG / 3:
            break
    return g2, Rg2, Rg2_value


# partitioning the bundle to 2
def Lemma4_1(remaining_goods: list, agent):
    A_tag = []
    B_tag = remaining_goods.copy()
    a_value = 0
    b_value = agent.value(remaining_goods)
    minimum = sys.maxsize
    for item in remaining_goods:
        a_value += agent.value(item)
        b_value -= agent.value(item)
        if abs(a_value - b_value) <= minimum:
            minimum = abs(a_value - b_value)
            A_tag.append(item)
            B_tag.remove(item)
        else:
            break
    return A_tag, B_tag


# def three_agents_AAV(agents: List[Agent], items: List[Any]) -> Allocation:
#     """
#     Algorithm No 3 - three agents with arbitrary additive valuations
#     Allocating the given items to three agents with different valuations for the items while satisfying EF1 condition
#     >>> Alice = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="Alice")
#     >>> Bob = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":3,"f":2,"g":3}, name="Bob")
#     >>> George = fairpy.agents.AdditiveAgent({"a":4,"b":5,"c":1,"d":2,"e":2,"f":3,"g":4}, name="George")
#     >>> allocation = three_agents_AAV([Alice,Bob,George],["a","b","c","d","e","f","g"])
#     >>> allocation
#     Alice gets {c,d,e} with value 5.
#     Bob gets {a,b} with value 11.
#     George gets {f,g} with value 7.
#     <BLANKLINE>
#     >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[2], allocation)
#     True
#     """
#     return 0


if __name__ == "__main__":
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

    # Alice = fairpy.agents.AdditiveAgent({"a": 4, "b": 3, "c": 2, "d": 1}, name="Alice")
    # Bob = fairpy.agents.AdditiveAgent({"a": 4, "b": 3, "c": 2, "d": 1}, name="Bob")
    # George = fairpy.agents.AdditiveAgent({"a": 4, "b": 3, "c": 2, "d": 1}, name="George")
    # a = three_agents_IAV([Alice, Bob, George], ["a", "b", "c", "d"])
    # print(a)

    # Alice = fairpy.agents.AdditiveAgent({"a": 5, "b": 6, "c": 1, "d": 2, "e": 2, "f": 2, "g": 4}, name="Alice")
    # Bob = fairpy.agents.AdditiveAgent({"a": 5, "b": 6, "c": 1, "d": 2, "e": 2, "f": 2, "g": 4}, name="Bob")
    # George = fairpy.agents.AdditiveAgent({"a": 5, "b": 6, "c": 1, "d": 2, "e": 2, "f": 2, "g": 4}, name="George")
    # a = three_agents_IAV([Alice, Bob, George], ["a", "b", "c", "d", "e", "f", "g"])
    # print(a)

    # Alice = fairpy.agents.AdditiveAgent(
    #     {"a": 5, "b": 6, "c": 1, "d": 2, "e": 2, "f": 2, "g": 4, "h": 5, "i": 0, "j": 9, "k": 8, "l": 2, "m": 8,
    #      "n": 7}, name="Alice")
    # Bob = fairpy.agents.AdditiveAgent(
    #     {"a": 5, "b": 6, "c": 1, "d": 2, "e": 2, "f": 2, "g": 4, "h": 5, "i": 0, "j": 9, "k": 8, "l": 2, "m": 8,
    #      "n": 7}, name="Bob")
    # George = fairpy.agents.AdditiveAgent(
    #     {"a": 5, "b": 6, "c": 1, "d": 2, "e": 2, "f": 2, "g": 4, "h": 5, "i": 0, "j": 9, "k": 8, "l": 2, "m": 8,
    #      "n": 7}, name="George")
    # a = three_agents_IAV([Alice, Bob, George], ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n"])
    # print(a)

    # Alice = fairpy.agents.AdditiveAgent({"a": 30, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 1}, name="Alice")
    # Bob = fairpy.agents.AdditiveAgent({"a": 30, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 1}, name="Bob")
    # George = fairpy.agents.AdditiveAgent({"a": 30, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 1},
    #                                      name="George")
    # allocation = three_agents_IAV([Alice, Bob, George], ["a", "b", "c", "d", "e", "f", "g", "h"])
    # # result = Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(
    # #     allocation[2],
    # #     allocation)
    # # print(result)
    # print(allocation)

    # Alice = fairpy.agents.AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 30}, name="Alice")
    # Bob = fairpy.agents.AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 30}, name="Bob")
    # George = fairpy.agents.AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 30},
    #                                      name="George")
    # a = three_agents_IAV([Alice, Bob, George], ["a", "b", "c", "d", "e", "f", "g", "h"])
    # print(a)
