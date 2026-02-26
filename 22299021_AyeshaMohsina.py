# task1
def calculation(built, target, weights):
    score = 0
    if len(built) > len(target):
        L = len(built)
    else:
        L = len(target)

    for i in range(L):
        if i < len(built):
            a = ord(built[i])
        else:
            a = 0

        if i < len(target):
            b = ord(target[i])
        else:
            b = 0

        if a > b:
            d = a - b
        else:
            d = b - a

        if i < len(weights):
            w = weights[i]
        else:
            w = 1

        score = score + (d * w)

    return -score


def build(P, path, goal, weights, turn):
    if len(P) == 0:
        return calculation(path, goal, weights), path

    outcomes = []
    for i in range(len(P)):
        ch = P[i]
        rest = P[:i] + P[i+1:]
        val, seq = build(rest, path + ch, goal, weights, not turn)
        outcomes.append((val, seq))

    if turn:
        return max(outcomes)
    else:
        return min(outcomes)

def buildin(P, partial, reference, weights, max_turn, alp, B):
    if len(P) == 0:
        return calculation(partial, reference, weights), partial

    best = None

    if max_turn:
        max_val = -999999
        for i in range(len(P)):
            ch = P[i]
            rest = P[:i] + P[i+1:]
            val, res = buildin(rest, partial + ch, reference, weights, False, alp, B)
            if val > max_val:
                max_val = val
                best = res
            if val > alp:
                alp = val
            if B <= alp:
                break
        return max_val, best

    else:
        min_val = 999999
        for i in range(len(P)):
            ch = P[i]
            rest = P[:i] + P[i+1:]
            val, res = buildin(rest, partial + ch, reference, weights, True, alp, B)
            if val < min_val:
                min_val = val
                best = res
            if val < B:
                B = val
            if B <= alp:
                break
        return min_val, best

print("gene P:")
raw = input().strip()

print("Target gene sequence:")
target = input().strip()

print("Student ID :")
sid_input = input().strip()

sid_parts = sid_input.split()
sid_nums = []
valid_input = True

for part in sid_parts:
    if part.isdigit():
        sid_nums.append(int(part))
    else:
        print("Invalid SID part:", part)
        valid_input = False

if len(sid_nums) == 0:
    print("No digits found in SID.")
    valid_input = False

if valid_input:
    P_list = raw.split(',')
    if len(sid_nums) >= len(target):
        wt = []
        start = len(sid_nums) - len(target)
        for i in range(start, len(sid_nums)):
            wt.append(sid_nums[i])
    else:
        wt = []
        pad = len(target) - len(sid_nums)
        for i in range(pad):
            wt.append(1)
        for num in sid_nums:
            wt.append(num)
    score, gene = buildin(P_list, '', target, wt, True, -999999, 999999)
    print(f"Best gene sequence generated:{gene}")
    print(f"Utility score:{score}")


# inp("A,T,C,G", "ATGC", "1 8 1 0 4 0 5 2")
# inp("A,T,C,G", "GCAT", "2 3 1 8 8 8 1 1") -153
# inp("A,T,C,G", "CGAT", "1 5 0 7 2 2 7 1") -51




# ////////////////////////////////////////////////////////////////////////////////////////////////////////
# task2

def opt(NUC, cur_ch, desired, map_W, turn_max, a_val, b_val, bstr_idx=None, factor_b=None):
    if len(NUC) == 0:
        wei = map_W[:]
        if bstr_idx!=None and factor_b != None:
            for m in range(bstr_idx, len(wei)):
                wei[m] *= factor_b
        return calc(cur_ch, desired, wei), cur_ch

    best_chain = None
    if turn_max:
        top = -9999
        n = 0
        while n < len(NUC):
            letter = NUC[n]
            rem = NUC[:n] + NUC[n+1:]
            new_chain = cur_ch + letter
            updated_boost_pos = bstr_idx
            if letter == 'S' and bstr_idx == None and factor_b != None:
                updated_boost_pos = len(cur_ch)

            score, trial = opt(rem, new_chain, desired, map_W, False, a_val, b_val, updated_boost_pos, factor_b)
            if score > top:
                top = score
                best_chain = trial
            if score > a_val:
                a_val = score
            if b_val <= a_val:
                break
            n += 1
        return top, best_chain

    else:
        bottom = 9999
        n = 0
        selected = None
        while n < len(NUC):
            letter = NUC[n]
            rem = NUC[:n] + NUC[n+1:]
            new_chain = cur_ch + letter

            score, trial = opt(rem, new_chain, desired, map_W, True, a_val, b_val, bstr_idx, factor_b)
            if score < bottom:
                bottom = score
                selected = trial
            if score < b_val:
                b_val = score
            if b_val <= a_val:
                break
            n += 1
        return bottom, selected
def calc(build, target, map_W):
    SC= 0
    longest = max(len(build), len(target))
    for k in range(longest):
        if k < len(build): 
            gene_val = ord(build[k]) 
        else:
            gene_val = 0
        if k < len(target):
            target_val = ord(target[k]) 
        else:
            target_val = 0
        if k < len(map_W):
            w = map_W[k] 
        else:
            w = 1
        if gene_val >= target_val:
            diff = gene_val - target_val 
        else:
            diff = target_val - gene_val
        SC+= diff * w
    return -SC

def inp(gene_input, target_input, sid_input):
    sid_parts = []
    for part in sid_input.strip().split():
        if part.isdigit():
            sid_parts.append(int(part))

    P = gene_input.strip().split(',')
    target = target_input.strip()

    if len(sid_parts) >= len(target):
        weights = sid_parts[-len(target):]
    else:
        weights = [1] * (len(target) - len(sid_parts)) + sid_parts  

    base_P = []
    for gene in P:
        if gene != 'S':
            base_P.append(gene)

    base_score, base_seq = opt(base_P, '', target, weights, True, -9999, 9999)

    if 'S' not in P:
        P.append('S')

    if len(sid_parts) >= 2:
        boost = (sid_parts[0] * 10 + sid_parts[1]) / 100.0
    else:
        boost = 1.0
    boosted_score, boosted_seq = opt(P, '', target, weights, True, -9999, 9999, None, boost)

    if boosted_score > base_score:
        print("YES")
    else:
        print("NO")

    print("With special nucleotide")
    print(f"Best gene sequence generated: {boosted_seq},")
    print(f"Utility score:{boosted_score}")


inp("A,T,C,G", "ATGC", "1 8 1 0 4 0 5 2") 
inp("A,T,C,G", "GCAT", "2 3 1 8 8 8 1 1")  
inp("A,T,C,G", "CGAT", "1 5 0 7 2 2 7 1")  


