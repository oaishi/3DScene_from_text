import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(torch.cuda.is_available())

MAX_WORD_LENGTH = 93
BATCH_SIZE = 512

class AttnDecoderRNN(nn.Module):
    def __init__(self, hidden_size, output_size_color, output_size_shape, output_size_mat,
                 output_size_size, dropout_p=0.1, max_length=MAX_WORD_LENGTH,batch_size= BATCH_SIZE):
        super(AttnDecoderRNN, self).__init__()
        self.hidden_size = hidden_size
        self.output_size_color = output_size_color
        self.output_size_shape = output_size_shape
        self.output_size_mat = output_size_mat
        self.output_size_size = output_size_size
        self.batch_size = batch_size
        self.output_size = 20
        self.dropout_p = dropout_p
        self.max_length = max_length

        self.embedding_color = nn.Embedding(self.output_size, hidden_size//4)
        self.embedding_shape = nn.Embedding(self.output_size, hidden_size//4)
        self.embedding_mat = nn.Embedding(self.output_size, hidden_size//4)
        self.embedding_size = nn.Embedding(self.output_size, hidden_size//4)
        
        self.linear_all_output = nn.Linear(self.hidden_size, self.hidden_size)
        self.linear_hidden = nn.Linear(self.hidden_size, self.hidden_size)
        self.attn = nn.Linear(self.hidden_size, 1)
#         self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.dropout = nn.Dropout(self.dropout_p)
        self.lstm = nn.LSTM(self.hidden_size, self.hidden_size, batch_first=True)
        self.out_color = nn.Linear(self.hidden_size, self.output_size_color)
        self.out_shape = nn.Linear(self.hidden_size, self.output_size_shape)
        self.out_material = nn.Linear(self.hidden_size, self.output_size_mat)
        self.out_size = nn.Linear(self.hidden_size, self.output_size_size)

    def forward(self, input_color, input_shape, input_size, input_mat, hidden, cell_state, encoder_outputs):
        
        self.batch_size = encoder_outputs.size()[0]

        # print("inside-train-input", input_color.size())
        embedded_color = self.embedding_color(input_color).view(1, self.batch_size, 1, -1)
        embedded_color = self.dropout(embedded_color)
        
        embedded_shape = self.embedding_shape(input_shape).view(1, self.batch_size, 1, -1)
        embedded_shape = self.dropout(embedded_shape)
        
        embedded_size = self.embedding_size(input_size).view(1, self.batch_size, 1, -1)
        embedded_size = self.dropout(embedded_size)
        
        embedded_mat = self.embedding_mat(input_mat).view(1, self.batch_size, 1, -1)
        embedded_mat = self.dropout(embedded_mat)
        
        # print('embedding-layer-output-size', embedded_color.size(), embedded_shape.size(), embedded_size.size(), embedded_mat.size())
        
        embedded = torch.cat((embedded_color[0], embedded_shape[0], embedded_size[0], embedded_mat[0]), 2)
                       
        hidden = self.linear_hidden(hidden.view(self.batch_size,1,-1))
        encoder_outputs = self.linear_all_output(encoder_outputs)
        
        # print('concated-size-hidden-size', embedded.size(), hidden.size())
        # hidden: batch_sizex1x1024, encoder_outputs: batch_sizex93x1024
        
        attn_align = F.tanh((hidden + encoder_outputs))    
        
        # attn_weights: batch_sizex1x93
        attn_weights = F.softmax((self.attn(attn_align)).view(self.batch_size, 1, -1) , dim=-1)
# #         print('attn_weights',attn_weights.size())
        
#         print('attn-weights', attn_weights.size(), encoder_outputs.size())
                   
        # attn_applied: batch_sizex1x1024          
        attn_applied = torch.bmm(attn_weights, encoder_outputs) #.unsqueeze(0))

        output = embedded + attn_applied
        
        # print('gru-check', output.size(), hidden.view(1,self.batch_size,-1).size())
        
        output, (hidden, cell_state) = self.lstm(output, (hidden.view(1,self.batch_size,-1), cell_state))

        output = output.view(self.batch_size,-1)

        # print('post-gru-check', output.size(), hidden.size())

        #dim (python:int) – A dimension along which log_softmax will be computed
        output_color = F.log_softmax(self.out_color(output), dim=1)
        output_shape = F.log_softmax(self.out_shape(output), dim=1)
        output_material = F.log_softmax(self.out_material(output), dim=1)
        output_size = F.log_softmax(self.out_size(output), dim=1)        
        
        return output_color, output_shape, output_material, output_size, hidden, cell_state, attn_weights   