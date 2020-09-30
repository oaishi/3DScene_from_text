import pickle

with open('generic_description_video_trainA','rb') as file:
    data = pickle.load(file)
    data  = data['desc_list']

    max_len  = 0

    for i in data:
    	cur_len = len(i["description"].split())
    	if cur_len > max_len :
    		max_len = cur_len
print(max_len)

	
# highest count - 103

#{'yellow': 582518, 'cyan': 583634, 'gray': 581456, 'any': 1706222, 'blue': 578503, 'brown': 584260, 'green': 586887, 'red': 584885, 'purple': 581971} 
# {'large': 2208640, 'small': 2454956, 'any': 1706740} 
# {'sphere': 1565330, 'cylinder': 1553063, 'any': 1706545, 'cube': 1545398} 
# {'metal': 2327821, 'rubber': 2336662, 'any': 1705853} 
#{'moving': 1483300, 'still': 1487766, 'bouncing': 1491630, 'rocking': 1483006, 'spinning': 424634}