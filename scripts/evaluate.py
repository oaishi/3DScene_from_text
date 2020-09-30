import m_image
import m_video
import evaluation_metric
import torch
from torch import optim
from dataloader import getdataloader

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(torch.cuda.is_available())

def start_eval(type, checkpoint_file = None):
    hidden_size = 1024
    output_size_color = 10
    output_size_shape = 5
    output_size_mat = 4
    output_size_size = 4
    output_size_motion = 6
    batch_size = 64

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
    
    if type == "image":   
        output_folder = '../per_description_file/testA/'   
        dataloader = getdataloader(type, batch_size,output_folder)
        evaluation_metric.image_evaluateAll(dataloader, attn_decoder1) 
    if type == "video":
        output_folder = '../per_video_file/testA/'    
        dataloader = getdataloader(type, batch_size,output_folder)
        evaluation_metric.video_evaluateAll(dataloader, attn_decoder1) 
    if type == "combined":
        output_folder = '../per_description_file/testA/'
        video_folder = '../per_video_file/testA/'    
        dataloader = getdataloader(type, batch_size,output_folder, video_folder)      
        evaluation_metric.combined_evaluateAll(dataloader, attn_decoder1) 

# start_eval("image", "model_weight_check/model_100_194")