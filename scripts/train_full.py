import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
import numpy as np
import pickle

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(torch.cuda.is_available())

teacher_forcing_ratio = 0.5
MAX_LENGTH = 11

       
def train_full(target_tensor_color, target_tensor_shape, target_tensor_texture, target_tensor_size, target_tensor_motion, 
          encoder_hidden, encoder_outputs, length, decoder, decoder_optimizer, criterion_color,criterion_shape,
                  criterion_texture,criterion_size,criterion_motion, max_length=MAX_LENGTH, MAX_WORD_LENGTH=MAX_WORD_LENGTH):

    decoder_optimizer.zero_grad()

    target_length = length
    Batch_size = encoder_hidden.size()[0]
#     print(length)

   
    loss = 0
    correct = 0
    

    SOS_token = 15
    EOS_token = 0
 
    t = (torch.empty(Batch_size).fill_(SOS_token)).long()
    input_color = torch.tensor(t, device=device)
    input_shape = torch.tensor(t, device=device)
    input_size = torch.tensor(t, device=device)
    input_mat = torch.tensor(t, device=device)
    input_motion = torch.tensor(t, device=device)
    
    t = (torch.empty(Batch_size).fill_(EOS_token)).long()
    decoder_eos = torch.tensor(t, device=device)
    
    # encoder_hidden and encoder outputs will come from dataloader
    # print('inside-trainiter-hidden', encoder_hidden.size())
    decoder_hidden = torch.tensor(encoder_hidden.view(Batch_size,1,-1), device=device) # encoder_hidden
    cell_state = torch.zeros((1,Batch_size,1024), device=device)
    encoder_outputs = torch.tensor(encoder_outputs.view(Batch_size,MAX_WORD_LENGTH,-1), device=device)
#     print('inside-trainiter-all-hidden', encoder_outputs.size())

    use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False

    if use_teacher_forcing:
        # Teacher forcing: Feed the target as the next input
        for di in range(max_length):
            output_color, output_shape, output_material, output_size, output_motion, decoder_hidden, cell_state, decoder_attention = decoder(
                input_color, input_shape, input_size, input_mat, input_motion, decoder_hidden, cell_state, encoder_outputs)
         
            # print(target_tensor_color[:,di].size())
            # print(output_color.size())
            
            loss += criterion_color(output_color, torch.tensor(target_tensor_color[:,di], device=device))  
            loss += criterion_shape(output_shape, torch.tensor(target_tensor_shape[:,di], device=device))  
            loss += criterion_texture(output_material, torch.tensor(target_tensor_texture[:,di], device=device))
            loss += criterion_size(output_size, torch.tensor(target_tensor_size[:,di], device=device))  
            loss += criterion_motion(output_motion, torch.tensor(target_tensor_motion[:,di], device=device))  
            
            _, topi_color = output_color.topk(1)
            _, topi_shape = output_shape.topk(1)
            _, topi_material = output_material.topk(1)
            _, topi_size = output_size.topk(1)
            _, topi_motion = output_motion.topk(1)
            
            correct += (topi_color.eq(torch.tensor(target_tensor_color[:,di], device=device))).sum().item()
            correct += (topi_shape.eq(torch.tensor(target_tensor_shape[:,di], device=device))).sum().item()
            correct += (topi_material.eq(torch.tensor(target_tensor_texture[:,di], device=device))).sum().item()
            correct += (topi_size.eq(torch.tensor(target_tensor_size[:,di], device=device))).sum().item()
            correct += (topi_motion.eq(torch.tensor(target_tensor_motion[:,di], device=device))).sum().item()
            
            
            input_color, input_shape, input_size, input_mat, input_motion =  torch.tensor(target_tensor_color[:,di], device=device), \
                       torch.tensor(target_tensor_shape[:,di], device=device), \
                    torch.tensor(target_tensor_size[:,di], device=device), torch.tensor(target_tensor_texture[:,di], device=device), \
                       torch.tensor(target_tensor_motion[:,di], device=device)
            # Teacher forcing

    else:
        # Without teacher forcing: use its own predictions as the next input
        for di in range(max_length):
            output_color, output_shape, output_material, output_size, output_motion, decoder_hidden, cell_state, decoder_attention = decoder(
                input_color, input_shape, input_size, input_mat, input_motion, decoder_hidden, cell_state, encoder_outputs)
            
#             print(target_tensor_color.size())
#             print(output_color.size())
            
            _, topi_color = output_color.topk(1)
            _, topi_shape = output_shape.topk(1)
            _, topi_material = output_material.topk(1)
            _, topi_size = output_size.topk(1)
            _, topi_motion = output_motion.topk(1)
            
            correct += (topi_color.eq(torch.tensor(target_tensor_color[:,di], device=device))).sum().item()
            correct += (topi_shape.eq(torch.tensor(target_tensor_shape[:,di], device=device))).sum().item()
            correct += (topi_material.eq(torch.tensor(target_tensor_texture[:,di], device=device))).sum().item()
            correct += (topi_size.eq(torch.tensor(target_tensor_size[:,di], device=device))).sum().item()
            correct += (topi_motion.eq(torch.tensor(target_tensor_motion[:,di], device=device))).sum().item()
            
            input_color, input_shape, input_size, input_mat, input_motion = topi_color.squeeze().detach(), topi_shape.squeeze().detach(), \
                                topi_size.squeeze().detach(), topi_material.squeeze().detach(), topi_motion.squeeze().detach()

            # print(target_tensor_color[:,di].size())
            # print(output_color.size())
            
            loss += criterion_color(output_color, torch.tensor(target_tensor_color[:,di], device=device))  
            loss += criterion_shape(output_shape, torch.tensor(target_tensor_shape[:,di], device=device))  
            loss += criterion_texture(output_material, torch.tensor(target_tensor_texture[:,di], device=device))
            loss += criterion_size(output_size, torch.tensor(target_tensor_size[:,di], device=device))  
            loss += criterion_motion(output_motion, torch.tensor(target_tensor_motion[:,di], device=device))  
            
            
#             total = 4
#             print(100 * (correct/total))
            
            # if decoder_input.item() == EOS_token:
#             if torch.all(torch.eq(input_color, decoder_eos)) or torch.all(torch.eq(input_shape, decoder_eos)) or torch.all(torch.eq(input_size, decoder_eos)) or torch.all(torch.eq(input_mat, decoder_eos)):
#                 break

    loss.backward()

    decoder_optimizer.step()

    return loss.item() / (5*target_length*Batch_size) , correct / (5*target_length*Batch_size)

def trainIters(dataloader, decoder, decoder_optimizer,n_iters, print_every=50, plot_every=100, learning_rate=0.01, save_every =130):
    print_loss_total = 0  # Reset every print_every
    
    print_acc_total = 0

    weight_color = torch.tensor([1.0,0.32,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0], device=device)
    weight_shape = torch.tensor([1.0,1.67,1.0,1.0,1.0], device=device)
    weight_size = torch.tensor([1.0,1.37,1.0,1.0], device=device)
    weight_mat = torch.tensor([1.0,1.3,1.0,1.0], device=device)
    weight_motion = torch.tensor([1.0,3.5,1.0,1.0,1.0,1.0], device=device)
    
    pad_token = 16
    
    criterion_color = nn.NLLLoss(weight_color, ignore_index=pad_token)
    criterion_shape = nn.NLLLoss(weight_shape, ignore_index=pad_token)
    criterion_texture = nn.NLLLoss(weight_mat, ignore_index=pad_token)
    criterion_size = nn.NLLLoss(weight_size, ignore_index=pad_token)
    criterion_motion = nn.NLLLoss(weight_motion, ignore_index=pad_token)

    for epoch in range(0, n_iters + 1):
        for iter, sample_batched in enumerate(dataloader):
        
            hidden_state, last_hidden, color_list, shape_list, size_list, texture_list, motion_list, length = sample_batched

            loss, acc = train_full(color_list, shape_list, texture_list, size_list, motion_list,
                  last_hidden, hidden_state, length, decoder, decoder_optimizer, criterion_color, criterion_shape,
                  criterion_texture, criterion_size, criterion_motion, max_length=MAX_LENGTH)

            loss = torch.mean(loss.double())
            acc = torch.mean(acc.double())

            # print('loss_size',loss.size())

            print_loss_total += loss
            print_acc_total += acc

            if iter % print_every == 0:
                print_loss_avg = print_loss_total / print_every
                print_loss_total = 0

                print_acc_avg = print_acc_total / print_every
                print_acc_total = 0
                print('%s (%d %d%%)' % (timeSince(start, iter / n_iters),
                                             iter, iter / n_iters * 100))
                # print('Epoch [{}/{}], Step [{}], Loss: {}, Accuracy: {}'.format(epoch, epochs, i, loss.item(), train_acc))
                print('Loss: {}, Running_Loss: {}'.format(print_loss_avg,loss))
                print('Accuracy: {}, Running_Accuracy: {}'.format(print_acc_avg,acc))

        state = {
            'iter': iter,
            'epoch': epoch,
            'state_dict': decoder.state_dict(),
            'optimizer': decoder_optimizer.state_dict(),
            'current_loss': print_loss_avg
        }
    #             model_save_path = os.path.join(self.model_dir, 'model_%d' % (iter))
    #                 with open('model_tracker.txt', 'w') as f:
    #                     f.write(model_save_path)
    #                     print('model saved at:', model_save_path)
        torch.save(state, 'model_weight_comb/model_%d_%d' % (epoch, iter))

#     showPlot(plot_losses)