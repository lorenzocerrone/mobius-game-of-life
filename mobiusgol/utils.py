import numpy as np
import glob
import re


def read_rle(path):
    with open(path, "r") as f:
        clean_lines = []
        for line in f.readlines():
            if line[0] != '#': # skip comments
                if line[0] == 'x': # get header
                    header = line
                else: # get pattern
                    clean_lines.append(line.replace("\n", ""))
                        
        clean_lines = "".join(clean_lines)
    
    # parse header
    shapey, shapex = re.findall('\d+', header)[:2]
    shapey, shapex = int(shapey), int(shapex)
    
    # generate pattern
    pattern = np.zeros((shapex, shapey), dtype=np.uint8)
    i, j = 0, 0
    it = 0
    possible_tokens = ['b', 'o', '$', '!']
    while len(clean_lines) > 0:
        #print(clean_lines)
        next_tokens = [clean_lines.find(token) for token in possible_tokens]
        next_tokens = [10**100 if token == -1 else token for token in next_tokens]
        #print(next_tokens)
        first_token = min(next_tokens)
        token_name = possible_tokens[next_tokens.index(first_token)]
        cell_increments = clean_lines[:first_token]
        
        cell_increments = 1 if cell_increments == '' else cell_increments
        #print(i, j, cell_increments)
        #print(token_name)
        if token_name == 'o':
            #print("- ", i, j, cell_increments)
            #print(pattern[j, i:i + int(cell_increments)])
            pattern[j, i:i + int(cell_increments)] = 1
            i += int(cell_increments)
        
        elif token_name == 'b':
            i += int(cell_increments)
        
        elif token_name == '$' or token_name == '!':
            j += int(cell_increments)
            i = 0
        
        clean_lines = clean_lines[first_token + 1:]
        
        it += 1
        if it > shapex * shapey + 1:
            break
            
    return pattern
