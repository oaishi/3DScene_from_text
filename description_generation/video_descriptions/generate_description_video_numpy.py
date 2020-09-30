import description_template_video_numpy as description_template
import json
import pickle

#with open('../CLEVR_CoGenT_v1.0_no_images/CLEVR_CoGenT_v1.0/scenes/CLEVR_trainA_scenes.json', 'r') as f:
# with open('../CLEVR_v1.0_no_images/CLEVR_v1.0/scenes/CLEVR_train_scenes.json', 'r') as f:
with open(r'CLEVR_trainA_videos.json', 'r') as f:
    data = json.load(f)
    print(len(data['scenes']))
    description_list = []
    for index in range(5):#(len(data['scenes'])):
        print(data['scenes'][index]['image_filename'])
        #print((data['scenes'][index]['objects']))
        
        objects_color, objects_size, objects_shape, objects_material, objects_motion, description = description_template.simple_description(data['scenes'][index]['objects'])
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["objects_motion"] = objects_motion
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)

        print(objects_color, objects_size, objects_shape, objects_material, objects_motion, description)
        
        
#         print(description)
#         print(objects)

        objects_color, objects_size, objects_shape, objects_material, objects_motion, description = description_template.simple_is_description(data['scenes'][index]['objects'])
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["objects_motion"] = objects_motion
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)

        print(objects_color, objects_size, objects_shape, objects_material, objects_motion, description)
#         print(description)
#         print(objects)
        
        objects_color, objects_size, objects_shape, objects_material, objects_motion, description = description_template.there_any_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["objects_motion"] = objects_motion
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)

        print(objects_color, objects_size, objects_shape, objects_material, objects_motion, description)

        
        objects_color, objects_size, objects_shape, objects_material, objects_motion, description = description_template.draw_any_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["objects_motion"] = objects_motion
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)

        print(objects_color, objects_size, objects_shape, objects_material, objects_motion, description)
        
        objects_color, objects_size, objects_shape, objects_material, objects_motion, description = description_template.simple_any_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["objects_motion"] = objects_motion
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)

        print(objects_color, objects_size, objects_shape, objects_material, objects_motion, description)

        
        objects_color, objects_size, objects_shape, objects_material, objects_motion, description = description_template.there_are_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["objects_motion"] = objects_motion
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)

        print(objects_color, objects_size, objects_shape, objects_material, objects_motion, description)

        
        objects_color, objects_size, objects_shape, objects_material, objects_motion, description = description_template.there_are_of_color_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["objects_motion"] = objects_motion
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)

        print(objects_color, objects_size, objects_shape, objects_material, objects_motion, description)

        
        objects_color, objects_size, objects_shape, objects_material, objects_motion, description = description_template.there_are_of_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["objects_motion"] = objects_motion
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)

        print(objects_color, objects_size, objects_shape, objects_material, objects_motion, description)

        
        objects_color, objects_size, objects_shape, objects_material, objects_motion, description = description_template.draw_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["objects_motion"] = objects_motion
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)

        print(objects_color, objects_size, objects_shape, objects_material, objects_motion, description)
        
        
        objects_color, objects_size, objects_shape, objects_material, objects_motion, description = description_template.draw_of_color_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["objects_motion"] = objects_motion
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)

        print(objects_color, objects_size, objects_shape, objects_material, objects_motion, description)

        
        objects_color, objects_size, objects_shape, objects_material, objects_motion, description = description_template.draw_of_description(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["objects_motion"] = objects_motion
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)

        print(objects_color, objects_size, objects_shape, objects_material, objects_motion, description)

        
        
        objects_color, objects_size, objects_shape, objects_material, objects_motion, description = description_template.draw_object_count(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["objects_motion"] = objects_motion
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)
        
        print(objects_color, objects_size, objects_shape, objects_material, objects_motion, description)
        

        objects_color, objects_size, objects_shape, objects_material, objects_motion, description = description_template.there_are_object_count(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["objects_motion"] = objects_motion
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)

        print(objects_color, objects_size, objects_shape, objects_material, objects_motion, description)

        
        
        objects_color, objects_size, objects_shape, objects_material, objects_motion, description = description_template.only_object_count(data['scenes'][index]['objects'])
#         print(description)
#         print(objects)
        keys = {}
        keys["source"] = data['scenes'][index]['image_filename']
        keys["objects_color"] = objects_color
        keys["objects_size"] = objects_size
        keys["objects_shape"] = objects_shape
        keys["objects_material"] = objects_material
        keys["objects_motion"] = objects_motion
        keys["description"] = description
        keys["length"] = len(data['scenes'][index]['objects'])
        description_list.append(keys)

        print(objects_color, objects_size, objects_shape, objects_material, objects_motion, description)
        
        
        print('------------------------------------------------------------------------')

        print(len(description_list))
# print(description_list)  

desc_dict = {'desc_list': description_list}
# with open('generic_description.json', 'w') as json_file:
#     json.dump(description_list, json_file, indent = 4, sort_keys=True)

with open('generic_description_video_dummy','wb') as outfile:
    pickle.dump(desc_dict,outfile)	