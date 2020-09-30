import torch
import eval
import m_image
import m_video

from torch import optim
import torch.nn as nn
import warnings
warnings.filterwarnings("ignore")
import json

from transformers import TransfoXLTokenizer, TransfoXLModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(torch.cuda.is_available())

MAX_LENGTH = 11

color_dict = {0:"eos", 1:"any",  2:"gray", 3:"blue", 4:"green", 5:"brown", 6:"purple",
                          7:"cyan", 8:"yellow", 9:"red"}
        
size_dict = {0:"eos", 1:"any", 2:"large", 3:"small"}
        
shape_dict = {0:"eos", 1:"any", 2:"cube", 3:"cylinder", 4:"sphere"}
        
material_dict = {0:"eos", 1:"any", 2:"rubber", 3:"metal"}

motion_dict = {0:"eos", 1:"spinning", 2:"rocking", 3:"bouncing", 4:"still", 5:"moving"}

def Get_Embedding(description, object_max_len):
    
    tokenizer = TransfoXLTokenizer.from_pretrained('transfo-xl-wt103')
    pretrained_model = TransfoXLModel.from_pretrained('transfo-xl-wt103')
    
    hidden_state, _ = pretrained_model(torch.tensor(tokenizer.encode(description, add_special_tokens=True, 
                add_space_before_punct_symbol=True)).unsqueeze(0))
        
    last_hidden = hidden_state[-1][-1]#.view(1,1,-1)
    val = (object_max_len - list(hidden_state.shape)[1])


            # https://pytorch.org/docs/stable/nn.html#constantpad2d
    hidden_state = nn.ConstantPad2d((0, 0, 0, val), 0)(hidden_state)
    
    return hidden_state.view(1,object_max_len,-1), last_hidden.view(1,1,-1)
    

def predictsingle(type, description, decoder):
    
       
    if type == "image":
        MAX_LENGTH_WORD = 93
        hidden_state, last_hidden = Get_Embedding(description, MAX_LENGTH_WORD)
        color_list, size_list, shape_list, material_list, attentions = \
                    eval.image_evaluate(last_hidden, hidden_state, decoder)
    else:
        MAX_LENGTH_WORD = 110
        hidden_state, last_hidden = Get_Embedding(description, MAX_LENGTH_WORD)
        color_list, size_list, shape_list, material_list, motion_list, attentions = \
                    eval.video_evaluate(last_hidden, hidden_state, decoder)
        
#     print(color_list, size_list, shape_list, material_list)   
        
    length = (color_list.size())[1] 
#     print(length)

    all = {}
    objects = []
    

    for i in range(length):
        if shape_list[0][i].item() == 0 :
            break
            
        keys = {}
        keys["color_name"] = color_dict[color_list[0][i].item()]
        keys["size_name"] = size_dict[size_list[0][i].item()]
        keys["mat_name"] = material_dict[material_list[0][i].item()]
        keys["obj_name"] = shape_dict[shape_list[0][i].item()]
        
        if type != "image":
            keys["motion_name"] = motion_dict[motion_list[0][i].item()]
        
        objects.append(keys)
        
        

    all["objects"] = objects
    all["description"] = description 
    filename = "../output/generated_jsons/" + type  + "/" + str(0) + ".json"        

    with open(filename, "w") as write_file:
        json.dump(all, write_file,indent=2)        

    print(all)
    
def start_predict(type, description, checkpoint_file = None):
    hidden_size = 1024
    output_size_color = 10
    output_size_shape = 5
    output_size_mat = 4
    output_size_size = 4
    output_size_motion = 6

    if type == "image":
        attn_decoder1 = m_image.AttnDecoderRNN(hidden_size, output_size_color, output_size_shape, output_size_mat,
                 output_size_size, dropout_p=0.1).to(device)
    else:
        attn_decoder1 = m_video.AttnDecoderRNN(hidden_size, output_size_color, output_size_shape, output_size_mat,
                 output_size_size, output_size_motion, dropout_p=0.1).to(device)

    decoder_optimizer = optim.SGD(attn_decoder1.parameters(), lr=0.01)

    if checkpoint_file is not None:
        checkpoint = torch.load(checkpoint_file)
        attn_decoder1.load_state_dict(checkpoint['state_dict'])
        decoder_optimizer.load_state_dict(checkpoint['optimizer'])

    attn_decoder1.eval()
    predictsingle(type, description, attn_decoder1)

    
# start_predict("video", "A large spinning yellow shiny sphere." ,"model_weight_video/model_100_195")    