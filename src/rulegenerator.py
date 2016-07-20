from collections import deque
from PIL import Image

def even_rules(generations, initial_config, rule_num):

    rule_bin = bin(rule_num)[2:]
    RULE_BIT_LENGTH = 8
    
    if len(rule_bin) < RULE_BIT_LENGTH :
        add_bits = RULE_BIT_LENGTH - len(rule_bin)
        add_bit_string = '0'*add_bits
        rule_bin = add_bit_string + rule_bin
    
    rule_little_endian = [int(x) for x in rule_bin[::-1]]   
    
    initial_config_arr = deque([int(initial_config[x]) for x in range(len(initial_config)) ])
    
    next_config = initial_config_arr
    
    if len(next_config) == 0:
        next_config.append(0)
    
    if not ( len(next_config) > 1 ):
        next_config.append(0)
        next_config.appendleft(0)
    
    auto_lattice = list()
    max_length = 0
    
    
    
    for i in range(generations):
        
        if next_config[0] != 0 or next_config[1] != 0:
            next_config.extendleft([0,0])
            next_config.extend([0,0])
        if next_config[-1] != 0 or next_config[-2] != 0:
            next_config.extend([0,0])
            next_config.extendleft([0,0])
    
    
        if max_length < len(next_config):
            max_length = len(next_config)
                
        auto_lattice.append(next_config)
        
        if i == generations - 1:
            break
        
        next_config = deque(list(next_config))
        cell_number = len(next_config)
        
        for j in range(1, cell_number - 1):
            left_cell = auto_lattice[i][j-1]
            right_cell = auto_lattice[i][j+1]
            current_cell = auto_lattice[i][j]
            next_config[j] = rule_little_endian[right_cell + 2*current_cell + 4*left_cell]
            
    for i in range(len(auto_lattice)):
        current_length = len(auto_lattice[i])
        if current_length < max_length:
            length_difference = max_length - current_length
            extender_list = [0] * int(length_difference / 2)
            auto_lattice[i].extend(extender_list)
            auto_lattice[i].extendleft(extender_list)
    
    '''
    auto_lattice = [x for y in auto_lattice for x in y ]
    '''
    return auto_lattice
    
    '''
    
    auto_image = Image.new('1', (max_length,generations))
    auto_image.putdata(auto_lattice)
    auto_image.convert('RGB')
    auto_image.save('../test/testimg6.png', 'PNG')
    
    '''

def odd_rules_1(generations, initial_config, rule_num):

    rule_bin = bin(rule_num)[2:]
    RULE_BIT_LENGTH = 8
    
    if len(rule_bin) < RULE_BIT_LENGTH :
        add_bits = RULE_BIT_LENGTH - len(rule_bin)
        add_bit_string = '0'*add_bits
        rule_bin = add_bit_string + rule_bin
    
    rule_little_endian = [int(x) for x in rule_bin[::-1]]   
    
    initial_config_arr = deque([int(initial_config[x]) for x in range(len(initial_config)) ])
    
    next_config = initial_config_arr
    
    if len(next_config) == 0:
        next_config.append(0)
    
    if not ( len(next_config) > 1 ):
        next_config.append(0)
        next_config.appendleft(0)
    
    auto_lattice = list()
    max_length = 0
    
    if next_config[0] != 0 or next_config[1] != 0:
        next_config.extendleft([0,0])
        next_config.extend([0,0])
    if next_config[-1] != 0 or next_config[-2] != 0:
        next_config.extend([0,0])
        next_config.extendleft([0,0])
    
    
    if max_length < len(next_config):
        max_length = len(next_config)
                
    auto_lattice.append(next_config)
        
     
        
    next_config = deque(list(next_config))
    cell_number = len(next_config)
        
    for j in range(0, cell_number):
        if j == 0:
            left_cell = 0
        else:
            left_cell = auto_lattice[0][j-1]
        if j == cell_number - 1:
            right_cell = 0
        else:
            right_cell = auto_lattice[0][j+1]
        current_cell = auto_lattice[0][j]
        next_config[j] = rule_little_endian[right_cell + 2*current_cell + 4*left_cell]
    
    
    for i in range(1, generations):
        
        if next_config[0] != 1 or next_config[1] != 1:
            next_config.extendleft([1,1])
            next_config.extend([1,1])
        if next_config[-1] != 1 or next_config[-2] != 1:
            next_config.extend([1,1])
            next_config.extendleft([1,1])
    
    
        if max_length < len(next_config):
            max_length = len(next_config)
                
        auto_lattice.append(next_config)
        
        if i == generations - 1:
            break
        
        next_config = deque(list(next_config))
        cell_number = len(next_config)
        
        for j in range(1, cell_number - 1):
            left_cell = auto_lattice[i][j-1]
            right_cell = auto_lattice[i][j+1]
            current_cell = auto_lattice[i][j]
            next_config[j] = rule_little_endian[right_cell + 2*current_cell + 4*left_cell]
            
    
    current_length = len(auto_lattice[0])
    if current_length < max_length:
        length_difference = max_length - current_length
        extender_list = [0] * int(length_difference / 2)
        auto_lattice[0].extend(extender_list)
        auto_lattice[0].extendleft(extender_list)
            
    
            
    for i in range(1, len(auto_lattice)):
        current_length = len(auto_lattice[i])
        if current_length < max_length:
            length_difference = max_length - current_length
            extender_list = [1] * int(length_difference / 2)
            auto_lattice[i].extend(extender_list)
            auto_lattice[i].extendleft(extender_list)
     
    return auto_lattice

def odd_rules_0(generations, initial_config, rule_num):

    rule_bin = bin(rule_num)[2:]
    RULE_BIT_LENGTH = 8
    
    if len(rule_bin) < RULE_BIT_LENGTH :
        add_bits = RULE_BIT_LENGTH - len(rule_bin)
        add_bit_string = '0'*add_bits
        rule_bin = add_bit_string + rule_bin
    
    rule_little_endian = [int(x) for x in rule_bin[::-1]]   
    
    initial_config_arr = deque([int(initial_config[x]) for x in range(len(initial_config)) ])
    
    next_config = initial_config_arr
    
    if len(next_config) == 0:
        next_config.append(0)
    
    if not ( len(next_config) > 1 ):
        next_config.append(0)
        next_config.appendleft(0)
    
    auto_lattice = list()
    max_length = 0
    
    if next_config[0] != 0 or next_config[1] != 0:
        next_config.extendleft([0,0])
        next_config.extend([0,0])
    if next_config[-1] != 0 or next_config[-2] != 0:
        next_config.extend([0,0])
        next_config.extendleft([0,0])
    
    
    if max_length < len(next_config):
        max_length = len(next_config)
                
    auto_lattice.append(next_config)
        
     
        
    next_config = deque(list(next_config))
    cell_number = len(next_config)
        
    for j in range(0, cell_number):
        if j == 0:
            left_cell = 0
        else:
            left_cell = auto_lattice[0][j-1]
        if j == cell_number - 1:
            right_cell = 0
        else:
            right_cell = auto_lattice[0][j+1]
        current_cell = auto_lattice[0][j]
        next_config[j] = rule_little_endian[right_cell + 2*current_cell + 4*left_cell]
        
    fill_cell = 0
    
    for i in range(1, generations):
        
        if i % 2 == 0:
            fill_cell = 0
        else:
            fill_cell = 1
        
        if next_config[0] != fill_cell or next_config[1] != fill_cell:
            next_config.extendleft([fill_cell,fill_cell])
            next_config.extend([fill_cell,fill_cell])
        if next_config[-1] != fill_cell or next_config[-2] != fill_cell:
            next_config.extend([fill_cell,fill_cell])
            next_config.extendleft([fill_cell,fill_cell])
    
    
        if max_length < len(next_config):
            max_length = len(next_config)
                
        auto_lattice.append(next_config)
        
        if i == generations - 1:
            break
        
        next_config = deque(list(next_config))
        cell_number = len(next_config)
        
        for j in range(0, cell_number):
            if j == 0:
                left_cell = fill_cell
            else:
                left_cell = auto_lattice[i][j-1]
            if j == cell_number - 1:
                right_cell = fill_cell
            else:
                right_cell = auto_lattice[i][j+1]
            current_cell = auto_lattice[i][j]
            next_config[j] = rule_little_endian[right_cell + 2*current_cell + 4*left_cell]
            
    
    current_length = len(auto_lattice[0])
    if current_length < max_length:
        length_difference = max_length - current_length
        extender_list = [0] * int(length_difference / 2)
        auto_lattice[0].extend(extender_list)
        auto_lattice[0].extendleft(extender_list)
            
    
    extender_cell = 0   
    for i in range(1, len(auto_lattice)):
        if i % 2 == 0:
            extender_cell = 0
        else:
            extender_cell = 1
        current_length = len(auto_lattice[i])
        if current_length < max_length:
            length_difference = max_length - current_length
            extender_list = [extender_cell] * int(length_difference / 2)
            auto_lattice[i].extend(extender_list)
            auto_lattice[i].extendleft(extender_list)
     
    return auto_lattice




gens = 1000
al = odd_rules_0(gens, '010', 101)
alwidth = len(al[-1])
al = [255 if x == 0 else 0 for y in al for x in y ]
    
auto_image = Image.new('1', (alwidth,gens))
auto_image.putdata(al)
auto_image.convert('RGB')
auto_image.save('../test/testimg18.png', 'PNG')
