from bg import *

# <--- CONSTANTS --->
toggle = True
dashed_line = "-" * 80

# <--- CARDS --->
c0 = Card(id="RH",
          name="Rockpool Hunter",
          attack=2,
          health=3,
          tribe="Murloc")

c1 = Card(id="MT",
          name="Murloc Tidehunter",
          attack=2,
          health=1,
          tribe="Murloc")

c2 = Card(id="WW",
          name="Wrath Weaver",
          attack=1,
          health=1)
# <--- OWNERS --->
c0.set_owner(0)
c1.set_owner(1)
c2.set_owner(1)
# <--- BOARDS --->
b0 = Board(player=0,
           cards=[c0])
b1 = Board(player=1,
           cards=[c1,c2])

st = State(boards=[b0,b1])

# <--- HELPER --->
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

# <--- TESTS --->
def test01():
    """Tests board getter functions for b0"""
    bool = True
    bool = bool and b0.get_player() == 0
    bool = bool and b0.get_cards() == [c0]
    bool = bool and b0.find_card("RH") == c0
    return bool

def test02(b0, c0):
    """Tests remove_card()"""
    bool = True
    print_board_stats(b0)
    remove_card(b0, c0)
    print_board_stats(b0)
    bool = bool and b0.get_cards() == []
    return bool

def test03():
    """Combat"""
    if toggle:
        print_state(st)
        print("<---PRECOMBAT--->")
        print_board_stats(b0)
        print_board_stats(b1)
        print("<---COMBAT--->")

    combat(c0, c1, st)
    combat(c0, c2, st)

    if toggle:
        print("<---POSTCOMBAT--->")
        print_board_stats(b0)
        print_board_stats(b1)
        print_state(st)

def test04():
    """Autobattler"""
    if toggle:
        print_state(st)
        print("<---PRECOMBAT--->")
        print_board_stats(b0)
        print_board_stats(b1)
        print("<---COMBAT--->")

    autobattler(st)

    if toggle:
        print("<---POSTCOMBAT--->")
        print_board_stats(b0)
        print_board_stats(b1)
        print_state(st)

    return True

if __name__ == "__main__":
    assert(test01())
    #assert(test02())
    #assert(test03())
    assert(test04())
