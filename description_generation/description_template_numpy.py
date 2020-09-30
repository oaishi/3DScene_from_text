import random
import numpy as np

texture_dict = { "metal" : "shiny", "rubber" : "matte"}
number_dict = { 1 : "one", 2 : "two", 3 : "three", 4 : "four", 5 : "five", 6 : "six", 7 : "seven",
               8 : "eight", 9 : "nine", 10 : "ten", 11 : "eleven", 12 : "twelve", 13 : "thirteen", 14 : "fourteen",
               15 : "fifteen", 16 : "sixteen", 17 : "seventeen", 18 : "eighteen", 19 : "nineteen", 20 : "twenty"}

max_object_length = 11
color_dict = {"eos":0, "any":1,  "gray":2, "blue":3, "green":4, "brown":5, "purple":6,
                          "cyan":7, "yellow":8, "red":9}
        
size_dict = {"eos":0, "any":1, "large":2, "small":3}
        
shape_dict = {"eos":0, "any":1, "cube":2, "cylinder":3, "sphere":4}
        
material_dict = {"eos":0, "any":1, "rubber":2, "metal":3}


#0:color_list , 1:shape_list , 2:size_list , 3:texture_list	   
#A large yellow shiny sphere, a large cyan shiny cylinder and a small gray matte sphere.
def simple_description(data_single):
    global texture_dict, max_object_length
    description = ''
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
    
    global color_dict, size_dict, shape_dict, material_dict

    for i in range(len(data_single)):
        description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['color'] + ' ' + texture_dict.get(data_single[i]['material']) + ' ' +  data_single[i]['shape'] + ', ' 
        objects_size[i] = size_dict[data_single[i]['size']]
        objects_color[i] = color_dict[data_single[i]['color']]
        objects_material[i] = material_dict[data_single[i]['material']]
        objects_shape[i] = shape_dict[data_single[i]['shape']]
    
#     print(objects)
    # to get rid of an extra comma, capitalize
    description = 'A' +  description[1:-2]  + '.' 
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")
    
    return objects_color, objects_size, objects_shape, objects_material, description

def simple_any_description(data_single):
    global texture_dict, max_object_length
    description = ''
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
    
    global color_dict, size_dict, shape_dict, material_dict

    for i in range(len(data_single)):
        seed = random.randint(1, 4)
        #leave_color
        if seed == 1:
            description += 'a ' + data_single[i]['size'] + ' ' + texture_dict.get(data_single[i]['material']) + ' ' +  data_single[i]['shape'] + ', ' 
            objects_size[i] = size_dict[data_single[i]['size']]
            objects_color[i] = color_dict['any']
            objects_material[i] = material_dict[data_single[i]['material']]
            objects_shape[i] = shape_dict[data_single[i]['shape']]
        #leave_size
        elif seed == 2:
            description += 'a ' + data_single[i]['color'] + ' ' + texture_dict.get(data_single[i]['material']) + ' ' +  data_single[i]['shape'] + ', ' 
            objects_size[i] = size_dict['any']
            objects_color[i] = color_dict[data_single[i]['color']]
            objects_material[i] = material_dict[data_single[i]['material']]
            objects_shape[i] = shape_dict[data_single[i]['shape']]
        #leave_texture
        elif seed == 3:
            description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['color'] + ' ' +  data_single[i]['shape'] + ', ' 
            objects_size[i] = size_dict[data_single[i]['size']]
            objects_color[i] = color_dict[data_single[i]['color']]
            objects_material[i] = material_dict['any']
            objects_shape[i] = shape_dict[data_single[i]['shape']]
        #leave_shape
        else:
            description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['color'] + ' ' + texture_dict.get(data_single[i]['material']) + ' object, ' 
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
    
    return objects_color, objects_size, objects_shape, objects_material, description

def there_any_description(data_single):
    global texture_dict, max_object_length
    global color_dict, size_dict, shape_dict, material_dict
    if len(data_single) > 1:
        description = 'There are '
    else:
        description = 'There is '
        
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
        
    for i in range(len(data_single)):
        seed = random.randint(1, 4)
        #leave_color
        if seed == 1:
            description += 'a ' + data_single[i]['size'] + ' ' + texture_dict.get(data_single[i]['material']) + ' ' +  data_single[i]['shape'] + ', ' 
            objects_size[i] = size_dict[data_single[i]['size']]
            objects_color[i] = color_dict['any']
            objects_material[i] = material_dict[data_single[i]['material']]
            objects_shape[i] = shape_dict[data_single[i]['shape']]
        #leave_size
        elif seed == 2:
            description += 'a ' + data_single[i]['color'] + ' ' + texture_dict.get(data_single[i]['material']) + ' ' +  data_single[i]['shape'] + ', ' 
            objects_size[i] = size_dict['any']
            objects_color[i] = color_dict[data_single[i]['color']]
            objects_material[i] = material_dict[data_single[i]['material']]
            objects_shape[i] = shape_dict[data_single[i]['shape']]
            
        #leave_texture
        elif seed == 3:
            description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['color'] + ' ' +  data_single[i]['shape'] + ', ' 
            objects_size[i] = size_dict[data_single[i]['size']]
            objects_color[i] = color_dict[data_single[i]['color']]
            objects_material[i] = material_dict['any']
            objects_shape[i] = shape_dict[data_single[i]['shape']]
            
        #leave_shape
        else:
            description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['color'] + ' ' + texture_dict.get(data_single[i]['material']) + ' object, ' 
            
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
        
    return objects_color, objects_size, objects_shape, objects_material, description

def draw_any_description(data_single):
    global texture_dict, max_object_length
    global color_dict, size_dict, shape_dict, material_dict
    description = 'Draw '
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
        
    for i in range(len(data_single)):
        seed = random.randint(1, 4)
        #leave_color
        if seed == 1:
            description += 'a ' + data_single[i]['size'] + ' ' + texture_dict.get(data_single[i]['material']) + ' ' +  data_single[i]['shape'] + ', ' 
            
            objects_size[i] = size_dict[data_single[i]['size']]
            objects_color[i] = color_dict['any']
            objects_material[i] = material_dict[data_single[i]['material']]
            objects_shape[i] = shape_dict[data_single[i]['shape']]
        #leave_size
        elif seed == 2:
            description += 'a ' + data_single[i]['color'] + ' ' + texture_dict.get(data_single[i]['material']) + ' ' +  data_single[i]['shape'] + ', ' 
            
            objects_size[i] = size_dict['any']
            objects_color[i] = color_dict[data_single[i]['color']]
            objects_material[i] = material_dict[data_single[i]['material']]
            objects_shape[i] = shape_dict[data_single[i]['shape']]
        #leave_texture
        elif seed == 3:
            description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['color'] + ' ' +  data_single[i]['shape'] + ', ' 
            
            objects_size[i] = size_dict[data_single[i]['size']]
            objects_color[i] = color_dict[data_single[i]['color']]
            objects_material[i] = material_dict['any']
            objects_shape[i] = shape_dict[data_single[i]['shape']]
        #leave_shape
        else:
            description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['color'] + ' ' + texture_dict.get(data_single[i]['material']) + ' object, ' 
            
            
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
        
    return objects_color, objects_size, objects_shape, objects_material, description

# There are a yellow metal large sphere, a cyan metal large cylinder, a gray rubber small sphere.
def there_are_description(data_single):
    if len(data_single) > 1:
        description = 'There are '
    else:
        description = 'There is '
        
    global max_object_length
    global color_dict, size_dict, shape_dict, material_dict
        
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int) 
    
    for i in range(len(data_single)):
        description += 'a ' + data_single[i]['color'] + ' ' + data_single[i]['material'] + ' ' + data_single[i]['size'] + ' ' + data_single[i]['shape'] + ', ' 
        objects_size[i] = size_dict[data_single[i]['size']]
        objects_color[i] = color_dict[data_single[i]['color']]
        objects_material[i] = material_dict[data_single[i]['material']]
        objects_shape[i] = shape_dict[data_single[i]['shape']]
    
    
    # to get rid of an extra comma
    description = description[:-2]+'.'
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")
        
    return objects_color, objects_size, objects_shape, objects_material, description

# There are a large yellow sphere of metal texture, a large cyan cylinder of
# metal texture and a small gray sphere of rubber texture.
def there_are_of_color_description(data_single):
    global texture_dict
    global color_dict, size_dict, shape_dict, material_dict
    if len(data_single) > 1:
        description = 'There are '
    else:
        description = 'There is '
        
    global max_object_length
        
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
        
    for i in range(len(data_single)):
        description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['color'] + ' ' + data_single[i]['shape'] + ' of '+ texture_dict.get(data_single[i]['material']) + ' texture' + ', ' 
        objects_size[i] = size_dict[data_single[i]['size']]
        objects_color[i] = color_dict[data_single[i]['color']]
        objects_material[i] = material_dict[data_single[i]['material']]
        objects_shape[i] = shape_dict[data_single[i]['shape']]
    
    # to get rid of an extra comma
    description = description[:-2]+'.' 
    
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")
        
    return objects_color, objects_size, objects_shape, objects_material, description

# There are a large sphere of yellow color and metal texture, a large cylinder of 
# cyan color and metal texture, a small sphere of gray color and rubber texture.
def there_are_of_description(data_single):
    global texture_dict
    global color_dict, size_dict, shape_dict, material_dict
    if len(data_single) > 1:
        description = 'There are '
    else:
        description = 'There is '
        
    global max_object_length
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
        
    for i in range(len(data_single)):
        description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['shape'] + ' of '+ data_single[i]['color'] + ' color and ' + texture_dict.get(data_single[i]['material']) + ' texture' + ', ' 
        objects_size[i] = size_dict[data_single[i]['size']]
        objects_color[i] = color_dict[data_single[i]['color']]
        objects_material[i] = material_dict[data_single[i]['material']]
        objects_shape[i] = shape_dict[data_single[i]['shape']]
    
    # to get rid of an extra comma
    description = description[:-2]+'.' 
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")
        
    return objects_color, objects_size, objects_shape, objects_material, description
    
# Draw a yellow metal large sphere, a cyan metal large cylinder, a gray rubber small sphere.
def draw_description(data_single):
    description = 'Draw '
    global max_object_length
    global color_dict, size_dict, shape_dict, material_dict
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)


    for i in range(len(data_single)):
        description += 'a ' + data_single[i]['color'] + ' ' + data_single[i]['material'] + ' ' + data_single[i]['size'] + ' ' + data_single[i]['shape'] + ', ' 
        objects_size[i] = size_dict[data_single[i]['size']]
        objects_color[i] = color_dict[data_single[i]['color']]
        objects_material[i] = material_dict[data_single[i]['material']]
        objects_shape[i] = shape_dict[data_single[i]['shape']]
    
    # to get rid of an extra comma
    description = description[:-2]+'.' 
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")

    return objects_color, objects_size, objects_shape, objects_material, description


def draw_of_color_description(data_single):
    global texture_dict
    global color_dict, size_dict, shape_dict, material_dict
    description = 'Draw '
    global max_object_length
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
        
    for i in range(len(data_single)):
        description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['color'] + ' colored ' + data_single[i]['shape'] + ' of '+ texture_dict.get(data_single[i]['material']) + ' texture' + ', ' 
        objects_size[i] = size_dict[data_single[i]['size']]
        objects_color[i] = color_dict[data_single[i]['color']]
        objects_material[i] = material_dict[data_single[i]['material']]
        objects_shape[i] = shape_dict[data_single[i]['shape']]
    
    # to get rid of an extra comma
    description = description[:-2]+'.' 
    
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")
        
    return objects_color, objects_size, objects_shape, objects_material, description

def draw_of_description(data_single):
    global texture_dict
    global color_dict, size_dict, shape_dict, material_dict
    description = 'Draw '
    global max_object_length
    objects_color = np.zeros(( max_object_length,), dtype=int)
    objects_size = np.zeros(( max_object_length,), dtype=int)
    objects_shape = np.zeros(( max_object_length,), dtype=int)
    objects_material = np.zeros(( max_object_length,), dtype=int)
        
    for i in range(len(data_single)):
        description += 'a ' + data_single[i]['size'] + ' ' + data_single[i]['shape'] + ' of '+ data_single[i]['color'] + ' color and ' + texture_dict.get(data_single[i]['material']) + ' texture' + ', ' 
        objects_size[i] = size_dict[data_single[i]['size']]
        objects_color[i] = color_dict[data_single[i]['color']]
        objects_material[i] = material_dict[data_single[i]['material']]
        objects_shape[i] = shape_dict[data_single[i]['shape']]
    
    # to get rid of an extra comma
    description = description[:-2]+'.' 
    
    # add and in place of the last comma
    try:
        idx = description.rindex(',')
        description = description[:idx] + ' and' + description[(idx+1):]
    except:
        print("only one object.")
        
    return objects_color, objects_size, objects_shape, objects_material, description

# There are 5 spheres, 2 cylinders, 3 cubes.
def only_object_count(data_single):
    global number_dict
    global color_dict, size_dict, shape_dict, material_dict
    description = ''
        
    num_sphere = 0
    num_cube = 0
    num_cylinder = 0
    for i in range(len(data_single)):
        if data_single[i]['shape'] == 'sphere':
            num_sphere += 1
        elif data_single[i]['shape'] == 'cylinder':
            num_cylinder += 1    
        else:
            num_cube += 1
            
    description_list = [] 
    objects = []
    obj_list_sphere = []
    obj_list_cube = []
    obj_list_cylinder = []
        
    if num_sphere != 0:
        keys = {}
        object_desc_sphere = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "sphere"}
        
        
        for itr in range(num_sphere):
            obj_list_sphere.append(object_desc_sphere)
        
        if num_sphere != 1:
            description_list.append( ' '+ number_dict.get(num_sphere) + ' spheres,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_sphere) + ' sphere,')
            
    if num_cylinder != 0:
        keys = {}
        object_desc_cylinder = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name' : "cylinder"}
        
        for itr in range(num_cylinder):
            obj_list_cylinder.append(object_desc_cylinder)
        
        if num_cylinder != 1:
            description_list.append(' '+ number_dict.get(num_cylinder) + ' cylinders,')
        else:
            description_list.append(' '+ number_dict.get(num_cylinder) + ' cylinder,')
        
    if num_cube != 0:
        keys = {}
        object_desc_cube = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name' : "cube"}
        
        for itr in range(num_cube):
            obj_list_cube.append(object_desc_cube)
            
            
        if num_cube != 1:
            description_list.append(' '+ number_dict.get(num_cube) + ' cubes,')
        else:    
            description_list.append(' '+ number_dict.get(num_cube) + ' cube,')
            
    # add randomness   
    random.shuffle(description_list) 
    
    
    for elem in description_list:
        description += elem
        if 'cube' in elem:
            objects.extend(obj_list_cube)
        elif 'sphere' in elem:
            objects.extend(obj_list_sphere)
        else:
            objects.extend(obj_list_cylinder)
    
          
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
        
    for i in range(len(objects)):
        objects_size[i] = size_dict[objects[i]['size_name']]
        objects_color[i] = color_dict[objects[i]['color_name']]
        objects_material[i] = material_dict[objects[i]['mat_name']]
        objects_shape[i] = shape_dict[objects[i]['obj_name']]
        
    return objects_color, objects_size, objects_shape, objects_material, description

# There are 5 spheres, 2 cylinders, 3 cubes.
def there_are_object_count(data_single):
    global number_dict
    global color_dict, size_dict, shape_dict, material_dict
    if len(data_single) > 1:
        description = 'There are'
    else:
        description = 'There is'
        
    num_sphere = 0
    num_cube = 0
    num_cylinder = 0
    for i in range(len(data_single)):
        if data_single[i]['shape'] == 'sphere':
            num_sphere += 1
        elif data_single[i]['shape'] == 'cylinder':
            num_cylinder += 1    
        else:
            num_cube += 1
            
    description_list = [] 
    objects = []
    obj_list_sphere = []
    obj_list_cube = []
    obj_list_cylinder = []
        
    if num_sphere != 0:
        keys = {}
        object_desc_sphere = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "sphere"}
        
        
        for itr in range(num_sphere):
            obj_list_sphere.append(object_desc_sphere)
        
        if num_sphere != 1:
            description_list.append( ' '+ number_dict.get(num_sphere) + ' spheres,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_sphere) + ' sphere,')
            
    if num_cylinder != 0:
        keys = {}
        object_desc_cylinder = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name' : "cylinder"}
        
        for itr in range(num_cylinder):
            obj_list_cylinder.append(object_desc_cylinder)
        
        if num_cylinder != 1:
            description_list.append(' '+ number_dict.get(num_cylinder) + ' cylinders,')
        else:
            description_list.append(' '+ number_dict.get(num_cylinder) + ' cylinder,')
        
    if num_cube != 0:
        keys = {}
        object_desc_cube = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name' : "cube"}
        
        for itr in range(num_cube):
            obj_list_cube.append(object_desc_cube)
            
            
        if num_cube != 1:
            description_list.append(' '+ number_dict.get(num_cube) + ' cubes,')
        else:    
            description_list.append(' '+ number_dict.get(num_cube) + ' cube,')
            
    # add randomness   
    random.shuffle(description_list) 
    
    
    for elem in description_list:
        description += elem
        if 'cube' in elem or 'cubes' in elem:
            objects.extend(obj_list_cube)
        elif 'sphere' in elem or 'spheres' in elem:
            objects.extend(obj_list_sphere)
        else:
            objects.extend(obj_list_cylinder)
    
    # to get rid of an extra comma
    description = description[:-1] + '.'
    
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
        
    for i in range(len(objects)):
        objects_size[i] = size_dict[objects[i]['size_name']]
        objects_color[i] = color_dict[objects[i]['color_name']]
        objects_material[i] = material_dict[objects[i]['mat_name']]
        objects_shape[i] = shape_dict[objects[i]['obj_name']]
        
    return objects_color, objects_size, objects_shape, objects_material, description

def draw_object_count(data_single):
    global number_dict
    global color_dict, size_dict, shape_dict, material_dict
    description = 'Draw'
        
    num_sphere = 0
    num_cube = 0
    num_cylinder = 0
    for i in range(len(data_single)):
        if data_single[i]['shape'] == 'sphere':
            num_sphere += 1
        elif data_single[i]['shape'] == 'cylinder':
            num_cylinder += 1    
        else:
            num_cube += 1
            
    description_list = [] 
    objects = []
    obj_list_sphere = []
    obj_list_cube = []
    obj_list_cylinder = []
        
    if num_sphere != 0:
        keys = {}
        object_desc_sphere = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "sphere"}
        
        
        for itr in range(num_sphere):
            obj_list_sphere.append(object_desc_sphere)
        
        if num_sphere != 1:
            description_list.append( ' '+ number_dict.get(num_sphere) + ' spheres,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_sphere) + ' sphere,')
            
    if num_cylinder != 0:
        keys = {}
        object_desc_cylinder = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name' : "cylinder"}
        
        for itr in range(num_cylinder):
            obj_list_cylinder.append(object_desc_cylinder)
        
        if num_cylinder != 1:
            description_list.append(' '+ number_dict.get(num_cylinder) + ' cylinders,')
        else:
            description_list.append(' '+ number_dict.get(num_cylinder) + ' cylinder,')
        
    if num_cube != 0:
        keys = {}
        object_desc_cube = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name' : "cube"}
        
        for itr in range(num_cube):
            obj_list_cube.append(object_desc_cube)
            
            
        if num_cube != 1:
            description_list.append(' '+ number_dict.get(num_cube) + ' cubes,')
        else:    
            description_list.append(' '+ number_dict.get(num_cube) + ' cube,')
            
    # add randomness   
    random.shuffle(description_list) 
    
    
    for elem in description_list:
        description += elem
        if 'cube' in elem or 'cubes' in elem:
            objects.extend(obj_list_cube)
        elif 'sphere' in elem or 'spheres' in elem:
            objects.extend(obj_list_sphere)
        else:
            objects.extend(obj_list_cylinder)
    
    # to get rid of an extra comma
    description = description[:-1] + '.' 
    
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
        
    for i in range(len(objects)):
        objects_size[i] = size_dict[objects[i]['size_name']]
        objects_color[i] = color_dict[objects[i]['color_name']]
        objects_material[i] = material_dict[objects[i]['mat_name']]
        objects_shape[i] = shape_dict[objects[i]['obj_name']]
        
    return objects_color, objects_size, objects_shape, objects_material, description

def paint_object_count(data_single):
    global number_dict
    global color_dict, size_dict, shape_dict, material_dict
    description = 'Paint'
        
    num_sphere = 0
    num_cube = 0
    num_cylinder = 0
    for i in range(len(data_single)):
        if data_single[i]['shape'] == 'sphere':
            num_sphere += 1
        elif data_single[i]['shape'] == 'cylinder':
            num_cylinder += 1    
        else:
            num_cube += 1
            
    description_list = [] 
    objects = []
    obj_list_sphere = []
    obj_list_cube = []
    obj_list_cylinder = []
        
    if num_sphere != 0:
        keys = {}
        object_desc_sphere = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name'  : "sphere"}
        
        
        for itr in range(num_sphere):
            obj_list_sphere.append(object_desc_sphere)
        
        if num_sphere != 1:
            description_list.append( ' '+ number_dict.get(num_sphere) + ' spheres,')
            
        else:
            description_list.append( ' '+ number_dict.get(num_sphere) + ' sphere,')
            
    if num_cylinder != 0:
        keys = {}
        object_desc_cylinder = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name' : "cylinder"}
        
        for itr in range(num_cylinder):
            obj_list_cylinder.append(object_desc_cylinder)
        
        if num_cylinder != 1:
            description_list.append(' '+ number_dict.get(num_cylinder) + ' cylinders,')
        else:
            description_list.append(' '+ number_dict.get(num_cylinder) + ' cylinder,')
        
    if num_cube != 0:
        keys = {}
        object_desc_cube = {'size_name' : "any",'color_name'  : "any",'mat_name' : "any",'obj_name' : "cube"}
        
        for itr in range(num_cube):
            obj_list_cube.append(object_desc_cube)
            
            
        if num_cube != 1:
            description_list.append(' '+ number_dict.get(num_cube) + ' cubes,')
        else:    
            description_list.append(' '+ number_dict.get(num_cube) + ' cube,')
            
    # add randomness   
    random.shuffle(description_list) 
    
    
    for elem in description_list:
        description += elem
        if 'cube' in elem or 'cubes' in elem:
            objects.extend(obj_list_cube)
        elif 'sphere' in elem or 'spheres' in elem:
            objects.extend(obj_list_sphere)
        else:
            objects.extend(obj_list_cylinder)
    
    # to get rid of an extra comma
    description = description[:-1] + '.' 
    
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
        
    for i in range(len(objects)):
        objects_size[i] = size_dict[objects[i]['size_name']]
        objects_color[i] = color_dict[objects[i]['color_name']]
        objects_material[i] = material_dict[objects[i]['mat_name']]
        objects_shape[i] = shape_dict[objects[i]['obj_name']]
        
    return objects_color, objects_size, objects_shape, objects_material, description
    
