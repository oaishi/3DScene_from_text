import pickle

max_object_length = 11
color_dict = {0:"eos", 1:"any",  2:"gray", 3:"blue", 4:"green", 5:"brown", 6:"purple",
                          7:"cyan", 8:"yellow", 9:"red"}
        
size_dict = {0:"eos", 1:"any", 2:"large", 3:"small"}
        
shape_dict = {0:"eos", 1:"any", 2:"cube", 3:"cylinder", 4:"sphere"}
        
material_dict = {0:"eos", 1:"any", 2:"rubber", 3:"metal"}

motion_dict = {0:"eos", 1:"spinning", 2:"rocking", 3:"bouncing", 4:"still", 5:"moving"}

key_color,key_motion,key_shape,key_material,key_size={},{},{},{},{}

with open('generic_description_video_trainA','rb') as file:
    data = pickle.load(file)
    data  = data['desc_list']

    for keys in data:

        max_len = keys["length"] 

        for j in range(max_len):
            try:
                key_color[color_dict[keys["objects_color"][j]]] += 1
            except:
                key_color[color_dict[keys["objects_color"][j]]] = 1

            try:
                key_size[size_dict[keys["objects_size"][j]]] += 1
            except:
                key_size[size_dict[keys["objects_size"][j]]] = 1

            try:
                key_shape[shape_dict[keys["objects_shape"][j]]] += 1
            except:
                key_shape[shape_dict[keys["objects_shape"][j]]] = 1

            try:
                key_material[material_dict[keys["objects_material"][j]]] += 1
            except:
                key_material[material_dict[keys["objects_material"][j]]] = 1

            try:
                key_motion[motion_dict[keys["objects_motion"][j]]] += 1
            except:
                key_motion[motion_dict[keys["objects_motion"][j]]] = 1
    	
print(key_color,key_size,key_shape,key_material,key_motion)

# highest count - 103