#!/usr/bin/env python3

from collections import deque
import sys, getopt

def main(argv):
    
    save_image = None
    rule_num = None
    gen_num = None
    init_conf = None
    fixed_b = False
    wrapped_b = False
    fixed_w = None
    wrapped_w = None
    user_input_error = False
    try:
        opts, args = getopt.getopt(argv[1:],"hi:r:o:g:",["fixedwidth=","wrapped="])
    except getopt.GetoptError:
        print("Type " + argv[0] + " -h for help")
        return
    for opt, arg in opts:
        if opt == '-h':
            print('\n')
            print(argv[0] + " will take an initial configuration for an elementary cellular automata, evolve it according to the given rule, and output the resultant simulation as an image.\n")
            print("Usage: " + argv[0] + " -i <initial configuration> -r <desired rule as an integer> -g <number of generations to compute> -o <name and path for output image> [--fixedwidth <width> --wrapped <width>]\n")
            print("-i: The initial configuration (generation 0) of the automata as a binary number. Must have odd length or will be extended.")
            print("-r: The rule for the cellular automata evolution as an integer from 0 to 255.")
            print("-g: Number of generations to evolve the automata. This will specify the height (in pixels) of the output image.")
            print("-o: Specify the name and location of the output image.")
            print("--fixedwidth: Force the output image to have the specified width (in pixels). The width must be an odd-numbered integer. If it is not odd it will be rounded up to the next odd number.")
            print("--wrapped: Make the grid have the specified width (in pixels) and wrap around instead of being infinite. The width must be an odd-numbered integer or it will be rounded up to the next odd number. Will override --fixedwidth.")
            print('\n')
            return
        elif opt == '-i':
            if arg is None or arg == '':
                print("Missing initial configuration.")
                return
            init_conf = arg
        elif opt == '-r':
            if arg is None or arg == '':
                print("Missing rule.")
                return
            rule_num = arg
        elif opt == '-o':
            if arg is None or arg == '':
                print("Missing output image location.")
                return
            save_image = arg
        elif opt == '-g':
            if arg is None or arg == '':
                print("Missing number of generations.")
                return
            gen_num = arg
        elif opt == '--fixedwidth':
            if arg is None or arg == '':
                print("Missing fixed width.")
                return
            fixed_b = True
            fixed_w = arg
        elif opt == '--wrapped':
            if arg is None or arg == '':
                print("Missing grid width.")
                return
            wrapped_b = True
            wrapped_w = arg
            
    if init_conf is None:
        print("Specify initial configuration.")
        user_input_error = True
        
    if rule_num is None:
        print("Specify rule number.")
        user_input_error = True
    
    if save_image is None:
        print("Specify output location.")
        user_input_error = True
        
    if gen_num is None:
        print("Specify number of generations.")
        user_input_error = True
        
    if user_input_error:
        return
    
    result_grid = None
    

    try:
        rule_num = int(rule_num)
    except ValueError as ve:
        print("Entered rule is not a valid integer.")
        return
        
    try:
        gen_num = int(gen_num)
    except ValueError as ve:
        print("Entered generation is not a valid integer.")
        return
    
    if rule_num < 0 or rule_num > 255:
        print("Entered rule is out of valid range (0-255).")
        return
    
    if len(init_conf) < 3:
        print("The initial configuration must contain at least 3 cells.")
        return
    
    if len(init_conf) % 2 == 0:
        init_conf += '0'
        
    for i in range(len(init_conf)):
        if init_conf[i] != '0' and init_conf[i] != '1':
            print("The initial configuration may only contain 0 or 1 as characters.")
            return
            
      
        
    
    if not wrapped_b:
        result_grid = generate_rule(gen_num, init_conf, rule_num)
    else:
        try:
            wrapped_w = int(wrapped_w)
        except ValueError as ve:
            print("Entered wrap width is not a valid integer.")
            return
        if wrapped_w % 2 == 0:
            wrapped_w += 1
        result_grid = generate_rule_wrap(gen_num, init_conf, rule_num, wrapped_w)
        
    if fixed_b and not wrapped_b:
        try:
            fixed_w = int(fixed_w)
        except ValueError as ve:
            print("Entered fixed width is not a valid integer.")
            return
        if fixed_w % 2 == 0:
            fixed_w += 1
        
        fix_width(result_grid, fixed_w)
    try:                
        to_image(result_grid, save_image)
    except ImportError:
        print("Missing required library Pillow (PIL).")
        return
    except IOError:
        print("Failed to write to file: ")
        print(save_image)
        return
    
def fix_width(grid, width):
    if width % 2 == 0:
        width += 1
        
    result_grid_gen = len(grid)
    result_grid_w = len(grid[0])
    for i in range(result_grid_gen):
        result_grid_w = len(grid[i])
        if result_grid_w > width:
            removes = int((result_grid_w - width)/2)
            for j in range(removes):
                grid[i].pop()
                grid[i].popleft()
            else:
                adds = int((width - result_grid_w)/2)
                for j in range(adds):
                    left_ext = grid[i][0]
                    right_ext = grid[i][-1]
                    grid[i].append(left_ext)
                    grid[i].appendleft(right_ext)
    return grid


def to_image(grid, path):
    from PIL import Image
    alwidth = len(grid[-1])
    gens = len(grid)
    al = [255 if x == 0 else 0 for y in grid for x in y ]
    auto_image = Image.new('1', (alwidth,gens))
    auto_image.putdata(al)
    auto_image.convert('RGB')
    auto_image.save(path, 'PNG')
        
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

def odd_rules(generations, initial_config, rule_num):
    rule_bin = bin(rule_num)[2:]
    RULE_BIT_LENGTH = 8
    
    if len(rule_bin) < RULE_BIT_LENGTH :
        add_bits = RULE_BIT_LENGTH - len(rule_bin)
        add_bit_string = '0'*add_bits
        rule_bin = add_bit_string + rule_bin
        
    if rule_bin[0] == '0':
        return odd_rules_0(generations, initial_config, rule_num)
    else:
        return odd_rules_1(generations, initial_config, rule_num)



def even_rules_wrap(generations, initial_config, rule_num, wrap_width):

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
    max_length = wrap_width
    
    
    
    for i in range(generations):

        if len(next_config) < wrap_width:
                
            if next_config[0] != 0 or next_config[1] != 0:
                next_config.extendleft([0,0])
                next_config.extend([0,0])
            if next_config[-1] != 0 or next_config[-2] != 0:
                next_config.extend([0,0])
                next_config.extendleft([0,0])
                
        while(len(next_config) > wrap_width):
            next_config.pop()
            next_config.popleft()
        

        auto_lattice.append(next_config)
            
        if i == generations - 1:
            break
            
        next_config = deque(list(next_config))
        cell_number = len(next_config)
        
        if cell_number < wrap_width:    
            for j in range(1, cell_number - 1):           
                left_cell = auto_lattice[i][j-1]
                right_cell = auto_lattice[i][j+1]
                current_cell = auto_lattice[i][j]
                next_config[j] = rule_little_endian[right_cell + 2*current_cell + 4*left_cell]
        else:
            for j in range(0, cell_number):           
                left_cell = auto_lattice[i][j-1]
                right_cell = auto_lattice[i][(j+1) % cell_number]
                current_cell = auto_lattice[i][j]
                next_config[j] = rule_little_endian[right_cell + 2*current_cell + 4*left_cell]           
        
        
    for i in range(len(auto_lattice)):
        current_length = len(auto_lattice[i])
        if current_length < max_length:
            length_difference = max_length - current_length
            extender_list = [0] * int(length_difference / 2)
            auto_lattice[i].extend(extender_list)
            auto_lattice[i].extendleft(extender_list)

    return auto_lattice

def odd_rules_1_wrap(generations, initial_config, rule_num, wrap_width):

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
    max_length = wrap_width
    
    if len(next_config) < wrap_width:
        if next_config[0] != 0 or next_config[1] != 0:
            next_config.extendleft([0,0])
            next_config.extend([0,0])
        if next_config[-1] != 0 or next_config[-2] != 0:
            next_config.extend([0,0])
            next_config.extendleft([0,0])

    while(len(next_config) > wrap_width):
        next_config.pop()
        next_config.popleft()
        
                
    auto_lattice.append(next_config)
        
     
        
    next_config = deque(list(next_config))
    cell_number = len(next_config)
        
    for j in range(0, cell_number):
        if j == 0:
            if cell_number < wrap_width:
                left_cell = 0
            else:
                left_cell = auto_lattice[0][-1]
        else:
            left_cell = auto_lattice[0][j-1]
        if j == cell_number - 1:
            if cell_number < wrap_width:
                right_cell = 0
            else:
                right_cell = auto_lattice[0][0]
        else:
            right_cell = auto_lattice[0][j+1]
        current_cell = auto_lattice[0][j]
        next_config[j] = rule_little_endian[right_cell + 2*current_cell + 4*left_cell]
    
    
    for i in range(1, generations):
        
        if len(next_config) < wrap_width:
            if next_config[0] != 1 or next_config[1] != 1:
                next_config.extendleft([1,1])
                next_config.extend([1,1])
            if next_config[-1] != 1 or next_config[-2] != 1:
                next_config.extend([1,1])
                next_config.extendleft([1,1])
                
        while(len(next_config) > wrap_width):
            next_config.pop()
            next_config.popleft()
        


        auto_lattice.append(next_config)
        
        if i == generations - 1:
            break
        
        next_config = deque(list(next_config))
        cell_number = len(next_config)
        
        for j in range(0, cell_number):
            left_cell = auto_lattice[i][j-1]
            right_cell = auto_lattice[i][(j+1) % cell_number]
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

def odd_rules_0_wrap(generations, initial_config, rule_num, wrap_width):

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
    max_length = wrap_width
    
    if len(next_config) < wrap_width:
        if next_config[0] != 0 or next_config[1] != 0:
            next_config.extendleft([0,0])
            next_config.extend([0,0])
        if next_config[-1] != 0 or next_config[-2] != 0:
            next_config.extend([0,0])
            next_config.extendleft([0,0])

    while(len(next_config) > wrap_width):
        next_config.pop()
        next_config.popleft()
                
    auto_lattice.append(next_config)
        
     
        
    next_config = deque(list(next_config))
    cell_number = len(next_config)
        
    for j in range(0, cell_number):
        if j == 0:
            if cell_number < wrap_width:
                left_cell = 0
            else:
                left_cell = auto_lattice[0][-1]
        else:
            left_cell = auto_lattice[0][j-1]
        if j == cell_number - 1:
            if cell_number < wrap_width:
                right_cell = 0
            else:
                right_cell = auto_lattice[0][0]
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
        
        if len(next_config) < wrap_width:
            if next_config[0] != fill_cell or next_config[1] != fill_cell:
                next_config.extendleft([fill_cell,fill_cell])
                next_config.extend([fill_cell,fill_cell])
            if next_config[-1] != fill_cell or next_config[-2] != fill_cell:
                next_config.extend([fill_cell,fill_cell])
                next_config.extendleft([fill_cell,fill_cell])
                
        while(len(next_config) > wrap_width):
            next_config.pop()
            next_config.popleft()
        
        auto_lattice.append(next_config)
        
        if i == generations - 1:
            break
        
        next_config = deque(list(next_config))
        cell_number = len(next_config)
        
        for j in range(0, cell_number):
            left_cell = auto_lattice[i][j-1]
            right_cell = auto_lattice[i][(j+1) % cell_number]
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

def odd_rules_wrap(generations, initial_config, rule_num, wrap_width):
    rule_bin = bin(rule_num)[2:]
    RULE_BIT_LENGTH = 8
    
    if len(rule_bin) < RULE_BIT_LENGTH :
        add_bits = RULE_BIT_LENGTH - len(rule_bin)
        add_bit_string = '0'*add_bits
        rule_bin = add_bit_string + rule_bin
        
    if rule_bin[0] == '0':
        return odd_rules_0_wrap(generations, initial_config, rule_num, wrap_width)
    else:
        return odd_rules_1_wrap(generations, initial_config, rule_num, wrap_width)
    
def generate_rule(generations, initial_config, rule_num):
    if rule_num % 2 == 0:
        return even_rules(generations, initial_config, rule_num)
    else:
        return odd_rules(generations, initial_config, rule_num)
    
def generate_rule_wrap(generations, initial_config, rule_num, wrap_width):
    if rule_num % 2 == 0:
        return even_rules_wrap(generations, initial_config, rule_num, wrap_width)
    else:
        return odd_rules_wrap(generations, initial_config, rule_num, wrap_width)
    

if __name__ == '__main__':
    main(sys.argv)

