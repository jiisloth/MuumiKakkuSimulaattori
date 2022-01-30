import random
import copy


# Cake sideways cause why not, also added border to avoid getting out of range :DD
empty = [
    [8,8,8,8,8,8,8,8,8],
    [8,9,9,9,9,9,0,0,8],
    [8,9,9,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,8],
    [8,0,0,0,0,0,0,0,8],
    [8,9,9,0,0,0,0,0,8],
    [8,9,9,9,9,9,0,0,8],
    [8,8,8,8,8,8,8,8,8],
]
fillchar = " ABCZYXI?#"
start_pos = 4
start_dir = -1

tac = {
    "NoFails": 0,
    "Fails": 0,
    "Moves": 0,
    "Turns": 0
}
fast = {
    "NoFails": 0,
    "Fails": 0,
    "Moves": 0,
    "Turns": 0
}
cycles = 1000

def main():
    for i in range(cycles):
        print("Turn: " + str(i))
        bake_cakes()
    print("TACTICAL:")
    print(tac)
    print("FAST:")
    print(fast)

def bake_cakes():
    # Very nice variables we have here..
    tac_cake = copy.deepcopy(empty)
    tac_pos = start_pos
    tac_dir = start_dir
    tac_fails = 0
    tac_moves = 0
    tac_turns = 0
    fast_cake = copy.deepcopy(empty)
    fast_pos = start_pos
    fast_dir = start_dir
    fast_fails = 0
    fast_moves = 0
    fast_turns = 0
    while True:
        next = random.randint(1, 7)
        if check_holes(tac_cake):
            #Do the tactical cake stuff:
            fill, fail = get_tac_fill_pos(tac_cake, next, tac_pos, tac_dir)
            tac_cake = fill_cake(tac_cake, fill, next)
            if fail:
                tac_fails += 1
            move, turn = get_moves(fill, tac_pos, tac_dir)
            tac_moves += abs(move)
            tac_pos += move
            if turn:
                tac_dir = -tac_dir
                tac_turns += 1

        if check_holes(fast_cake):
            #Do the fast cake stuff
            fill, fail = get_fast_fill_pos(fast_cake, next, fast_pos, fast_dir)
            fast_cake = fill_cake(fast_cake, fill, next)
            if fail:
                fast_fails += 1
            move, turn = get_moves(fill, fast_pos, fast_dir)
            fast_moves += abs(move)
            fast_pos += move
            if turn:
                fast_dir = -fast_dir
                fast_turns += 1
        if not check_holes(tac_cake) and not check_holes(fast_cake):
            break
        #print_cake(tac_cake)
        #print_cake(fast_cake)
    print("TACT: Fails: " + str(tac_fails) + " Moves: " + str(tac_moves) + " Turns: " +str(tac_turns))
    print("FAST: Fails: " + str(fast_fails) + " Moves: " + str(fast_moves) + " Turns: " +str())
    tac["Fails"] += tac_fails
    tac["Moves"] += tac_moves
    tac["Turns"] += tac_turns
    if tac_fails == 0:
        tac["NoFails"] += 1
    fast["Fails"] += fast_fails
    fast["Moves"] += fast_moves
    fast["Turns"] += fast_turns
    if fast_fails == 0:
        fast["NoFails"] += 1

def check_holes(cake):
    #returns false if cake is finished
    for row in cake:
        for spot in row:
            if spot == 0:
                return True
    return False

def get_tac_fill_pos(cake, next, pos, d):
    tactical_scores = []
    fails = []
    distance_scores = []
    for x, line in enumerate(cake):
        if 0 < x < len(cake)-1:
            ts = None
            fail = None
            distance_scores.append(10-get_distance(x, pos, d))
            for y, spot in enumerate(line):
                if spot == 0:
                    newcake, fail = add_to_spot(cake, x, y, next)
                    ts = calculate_tactical_score(newcake)
                    break
            tactical_scores.append(ts)
            fails.append(fail)
    best = [-9999999,0]  #just some base numbers
    for i in range(len(fails)):
        if fails[i] is not None:  #dont do full lines
            score = tactical_scores[i]*100+distance_scores[i]
            if fails[i]:
                score -= 10000
            if score > best[0]:
                best = [score, i+1]
    if best[0] < 0:
        return best[1], True
    else:
        return best[1], False


def get_fast_fill_pos(cake, next, pos, d):
    fails = []
    distance_scores = []
    for x, line in enumerate(cake):
        if 0 < x < len(cake):
            fail = None
            distance_scores.append(10-get_distance(x, pos, d))
            for y, spot in enumerate(line):
                if spot == 0:
                    newcake, fail = add_to_spot(cake, x, y, next)
            fails.append(fail)
    best = [-9999999,0]
    for i in range(len(distance_scores)):
        if fails[i] is not None:
            score = distance_scores[i]
            if fails[i]:
                score -= 10000
            if score > best[0]:
                best = [score, i+1]
    if best[0] < 0:
        return best[1], True
    else:
        return best[1], False


def fill_cake(cake, fill, next):
    for y, spot in enumerate(cake[fill]):
        if spot == 0:
            cake, f = add_to_spot(cake, fill, y, next)
            return cake

def get_moves(fill, pos, d):
    if abs(pos+d-fill) < abs(pos-d-fill):
        return fill-(pos+d), False
    else:
        return fill-(pos-d), True


def get_distance(x, pos, dire):
    least = 100
    for d in [-1,1]:
        extra = 0
        if d != dire:
            extra = 0.5
        least = min(abs(pos+d-x)+extra, least)
    return least

def calculate_tactical_score(cake):
    #Could be much better...
    score = 0
    for x, line in enumerate(cake):
        if 0 < x < len(cake):
            for y, spot in enumerate(line):
                candies = [1,2,3,4,5,6,7]
                if spot == 0:
                    for s in [cake[x][y - 1], cake[x+1][y], cake[x-1][y]]:
                        if s not in candies:
                            score += 1
                        else:
                            candies.remove(s)
    return score




def add_to_spot(cake, x, y, next):
    new_cake = copy.deepcopy(cake)
    fail = True
    if new_cake[x][y-1] == next:  #Remove candy if next to same..
        new_cake[x][y - 1] = 0
    elif new_cake[x-1][y] == next:  #Remove candy if next to same..
        new_cake[x - 1][y] = 0
    elif new_cake[x+1][y] == next:  #Remove candy if next to same..
        new_cake[x + 1][y] = 0
    else:  # add candy.
        fail = False
        new_cake[x][y] = next
    return new_cake, fail





def print_cake(cake):
    # use this if ya wanna print the cake.
    for x in range(len(cake[0])):
        line = ""
        for y in range(len(cake)):
            line += fillchar[cake[y][x]]
        print(line)

if __name__ == '__main__':
    main()

