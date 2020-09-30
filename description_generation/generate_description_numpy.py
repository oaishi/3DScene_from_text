import description_template_numpy as description_template
import json
import pickle

with open('../CLEVR_CoGenT_v1.0_no_images/CLEVR_CoGenT_v1.0/scenes/CLEVR_valB_scenes.json', 'r') as f:
# with open('../CLEVR_v1.0_no_images/CLEVR_v1.0/scenes/CLEVR_train_scenes.json', 'r') as f:
# with open('../output/CLEVR_scenes.json', 'r') as f:
    data = json.load(f)
    print(len(data['scenes']))
    description_list = []
    for index in range(len(data['scenes'])):
        print(data['scenes'][index]['image_filename'])
        
        objects_color, objects_size, objects_shape, objects_material, description = description_template.simple_description(data['scenes'][index]['objects'])
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)
#         print(description)
#         print(objects)
        
        objects_color, objects_size, objects_shape, objects_material, description = description_template.there_any_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)
        
        objects_color, objects_size, objects_shape, objects_material, description = description_template.draw_any_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)
        
        objects_color, objects_size, objects_shape, objects_material, description = description_template.simple_any_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)
        
        objects_color, objects_size, objects_shape, objects_material, description = description_template.there_are_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)
        
        objects_color, objects_size, objects_shape, objects_material, description = description_template.there_are_of_color_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)
        
        objects_color, objects_size, objects_shape, objects_material, description = description_template.there_are_of_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)
        
        objects_color, objects_size, objects_shape, objects_material, description = description_template.draw_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)
        
        objects_color, objects_size, objects_shape, objects_material, description = description_template.draw_of_color_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)
        
        objects_color, objects_size, objects_shape, objects_material, description = description_template.draw_of_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)
        
        objects_color, objects_size, objects_shape, objects_material, description = description_template.draw_object_count(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)
        
        objects_color, objects_size, objects_shape, objects_material, description = description_template.there_are_object_count(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)
        
        objects_color, objects_size, objects_shape, objects_material, description = description_template.only_object_count(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)
        
        print('------------------------------------------------------------------------')
# print(description_list)  

desc_dict = {'desc_list': description_list}
# with open('generic_description.json', 'w') as json_file:
#     json.dump(description_list, json_file, indent = 4, sort_keys=True)

with open('generic_description_valB','wb') as outfile:
    pickle.dump(desc_dict,outfile)	