import numpy as np
import re
import math
import yaml
import importlib


def read_rle(path):
    with open(path, "r") as f:
        clean_lines = []
        for line in f.readlines():
            if line[0] != '#':  # skip comments
                if line[0] == 'x':  # get header
                    header = line
                else:  # get pattern
                    clean_lines.append(line.replace("\n", ""))
                        
        clean_lines = "".join(clean_lines)
    
    # parse header
    shape_y, shape_x = re.findall('\d+', header)[:2]
    shape_y, shape_x = int(shape_y), int(shape_x)
    
    # generate pattern
    pattern = np.zeros((shape_x, shape_y), dtype=np.uint8)
    i, j = 0, 0
    it = 0
    possible_tokens = ['b', 'o', '$', '!']
    while len(clean_lines) > 0:
        next_tokens = [clean_lines.find(token) for token in possible_tokens]
        next_tokens = [10**100 if token == -1 else token for token in next_tokens]

        first_token = min(next_tokens)
        token_name = possible_tokens[next_tokens.index(first_token)]
        cell_increments = clean_lines[:first_token]
        cell_increments = 1 if cell_increments == '' else cell_increments

        if token_name == 'o':
            pattern[j, i:i + int(cell_increments)] = 1
            i += int(cell_increments)
        
        elif token_name == 'b':
            i += int(cell_increments)
        
        elif token_name == '$' or token_name == '!':
            j += int(cell_increments)
            i = 0
        
        clean_lines = clean_lines[first_token + 1:]
        
        it += 1
        if it > shape_x * shape_y + 1:
            break
            
    return pattern


def add_pattern_from_file(x, path, pos, angle=0, flip=(1, 1), centered=False):
    pattern = read_rle(path)
    return add_pattern(x, pattern, pos, angle, flip, centered)


def add_pattern_from_macro(x, kwargs, pos, angle=0, flip=(1, 1), centered=False):
    pattern = load_macro(**kwargs)
    return add_pattern(x, pattern, pos, angle, flip, centered)


def load_macro(name, kwargs=None, source='temple_macro', module_base='moebiusgol.macro'):
    module = f'{module_base}.{source}'
    m = importlib.import_module(module)
    kwargs = {} if kwargs is None else kwargs
    clazz = getattr(m, name, None)
    if clazz is not None:
        return clazz(**kwargs)
    else:
        raise RuntimeError


def add_pattern(x, pattern, pos, angle=0, flip=(1, 1), centered=False):
    pattern = np.rot90(pattern, angle)

    if centered:
        x_slice = slice(pos[0] - math.floor(pattern.shape[0] / 2), pos[0] + math.ceil(pattern.shape[0] / 2))
        y_slice = slice(pos[1] - math.floor(pattern.shape[1] / 2), pos[1] + math.ceil(pattern.shape[1] / 2))
    else:
        x_slice = slice(pos[0], pos[0] + pattern.shape[0])
        y_slice = slice(pos[1], pos[1] + pattern.shape[1])

    pattern = np.logical_or(pattern, x[x_slice, y_slice])
    x[x_slice, y_slice] = pattern[::flip[0], ::flip[1]]
    return x


def read_pattern_shape(path):
    pattern = read_rle(path)
    return pattern.shape


def basic_load(path):
    with open(path, 'r') as f:
        timeline = yaml.safe_load(f)

    return timeline
