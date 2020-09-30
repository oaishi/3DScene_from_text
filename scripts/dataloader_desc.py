import random
import os
import torch
import torch.nn as nn

from torch.utils.data import Dataset, DataLoader
# from torchvision import transforms, utils
import pickle
# from transformers import TransfoXLTokenizer, TransfoXLModel

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(torch.cuda.is_available())


class ImageDataset(Dataset):

    def __init__(self, pickle_dir, object_max_len):
        
        self.pickle_dir = pickle_dir
        
        self.object_max_len = object_max_len
        
        self.object_list_len = 11
        
        import os

        onlyfiles = next(os.walk(pickle_dir))[2] #dir is your directory path as string
        print(len(onlyfiles))

        self.data_size = len(onlyfiles)
        
    def __len__(self):
        return self.data_size #99840 #

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
            
        pad_token = 16
            
        save_file_name = self.pickle_dir + str(int(idx))

        with open(save_file_name, 'rb') as outfile:
            self.data_items = pickle.load(outfile)
            self.data_items = self.data_items['desc_list']
#             print((data_items))    

        description = self.data_items["description"]
        
        color_list_index = torch.from_numpy(self.data_items["objects_color"])
        shape_list_index = torch.from_numpy(self.data_items["objects_shape"])
        size_list_index = torch.from_numpy(self.data_items["objects_size"])
        texture_list_index = torch.from_numpy(self.data_items["objects_material"])
        
        length = self.data_items["length"]
        
        if length < 10 :
            color_list_index[(length+1):].fill_(pad_token)
            shape_list_index[(length+1):].fill_(pad_token)
            size_list_index[(length+1):].fill_(pad_token)
            texture_list_index[(length+1):].fill_(pad_token)
        

        hidden_state = torch.tensor(self.data_items['hidden_state'], device=device)
        
        last_hidden = torch.tensor(self.data_items['last_hidden'], device=device)      
        
        
        return hidden_state, last_hidden, color_list_index.long(), shape_list_index.long(), size_list_index.long(), texture_list_index.long() , self.data_items["source"], description
    

class VideoDataset(Dataset):

    def __init__(self, pickle_dir, object_max_len):
        
        self.pickle_dir = pickle_dir
        
        self.object_max_len = object_max_len
        
        self.object_list_len = 11
        
        import os

        onlyfiles = next(os.walk(pickle_dir))[2] #dir is your directory path as string
        print(len(onlyfiles))

        self.data_size = len(onlyfiles)
        
    def __len__(self):
        return self.data_size #99840 #

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
            
        pad_token = 16
            
        save_file_name = self.pickle_dir + str(int(idx))

        with open(save_file_name, 'rb') as outfile:
            self.data_items = pickle.load(outfile)
            self.data_items = self.data_items['desc_list']
#             print((data_items))    

        description = self.data_items["description"]
        
        color_list_index = torch.from_numpy(self.data_items["objects_color"])
        shape_list_index = torch.from_numpy(self.data_items["objects_shape"])
        size_list_index = torch.from_numpy(self.data_items["objects_size"])
        texture_list_index = torch.from_numpy(self.data_items["objects_material"])
        motion_list_index = torch.from_numpy(self.data_items["objects_motion"])
        
        length = self.data_items["length"]
        
        if length < 10 :
            color_list_index[(length+1):].fill_(pad_token)
            shape_list_index[(length+1):].fill_(pad_token)
            size_list_index[(length+1):].fill_(pad_token)
            texture_list_index[(length+1):].fill_(pad_token)
            motion_list_index[(length+1):].fill_(pad_token)
        

        hidden_state = torch.tensor(self.data_items['hidden_state'], device=device)
        
        last_hidden = torch.tensor(self.data_items['last_hidden'], device=device)
        
        
        return hidden_state, last_hidden, color_list_index.long() , shape_list_index.long() , size_list_index.long() , texture_list_index.long() , motion_list_index.long() , self.data_items["source"], description
    

class CombinedDataset(Dataset):

    def __init__(self, pickle_dir_image, pickle_dir_video, object_max_len):
        
        self.pickle_dir_image = pickle_dir_image
        self.pickle_dir_video = pickle_dir_video
        
        self.object_max_len = object_max_len
        
        self.object_list_len = 11
        
        import os

        onlyfiles = next(os.walk(pickle_dir_image))[2] #dir is your directory path as string
        print(len(onlyfiles))

        self.data_size = len(onlyfiles)
        
    def __len__(self):
        return self.data_size #99840 #

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        
        seed = random.randint(0, 1)
        pad_token = 16  
        
        # fetch image
        if seed == 0:       
            save_file_name = self.pickle_dir_image + str(int(idx))
        # fetch video
        else:
            save_file_name = self.pickle_dir_video + str(int(idx))

        with open(save_file_name, 'rb') as outfile:
            self.data_items = pickle.load(outfile)
            self.data_items = self.data_items['desc_list']
#             print((data_items))    

        description = self.data_items["description"]
        
        color_list_index = torch.from_numpy(self.data_items["objects_color"])
        shape_list_index = torch.from_numpy(self.data_items["objects_shape"])
        size_list_index = torch.from_numpy(self.data_items["objects_size"])
        texture_list_index = torch.from_numpy(self.data_items["objects_material"])
        try:
            motion_list_index = torch.from_numpy(self.data_items["objects_motion"])
        except:
            t = (torch.empty(self.object_list_len).fill_(pad_token)).long()
            motion_list_index = torch.tensor(t)#, device=device)
           
        length = self.data_items["length"]
        
        if length < 10 :
            color_list_index[(length+1):].fill_(pad_token)
            shape_list_index[(length+1):].fill_(pad_token)
            size_list_index[(length+1):].fill_(pad_token)
            texture_list_index[(length+1):].fill_(pad_token)
            motion_list_index[(length+1):].fill_(pad_token)
        
        hidden_state = torch.tensor(self.data_items['hidden_state'], device=device)
        
        # image, hence padding needed
        if seed == 0: 
            val = (self.object_max_len - list(hidden_state.shape)[1])
            hidden_state = nn.ConstantPad2d((0, 0, 0, val), 0)(hidden_state)
        
        last_hidden = torch.tensor(self.data_items['last_hidden'], device=device)
                
        return hidden_state, last_hidden, color_list_index.long() , shape_list_index.long() , size_list_index.long() , texture_list_index.long() , motion_list_index.long() , self.data_items["source"], description
    
def getdataloader(type, batch_size,output_folder, video_folder = None):
    if type == "image":      
        MAX_LENGTH_WORD = 93
        description_set= ImageDataset(pickle_dir = output_folder, object_max_len = MAX_LENGTH_WORD)
    if type == "video":
        MAX_LENGTH_WORD = 110
        description_set= VideoDataset(pickle_dir = output_folder, object_max_len = MAX_LENGTH_WORD)
    if type == "combined":
        MAX_LENGTH_WORD = 110
        description_set= CombinedDataset(pickle_dir_image = output_folder,pickle_dir_video = video_folder, object_max_len = MAX_LENGTH_WORD)
    return DataLoader(description_set, batch_size=batch_size, shuffle=True, num_workers=0)
           
# getdataloader("image", 64,'../per_description_file/testC/')    
# output_folder = '../per_description_file/train/'
# description_set = DescriptionDataset(pickle_dir = output_folder)    
# dataloader = DataLoader(description_set, batch_size=64, shuffle=True, num_workers=0)

# dataiter = iter(dataloader)
# hidden_state, last_hidden, color_list_index , shape_list_index , size_list_index , texture_list_index , length = dataiter.next()
# print(color_list_index.shape)