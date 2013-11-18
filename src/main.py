def returnContOpen(pat, pos, board, withEnds=False):
    results = []
    ends = []
    def appendContinous(direction):
        for field in [(pos[0]+d*direction[0],pos[1]+d*direction[1]) for d in range(1,8)]:
                try:
                    if board[field[0]][field[1]]:
                        ends.append(field)
                        break
                    else: results.append(field);
                except IndexError: break
    if pat[1]:
        for direction in ((1,1),(1,-1),(-1,1),(-1,-1)): appendContinous(direction)
    if pat[0]:
        for direction in ((1,0),(-1,0),(0,1),(0,-1)): appendContinous(direction)
    if withEnds: return results, ends
    else: return results

def getLegal(pat, pos, board, col):
    results = []
    if pat == "K":
        for field in [(pos[0]+x,pos[1]+y) for x in (-1,0,1) for y in (-1,0,1)]:
            try:
                if not (board[field[0]][field[1]]) or isAttackable(field,board,col): results.append(field)
            except IndexError: continue
    elif pat == "N":
        for field in [(pos[0]+x,pos[1]+y) for x in (-2,0,2) for y in (-1,0,1)]:
            try:
                if (not board[field[0]][field[1]]) or isAttackable(field,board,col): results.append(field)
                if (not board[field[1]][field[0]]) or isAttackable((field[1],field[0]),board,col): results.append((field[1],field[0]))
            except IndexError: continue
    elif pat == "P":
        try:
            if not board[pos[0]][pos[1]+col]: results.append((pos[0],pos[1]+col))
        except IndexError: pass
    elif pat == "P1":
        try:
            if not board[pos[0]][pos[1]+2*col]: results.append((pos[0],pos[1]+2*col))
        except IndexError: pass
        results+=getLegal("P",pos,board,col)
    elif pat == "PA":
        for dirct in (-1,1):
            try:
                if isAttackable((pos[0]+dirct,pos[1]+col),board,col): results.append((pos[0]+dirct,pos[1]+col))
            except IndexError: continue
    else:
        cont, ends = returnContOpen(pat,pos,board)
        return cont + [f for f in ends if isAttackable(f,board,col)]
    return results

