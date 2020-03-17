import random, math, time

toggle0 = True
dashed_line = "-" * 80

class Card:
    def __init__(self,
                id,
                name,
                owner=0,
                tier=0,
                alive=True,
                attack=1,
                health=1,
                curr_attack=1,
                curr_health=1,
                tribe="None",
                is_token=False,
                divine_shield=False,
                taunt=False):
        self.id = id
        self.name = name
        self.owner = owner
        self.tier = tier
        self.alive = alive
        self.attack = attack
        self.health = health
        self.curr_attack = attack
        self.curr_health = health
        self.tribe = tribe
        self.is_token = is_token
        self.divine_shield = divine_shield
        self.taunt = taunt

    # ==========================================================================
    # SETTERS
    # ==========================================================================

    def set_id(self, id):
        self.id = id

    def set_name(self, name):
        self.name = name

    def set_owner(self, owner):
        self.owner = owner

    def set_tier(self, tier):
        self.tier = tier

    def set_alive(self, alive):
        self.alive = alive

    def set_attack(self, attack):
        self.attack = attack

    def set_health(self, health):
        self.health = health

    def set_curr_attack(self, curr_attack):
        self.curr_attack = curr_attack

    def set_curr_health(self, curr_health):
        self.curr_health = curr_health

    def set_tribe(self, tribe):
        self.tribe = tribe

    def set_is_token(self, is_token):
        self.is_token = is_token

    def set_divine_shield(self, divine_shield):
        self.divine_shield = divine_shield

    def set_taunt(self, taunt):
        self.taunt = taunt

    # ==========================================================================
    # GETTERS
    # ==========================================================================
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_owner(self):
        return self.owner

    def get_tier(self, tier):
        self.tier = tier

    def get_alive(self):
        return self.alive

    def get_attack(self):
        return self.attack

    def get_health(self):
        return self.health

    def get_curr_attack(self):
        return self.curr_attack

    def get_curr_health(self):
        return self.curr_health

    def get_tribe(self):
        return self.tribe

    def get_is_token(self):
        return self.is_token

    def get_divine_shield(self):
        return self.divine_shield

    def get_taunt(self):
        return self.taunt

class Board:
    def __init__(self, player, cards=[], is_full=False, num_alive = 0):
        self.player = player # either 0 or 1
        self.cards = cards
        self.is_full = is_full
        self.num_alive = len(cards)

    # ==========================================================================
    # SETTERS
    # ==========================================================================

    def set_player(self, player):
        self.player = player

    def set_cards(self, cards):
        self.cards = cards

    def set_is_full(self, is_full):
        self.is_full = is_full

    def set_num_alive(self, num_alive):
        self.num_alive = num_alive

    # ==========================================================================
    # GETTERS
    # ==========================================================================
    def get_player(self):
        return self.player

    def get_cards(self):
        return self.cards

    def get_is_full(self):
        return self.is_full

    def get_num_alive(self):
        return self.num_alive

    # <--- OTHER --->
    def find_card(self, id):
        for c in self.cards:
            if c.get_id() == id:
                return c
        return 0

class State:
    def __init__(self, cards=[],boards=[]):
        self.boards = boards
        self.cards = cards
    # ==========================================================================
    # SETTERS
    # ==========================================================================
    def set_boards(self, boards):
        self.boards = boards

    def set_cards(self):
        self.cards = []
        for board in self.boards:
            self.cards.append(board.get_cards())

    # ==========================================================================
    # GETTERS
    # ==========================================================================
    def get_boards(self):
        return self.boards

    def get_cards(self):
        return self.cards
    # ==========================================================================
    # OTHER
    # ==========================================================================

    def find_card(self, id):
        for c in self.cards:
            if c.get_id() == id:
                return c
        return 0

def calc_health(c1, c2):
    return c1.get_curr_health() - c2.get_curr_attack()

def remove_card(board, card):
    #print("beginning removal process")
    board_cards = board.get_cards()
    target_id = card.get_id()
    #print("target_id is " + target_id)
    for c in board_cards:
        #print("c_id is " + c.get_id())
        if c.get_id() == target_id:
            #print("will remove")
            board_cards.remove(c)
    board.set_cards(board_cards)
    #print("ending removal process")

def reset_stats(c):
    c.set_curr_attack(c.get_attack())
    c.set_curr_health(c.get_health())

def print_card_info(c):
    print("    * Card_ID: " + c.get_id())
    print("      * Curr Attack: " + str(c.get_curr_attack()) )
    print("      * Curr Health: " + str(c.get_curr_health()) )


def print_board_stats(b):
    print(dashed_line)
    title = "/" * 10 + "\\" * 10
    title_rev = "\\" * 10 + "/" * 10

    print(title)
    print("Board Stats: " + str(b.get_player()) )
    print(title_rev)
    print("* Player: " + str(b.get_player()) )

    i = 0
    print("* Cards")
    for c in b.get_cards():
        print_card_info(c)
        i +=1

    print("* Is_full: " + str(b.get_is_full()) )
    print(dashed_line)

def print_state(st):
    boards = st.get_boards()
    length = 0
    string = ""
    spaces = ""
    title_spaces = "<" * 10 + ">" * 10

    print(title_spaces)
    print(" "*4+"BOARD STATE")
    print(title_spaces)

    for b in boards:
        p = str(b.get_player())
        cards = b.get_cards()
        for c in cards:
            if c.get_alive():
                length += len(c.get_id()) + 1
                string += c.get_id() + " "
        spaces = "="*(length+2)
        print("Player " + str(p))
        print(spaces)
        print(string)
        print(spaces)
        print(" "*(length+2))
        length = 0
        string = ""
        spaces = ""

def combat(card1, card2, st):
    """
    Combat is performed, where {card1} attacks {card2}.
    """
    boards = st.get_boards()
    cards = st.get_cards()
    c1 = card1
    c2 = card2
    b1 = boards[c1.get_owner()]
    b2 = boards[c2.get_owner()]
    # update health

    c2_health = calc_health(c2, c1)
    #print("c2 health is " + str(c2_health))
    c2.set_curr_health(c2_health)

    if c2.get_curr_health() <= 0:
        #print("BOARD STATE UPDATED: " + c2.get_id() + " DIED")
        c2.set_alive(False)
        b2_alive = b2.get_num_alive()
        b2.set_num_alive(b2_alive-1)
        # remove_card(b2, c2)

    c1_health = calc_health(c1, c2)
    #print("c1 health is " + str(c1_health))
    c1.set_curr_health(c1_health)
    if c1.get_curr_health() <= 0:
        #print("BOARD STATE UPDATED: " + c1.get_id() + "DIED\N")
        c1.set_alive(False)
        b1_alive = b1.get_num_alive()
        b1.set_num_alive(b1_alive-1)
        # remove_card(b1, c1)

    st.set_cards()
    return st

def autobattler(st):
    # compare number of units
    idx_fst = st.boards[1].get_num_alive() > st.boards[0].get_num_alive()
    idx_snd = not idx_fst
    fst = st.boards[idx_fst]
    snd = st.boards[idx_snd]
    len_fst = fst.get_num_alive()
    len_snd = snd.get_num_alive()
    fst_cards = fst.get_cards()
    snd_cards = snd.get_cards()
    i = 0
    j = 0
    # person with most units fights first
    fighter = fst
    defender = snd
    fc = fst_cards
    dc = snd_cards
    q = 0
    while fst.get_num_alive() > 0 and snd.get_num_alive() > 0:
        print("iteration: " + str(q))
        if toggle0:
            print_state(st)
            print("<---PRECOMBAT--->")
            print_board_stats(fighter)
            print_board_stats(defender)
            print("<---COMBAT--->")
        time.sleep(3)
        combat(fc[i], dc[j], st)
        if toggle0:
            print("<---POSTCOMBAT--->")
            print_board_stats(fighter)
            print_board_stats(defender)
            print_state(st)
        time.sleep(3)
        temp = fighter
        fighter = defender
        defender = temp
        temp = fc
        fc = dc
        dc = temp
        j = random.randint(0, defender.get_num_alive())
        q += 1
    # keep fighting until no more units alive
    # declare a winner
    if fst.get_num_alive() > snd.get_num_alive():
        winner = fst
        print("WINNER IS... " + fst.get_player())
    elif snd.get_num_alive() > fst.get_num_alive():
        winner = snd
        print("WINNER IS... " + snd.get_player())
    else:
        winner = "None"
        print("WINNER IS... NO ONE")
    # reset curr health
    for c in fc:
        reset_stats(c)
    for c in dc:
        reset_stats(c)
