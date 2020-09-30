import random
import numpy as np

texture_dict = { "metal" : "shiny", "rubber" : "matte"}
number_dict = { 1 : "one", 2 : "two", 3 : "three", 4 : "four", 5 : "five", 6 : "six", 7 : "seven",
               8 : "eight", 9 : "nine", 10 : "ten", 11 : "eleven", 12 : "twelve", 13 : "thirteen", 14 : "fourteen",
               15 : "fifteen", 16 : "sixteen", 17 : "seventeen", 18 : "eighteen", 19 : "nineteen", 20 : "twenty"}

max_object_length = 11
color_dict = {"eos":0, "any":1,  "gray":2, "blue":3, "green":4, "brown":5, "purple":6,
                          "cyan":7, "yellow":8, "red":9}

motion_detail_dict  = {"moving": "moving forward","spinning": "whirling", "rocking": "moving back and forth", "bouncing":"bouncing", "still":"stationary"}                          
        
size_dict = {"eos":0, "any":1, "large":2, "small":3}
        
shape_dict = {"eos":0, "any":1, "cube":2, "cylinder":3, "sphere":4}
        
material_dict = {"eos":0, "any":1, "rubber":2, "metal":3}

motion_dict = {"eos":0, "spinning":1, "rocking":2, "bouncing":3, "still":4, "moving": 5}


#0:color_list , 1:shape_list , 2:size_list , 3:texture_list	   
#A large yellow shiny sphere, a large cyan shiny cylinder and a small gray matte sphere.
def simple_description(data_single):
    global texture_dict, max_object_length
    description = ''
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
    objects_motion = np.zeros(( max_object_length,), dtype=int)
    
    global color_dict, size_dict, shape_dict, material_dict, motion_dict

    for i in range(len(data_single)):
        description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['motion'] + ' '+ data_single[i]['color'] + ' ' + texture_dict.get(data_single[i]['material']) + ' ' +  data_single[i]['shape'] + ', ' 
        objects_size[i] = size_dict[data_single[i]['size']]
        objects_color[i] = color_dict[data_single[i]['color']]
        objects_material[i] = material_dict[data_single[i]['material']]
        objects_shape[i] = shape_dict[data_single[i]['shape']]
        objects_motion[i] = motion_dict[data_single[i]['motion']]            
    
#     print(objects)
    # to get rid of an extra comma, capitalize
    description = 'A' +  description[1:-2]  + '.' 
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")
    
    return objects_color, objects_size, objects_shape, objects_material, objects_motion, description

def simple_is_description(data_single):
    global texture_dict, max_object_length, motion_detail_dict
    description = ''
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
    objects_motion = np.zeros(( max_object_length,), dtype=int)
    
    global color_dict, size_dict, shape_dict, material_dict, motion_dict

    for i in range(len(data_single)):
        description += 'a ' + data_single[i]['size'] + ' '+ data_single[i]['color'] + ' ' + texture_dict.get(data_single[i]['material']) + ' ' +  data_single[i]['shape'] + ' is ' + motion_detail_dict.get(data_single[i]['motion']) + ', ' 
        objects_size[i] = size_dict[data_single[i]['size']]
        objects_color[i] = color_dict[data_single[i]['color']]
        objects_material[i] = material_dict[data_single[i]['material']]
        objects_shape[i] = shape_dict[data_single[i]['shape']]
        objects_motion[i] = motion_dict[data_single[i]['motion']]            
    
#     print(objects)
    # to get rid of an extra comma, capitalize
    description = 'A' +  description[1:-2]  + '.' 
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")
    
    return objects_color, objects_size, objects_shape, objects_material, objects_motion, description

def simple_any_description(data_single):
    global texture_dict, max_object_length
    description = ''
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
    objects_motion = np.zeros(( max_object_length,), dtype=int)
    
    global color_dict, size_dict, shape_dict, material_dict, motion_dict

    for i in range(len(data_single)):
        objects_motion[i] = motion_dict[data_single[i]['motion']]
        seed = random.randint(1, 4)
        #leave_color
        if seed == 1:
            description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['motion'] + ' ' + texture_dict.get(data_single[i]['material']) + ' ' +  data_single[i]['shape'] + ', ' 
            objects_size[i] = size_dict[data_single[i]['size']]
            objects_color[i] = color_dict['any']
            objects_material[i] = material_dict[data_single[i]['material']]
            objects_shape[i] = shape_dict[data_single[i]['shape']]            
        #leave_size
        elif seed == 2:
            description += 'a ' + data_single[i]['motion'] + ' ' + data_single[i]['color'] + ' ' + texture_dict.get(data_single[i]['material']) + ' ' +  data_single[i]['shape'] + ', ' 
            objects_size[i] = size_dict['any']
            objects_color[i] = color_dict[data_single[i]['color']]
            objects_material[i] = material_dict[data_single[i]['material']]
            objects_shape[i] = shape_dict[data_single[i]['shape']]
        #leave_texture
        elif seed == 3:
            description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['motion'] + ' ' + data_single[i]['color'] + ' ' +  data_single[i]['shape'] + ', ' 
            objects_size[i] = size_dict[data_single[i]['size']]
            objects_color[i] = color_dict[data_single[i]['color']]
            objects_material[i] = material_dict['any']
            objects_shape[i] = shape_dict[data_single[i]['shape']]
        #leave_shape
        else:
            description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['motion'] + ' ' + data_single[i]['color'] + ' ' + texture_dict.get(data_single[i]['material']) + ' object, ' 
            objects_size[i] = size_dict[data_single[i]['size']]
            objects_color[i] = color_dict[data_single[i]['color']]
            objects_material[i] = material_dict[data_single[i]['material']]
            objects_shape[i] = shape_dict['any']
            
    # to get rid of an extra comma, capitalize
    
    description = 'A' +  description[1:-2]  + '.' 
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")
    
    return objects_color, objects_size, objects_shape, objects_material, objects_motion, description

def there_any_description(data_single):
    global texture_dict, max_object_length
    if len(data_single) > 1:
        description = 'There are '
    else:
        description = 'There is '
        
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
    objects_motion = np.zeros(( max_object_length,), dtype=int)
    
    global color_dict, size_dict, shape_dict, material_dict, motion_dict
        
    for i in range(len(data_single)):

        objects_motion[i] = motion_dict[data_single[i]['motion']]
        seed = random.randint(1, 4)
        #leave_color
        if seed == 1:
            description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['motion'] + ' ' + texture_dict.get(data_single[i]['material']) + ' ' +  data_single[i]['shape'] + ', ' 
            objects_size[i] = size_dict[data_single[i]['size']]
            objects_color[i] = color_dict['any']
            objects_material[i] = material_dict[data_single[i]['material']]
            objects_shape[i] = shape_dict[data_single[i]['shape']]
        #leave_size
        elif seed == 2:
            description += 'a ' + data_single[i]['motion'] + ' ' + data_single[i]['color'] + ' ' + texture_dict.get(data_single[i]['material']) + ' ' +  data_single[i]['shape'] + ', ' 
            objects_size[i] = size_dict['any']
            objects_color[i] = color_dict[data_single[i]['color']]
            objects_material[i] = material_dict[data_single[i]['material']]
            objects_shape[i] = shape_dict[data_single[i]['shape']]
            
        #leave_texture
        elif seed == 3:
            description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['motion'] + ' ' + data_single[i]['color'] + ' ' +  data_single[i]['shape'] + ', ' 
            objects_size[i] = size_dict[data_single[i]['size']]
            objects_color[i] = color_dict[data_single[i]['color']]
            objects_material[i] = material_dict['any']
            objects_shape[i] = shape_dict[data_single[i]['shape']]
            
        #leave_shape
        else:
            description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['motion'] + ' ' + data_single[i]['color'] + ' ' + texture_dict.get(data_single[i]['material']) + ' object, ' 
            
            objects_size[i] = size_dict[data_single[i]['size']]
            objects_color[i] = color_dict[data_single[i]['color']]
            objects_material[i] = material_dict[data_single[i]['material']]
            objects_shape[i] = shape_dict['any']
            
    # to get rid of an extra comma
    description = description[:-2]+' in the picture.'
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")
        
    return objects_color, objects_size, objects_shape, objects_material, objects_motion, description

def draw_any_description(data_single):
    global texture_dict, max_object_length
    description = 'Draw '
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
    objects_motion = np.zeros(( max_object_length,), dtype=int)
    
    global color_dict, size_dict, shape_dict, material_dict, motion_dict
        
    for i in range(len(data_single)):
        objects_motion[i] = motion_dict[data_single[i]['motion']]
        seed = random.randint(1, 4)
        #leave_color
        if seed == 1:
            description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['motion'] + ' ' + texture_dict.get(data_single[i]['material']) + ' ' +  data_single[i]['shape'] + ', ' 
            
            objects_size[i] = size_dict[data_single[i]['size']]
            objects_color[i] = color_dict['any']
            objects_material[i] = material_dict[data_single[i]['material']]
            objects_shape[i] = shape_dict[data_single[i]['shape']]
        #leave_size
        elif seed == 2:
            description += 'a ' + data_single[i]['motion'] + ' ' + data_single[i]['color'] + ' ' + texture_dict.get(data_single[i]['material']) + ' ' +  data_single[i]['shape'] + ', ' 
            
            objects_size[i] = size_dict['any']
            objects_color[i] = color_dict[data_single[i]['color']]
            objects_material[i] = material_dict[data_single[i]['material']]
            objects_shape[i] = shape_dict[data_single[i]['shape']]
        #leave_texture
        elif seed == 3:
            description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['motion'] + ' ' + data_single[i]['color'] + ' ' +  data_single[i]['shape'] + ', ' 
            
            objects_size[i] = size_dict[data_single[i]['size']]
            objects_color[i] = color_dict[data_single[i]['color']]
            objects_material[i] = material_dict['any']
            objects_shape[i] = shape_dict[data_single[i]['shape']]
        #leave_shape
        else:
            description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['motion'] + ' ' + data_single[i]['color'] + ' ' + texture_dict.get(data_single[i]['material']) + ' object, ' 
                        
            objects_size[i] = size_dict[data_single[i]['size']]
            objects_color[i] = color_dict[data_single[i]['color']]
            objects_material[i] = material_dict[data_single[i]['material']]
            objects_shape[i] = shape_dict['any']
            
    # to get rid of an extra comma
    description = description[:-2]+'.'
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")
        
    return objects_color, objects_size, objects_shape, objects_material, objects_motion, description

# There are a yellow metal large sphere, a cyan metal large cylinder, a gray rubber small sphere.
def there_are_description(data_single):
    if len(data_single) > 1:
        description = 'There are '
    else:
        description = 'There is '
        
    global max_object_length
        
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int) 
    objects_motion = np.zeros(( max_object_length,), dtype=int)
    
    global color_dict, size_dict, shape_dict, material_dict, motion_dict
    
    for i in range(len(data_single)):
        description += 'a ' + data_single[i]['color'] + ' ' + data_single[i]['motion'] + ' ' + data_single[i]['material'] + ' ' + data_single[i]['size'] + ' ' + data_single[i]['shape'] + ', ' 
        objects_size[i] = size_dict[data_single[i]['size']]
        objects_color[i] = color_dict[data_single[i]['color']]
        objects_material[i] = material_dict[data_single[i]['material']]
        objects_shape[i] = shape_dict[data_single[i]['shape']]
        objects_motion[i] = motion_dict[data_single[i]['motion']]
    
    
    # to get rid of an extra comma
    description = description[:-2]+'.'
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")
        
    return objects_color, objects_size, objects_shape, objects_material, objects_motion, description

# There are a large yellow sphere of metal texture, a large cyan cylinder of
# metal texture and a small gray sphere of rubber texture.
def there_are_of_color_description(data_single):
    global texture_dict
    if len(data_single) > 1:
        description = 'There are '
    else:
        description = 'There is '
        
    global max_object_length
        
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
    objects_motion = np.zeros(( max_object_length,), dtype=int)
    
    global color_dict, size_dict, shape_dict, material_dict, motion_dict
            
    for i in range(len(data_single)):
        description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['motion'] + ' ' + data_single[i]['color'] + ' ' + data_single[i]['shape'] + ' of '+ texture_dict.get(data_single[i]['material']) + ' texture' + ', ' 
        objects_size[i] = size_dict[data_single[i]['size']]
        objects_color[i] = color_dict[data_single[i]['color']]
        objects_material[i] = material_dict[data_single[i]['material']]
        objects_shape[i] = shape_dict[data_single[i]['shape']]
        objects_motion[i] = motion_dict[data_single[i]['motion']]
    
    # to get rid of an extra comma
    description = description[:-2]+'.' 
    
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")
        
    return objects_color, objects_size, objects_shape, objects_material, objects_motion, description

# There are a large sphere of yellow color and metal texture, a large cylinder of 
# cyan color and metal texture, a small sphere of gray color and rubber texture.
def there_are_of_description(data_single):
    global texture_dict
    if len(data_single) > 1:
        description = 'There are '
    else:
        description = 'There is '
        
    global max_object_length
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
    objects_motion = np.zeros(( max_object_length,), dtype=int)
    
    global color_dict, size_dict, shape_dict, material_dict, motion_dict
        
    for i in range(len(data_single)):
        description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['motion'] + ' ' + data_single[i]['shape'] + ' of '+ data_single[i]['color'] + ' color and ' + texture_dict.get(data_single[i]['material']) + ' texture' + ', ' 
        objects_size[i] = size_dict[data_single[i]['size']]
        objects_color[i] = color_dict[data_single[i]['color']]
        objects_material[i] = material_dict[data_single[i]['material']]
        objects_shape[i] = shape_dict[data_single[i]['shape']]
        objects_motion[i] = motion_dict[data_single[i]['motion']]
    
    # to get rid of an extra comma
    description = description[:-2]+'.' 
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")
        
    return objects_color, objects_size, objects_shape, objects_material, objects_motion, description

# Draw a yellow metal large sphere, a cyan metal large cylinder, a gray rubber small sphere.
def draw_description(data_single):
    description = 'Draw '
    global max_object_length
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
    objects_motion = np.zeros(( max_object_length,), dtype=int)
    
    global color_dict, size_dict, shape_dict, material_dict, motion_dict


    for i in range(len(data_single)):
        description += 'a ' + data_single[i]['motion']  + ' ' + data_single[i]['color'] + ' ' + data_single[i]['material'] + ' ' + data_single[i]['size'] + ' ' + data_single[i]['shape'] + ', ' 
        objects_size[i] = size_dict[data_single[i]['size']]
        objects_color[i] = color_dict[data_single[i]['color']]
        objects_material[i] = material_dict[data_single[i]['material']]
        objects_shape[i] = shape_dict[data_single[i]['shape']]
        objects_motion[i] = motion_dict[data_single[i]['motion']]
    
    # to get rid of an extra comma
    description = description[:-2]+'.' 
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")

    return objects_color, objects_size, objects_shape, objects_material, objects_motion, description

def draw_of_color_description(data_single):
    global texture_dict
    description = 'Draw '
    global max_object_length
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
    objects_motion = np.zeros(( max_object_length,), dtype=int)
    
    global color_dict, size_dict, shape_dict, material_dict, motion_dict
        
    for i in range(len(data_single)):
        description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['motion']  + ' ' + data_single[i]['color'] + ' colored ' + data_single[i]['shape'] + ' of '+ texture_dict.get(data_single[i]['material']) + ' texture' + ', ' 
        objects_size[i] = size_dict[data_single[i]['size']]
        objects_color[i] = color_dict[data_single[i]['color']]
        objects_material[i] = material_dict[data_single[i]['material']]
        objects_shape[i] = shape_dict[data_single[i]['shape']]
        objects_motion[i] = motion_dict[data_single[i]['motion']]
    
    # to get rid of an extra comma
    description = description[:-2]+'.' 
    
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")
        
    return objects_color, objects_size, objects_shape, objects_material, objects_motion, description

def draw_of_description(data_single):
    global texture_dict
    description = 'Draw '
    global max_object_length
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
    objects_motion = np.zeros(( max_object_length,), dtype=int)
    
    global color_dict, size_dict, shape_dict, material_dict, motion_dict
          
    for i in range(len(data_single)):
        description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['motion']  + ' ' + data_single[i]['shape'] + ' of '+ data_single[i]['color'] + ' color and ' + texture_dict.get(data_single[i]['material']) + ' texture' + ', ' 
        objects_size[i] = size_dict[data_single[i]['size']]
        objects_color[i] = color_dict[data_single[i]['color']]
        objects_material[i] = material_dict[data_single[i]['material']]
        objects_shape[i] = shape_dict[data_single[i]['shape']]
        objects_motion[i] = motion_dict[data_single[i]['motion']]
    
    # to get rid of an extra comma
    description = description[:-2]+'.' 
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")
        
    return objects_color, objects_size, objects_shape, objects_material, objects_motion, description

# There are 5 spheres, 2 cylinders, 3 cubes.
def only_object_count(data_single):
    global number_dict
    global color_dict, size_dict, shape_dict, material_dict, motion_dict
    description = ''
        
    num_rock = 0
    num_spin = 0
    num_bounce = 0
    num_move = 0
    num_still = 0
    for i in range(len(data_single)):
        if data_single[i]['motion'] == 'rocking':
            num_rock += 1
        elif data_single[i]['motion'] == 'spinning':
            num_spin += 1  
        elif data_single[i]['motion'] == 'bouncing':
            num_bounce += 1 
        elif data_single[i]['motion'] == 'moving':
            num_move += 1     
        else:
            num_still += 1
            
    description_list = [] 
    objects = []
    obj_list_rock = []
    obj_list_spin = []
    obj_list_bounce = []
    obj_list_move = []
    obj_list_still = []
        
    if num_rock != 0:
        keys = {}
        obj_desc_temp = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "any", "motion_name" : "rocking"}
        
        
        for itr in range(num_rock):
            obj_list_rock.append(obj_desc_temp)
        
        if num_rock != 1:
            description_list.append( ' '+ number_dict.get(num_rock) + ' rocking objects,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_rock) + ' rocking object,')
            
    if num_spin != 0:
        keys = {}
        obj_desc_temp = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "any", "motion_name" : "spinning"}
        
        
        for itr in range(num_spin):
            obj_list_spin.append(obj_desc_temp)
        
        if num_spin != 1:
            description_list.append( ' '+ number_dict.get(num_spin) + ' spinning objects,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_spin) + ' spinning object,')

    if num_bounce != 0:
        keys = {}
        obj_desc_temp = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "any", "motion_name" : "bouncing"}
        
        
        for itr in range(num_bounce):
            obj_list_bounce.append(obj_desc_temp)
        
        if num_bounce != 1:
            description_list.append( ' '+ number_dict.get(num_bounce) + ' bouncing objects,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_bounce) + ' bouncing object,')

    if num_move != 0:
        keys = {}
        obj_desc_temp = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "any", "motion_name" : "moving"}
        
        
        for itr in range(num_move):
            obj_list_move.append(obj_desc_temp)
        
        if num_move != 1:
            description_list.append( ' '+ number_dict.get(num_move) + ' moving objects,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_move) + ' moving object,')

    if num_still != 0:
        keys = {}
        obj_desc_temp = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "any", "motion_name" : "still"}
        
        
        for itr in range(num_still):
            obj_list_still.append(obj_desc_temp)
        
        if num_still != 1:
            description_list.append( ' '+ number_dict.get(num_still) + ' still objects,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_still) + ' still object,')
    # add randomness   
    random.shuffle(description_list) 
    
    
    for elem in description_list:
        description += elem
        if 'rocking' in elem:
            objects.extend(obj_list_rock)
        elif 'bouncing' in elem:
            objects.extend(obj_list_bounce)
        elif 'spinning' in elem:
            objects.extend(obj_list_spin)
        elif 'moving' in elem:
        	objects.extend(obj_list_move)
        else:
            objects.extend(obj_list_still)
    
          
    # to get rid of an extra comma
    description = description[1:-1] + '.' 
    description = description[:1].upper() + description[1:]
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")

    global max_object_length
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
    objects_motion = np.zeros(( max_object_length,), dtype=int)
        
    for i in range(len(objects)):
        objects_size[i] = size_dict[objects[i]['size_name']]
        objects_color[i] = color_dict[objects[i]['color_name']]
        objects_material[i] = material_dict[objects[i]['mat_name']]
        objects_shape[i] = shape_dict[objects[i]['obj_name']]
        objects_motion[i] = motion_dict[objects[i]['motion_name']]
        
    return objects_color, objects_size, objects_shape, objects_material, objects_motion, description

# There are 5 spheres, 2 cylinders, 3 cubes.
def there_are_object_count(data_single):
    global number_dict
    global color_dict, size_dict, shape_dict, material_dict
    if len(data_single) > 1:
        description = 'There are'
    else:
        description = 'There is'
        
    num_rock = 0
    num_spin = 0
    num_bounce = 0
    num_move = 0
    num_still = 0
    for i in range(len(data_single)):
        if data_single[i]['motion'] == 'rocking':
            num_rock += 1
        elif data_single[i]['motion'] == 'spinning':
            num_spin += 1  
        elif data_single[i]['motion'] == 'bouncing':
            num_bounce += 1
        elif data_single[i]['motion'] == 'moving':
            num_move += 1         
        else:
            num_still += 1
            
    description_list = [] 
    objects = []
    obj_list_rock = []
    obj_list_spin = []
    obj_list_bounce = []
    obj_list_move = []
    obj_list_still = []
        
    if num_rock != 0:
        keys = {}
        obj_desc_temp = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "any", "motion_name" : "rocking"}
        
        
        for itr in range(num_rock):
            obj_list_rock.append(obj_desc_temp)
        
        if num_rock != 1:
            description_list.append( ' '+ number_dict.get(num_rock) + ' rocking objects,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_rock) + ' rocking object,')

    if num_move != 0:
        keys = {}
        obj_desc_temp = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "any", "motion_name" : "moving"}
        
        
        for itr in range(num_move):
            obj_list_move.append(obj_desc_temp)
        
        if num_move != 1:
            description_list.append( ' '+ number_dict.get(num_move) + ' moving objects,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_move) + ' moving object,')
            
    if num_spin != 0:
        keys = {}
        obj_desc_temp = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "any", "motion_name" : "spinning"}
        
        
        for itr in range(num_spin):
            obj_list_spin.append(obj_desc_temp)
        
        if num_spin != 1:
            description_list.append( ' '+ number_dict.get(num_spin) + ' spinning objects,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_spin) + ' spinning object,')

    if num_bounce != 0:
        keys = {}
        obj_desc_temp = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "any", "motion_name" : "bouncing"}
        
        
        for itr in range(num_bounce):
            obj_list_bounce.append(obj_desc_temp)
        
        if num_bounce != 1:
            description_list.append( ' '+ number_dict.get(num_bounce) + ' bouncing objects,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_bounce) + ' bouncing object,')

    if num_still != 0:
        keys = {}
        obj_desc_temp = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "any", "motion_name" : "still"}
        
        
        for itr in range(num_still):
            obj_list_still.append(obj_desc_temp)
        
        if num_still != 1:
            description_list.append( ' '+ number_dict.get(num_still) + ' still objects,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_still) + ' still object,')
    # add randomness   
    random.shuffle(description_list) 
    
    
    for elem in description_list:
        description += elem
        if 'rocking' in elem:
            objects.extend(obj_list_rock)
        elif 'bouncing' in elem:
            objects.extend(obj_list_bounce)
        elif 'spinning' in elem:
            objects.extend(obj_list_spin)
        elif 'moving' in elem:
            objects.extend(obj_list_move)
        else:
            objects.extend(obj_list_still)
    
          
    # to get rid of an extra comma
    description = description[0:-1] + '.' 
    #description = description[:1].upper() + description[1:]
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")

    global max_object_length
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
    objects_motion = np.zeros(( max_object_length,), dtype=int)
        
    for i in range(len(objects)):
        objects_size[i] = size_dict[objects[i]['size_name']]
        objects_color[i] = color_dict[objects[i]['color_name']]
        objects_material[i] = material_dict[objects[i]['mat_name']]
        objects_shape[i] = shape_dict[objects[i]['obj_name']]
        objects_motion[i] = motion_dict[objects[i]['motion_name']]
        
    return objects_color, objects_size, objects_shape, objects_material, objects_motion, description

def draw_object_count(data_single):
    global number_dict
    global color_dict, size_dict, shape_dict, material_dict
    description = 'Draw'
        
    num_rock = 0
    num_spin = 0
    num_bounce = 0
    num_still = 0
    num_move = 0
    for i in range(len(data_single)):
        if data_single[i]['motion'] == 'rocking':
            num_rock += 1
        elif data_single[i]['motion'] == 'spinning':
            num_spin += 1  
        elif data_single[i]['motion'] == 'bouncing':
            num_bounce += 1
        elif data_single[i]['motion'] == 'moving':
            num_move += 1          
        else:
            num_still += 1
          
    description_list = [] 
    objects = []
    obj_list_rock = []
    obj_list_spin = []
    obj_list_bounce = []
    obj_list_still = []
    obj_list_move =  []
        
    if num_rock != 0:
        keys = {}
        obj_desc_temp = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "any", "motion_name" : "rocking"}
        
        
        for itr in range(num_rock):
            obj_list_rock.append(obj_desc_temp)
        
        if num_rock != 1:
            description_list.append( ' '+ number_dict.get(num_rock) + ' rocking objects,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_rock) + ' rocking object,')

    if num_move != 0:
        keys = {}
        obj_desc_temp = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "any", "motion_name" : "moving"}
        
        
        for itr in range(num_move):
            obj_list_move.append(obj_desc_temp)
        
        if num_move != 1:
            description_list.append( ' '+ number_dict.get(num_move) + ' moving objects,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_move) + ' moving object,')
            
    if num_spin != 0:
        keys = {}
        obj_desc_temp = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "any", "motion_name" : "spinning"}
        
        
        for itr in range(num_spin):
            obj_list_spin.append(obj_desc_temp)
        
        if num_spin != 1:
            description_list.append( ' '+ number_dict.get(num_spin) + ' spinning objects,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_spin) + ' spinning object,')

    if num_bounce != 0:
        keys = {}
        obj_desc_temp = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "any", "motion_name" : "bouncing"}
        
        
        for itr in range(num_bounce):
            obj_list_bounce.append(obj_desc_temp)
        
        if num_bounce != 1:
            description_list.append( ' '+ number_dict.get(num_bounce) + ' bouncing objects,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_bounce) + ' bouncing object,')

    if num_still != 0:
        keys = {}
        obj_desc_temp = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "any", "motion_name" : "still"}
        
        
        for itr in range(num_still):
            obj_list_still.append(obj_desc_temp)
        
        if num_still != 1:
            description_list.append( ' '+ number_dict.get(num_still) + ' still objects,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_still) + ' still object,')
    # add randomness   
    random.shuffle(description_list) 
    
    for elem in description_list:
        description += elem
        if 'rocking' in elem:
            objects.extend(obj_list_rock)
        elif 'bouncing' in elem:
            objects.extend(obj_list_bounce)
        elif 'spinning' in elem:
            objects.extend(obj_list_spin)
        elif 'moving' in elem:
            objects.extend(obj_list_move)
        else:
            objects.extend(obj_list_still)
    
          
    # to get rid of an extra comma
    description = description[0:-1] + '.' 
    #description = description[:1].upper() + description[1:]
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")

    global max_object_length
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
    objects_motion = np.zeros(( max_object_length,), dtype=int)

        
    for i in range(len(objects)):
        objects_size[i] = size_dict[objects[i]['size_name']]
        objects_color[i] = color_dict[objects[i]['color_name']]
        objects_material[i] = material_dict[objects[i]['mat_name']]
        objects_shape[i] = shape_dict[objects[i]['obj_name']]
        objects_motion[i] = motion_dict[objects[i]['motion_name']]
        
    return objects_color, objects_size, objects_shape, objects_material, objects_motion, description
