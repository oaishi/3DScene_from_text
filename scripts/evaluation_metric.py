import torch
import eval

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(torch.cuda.is_available())

def image_evaluateAll(dataloader, decoder):
    
    total_acc_final = 0
    
    for iter, sample_batched in enumerate(dataloader):
        
        total_acc = 0
        
        hidden_state, last_hidden, color_list, shape_list, size_list, texture_list, length = sample_batched

        decoded_color, decoded_size, decoded_shape, decoded_material, attentions = \
                    eval.image_evaluate(last_hidden, hidden_state, decoder)
        
        Batch_size = hidden_state.size()[0]
        
        for i in range(0,Batch_size):
            
            running_acc_color = (decoded_color[i][:length[i]].eq(torch.tensor(color_list[i][:length[i]], device=device))).sum().item()
            running_acc_size = (decoded_size[i][:length[i]].eq(torch.tensor(size_list[i][:length[i]], device=device))).sum().item()
            running_acc_shape = (decoded_shape[i][:length[i]].eq(torch.tensor(shape_list[i][:length[i]], device=device))).sum().item()
            running_acc_mat = (decoded_material[i][:length[i]].eq(torch.tensor(texture_list[i][:length[i]], device=device))).sum().item()
            running_acc = running_acc_color+running_acc_size+running_acc_shape+running_acc_mat
            total_acc += 100*running_acc/(4*length[i].item())
            
#             print(decoded_material[i][:length[i]],texture_list[i][:length[i]],length[i],running_acc_mat)
        
        total_acc = total_acc/Batch_size
#         print(total_acc)
        total_acc_final += total_acc
        
        if (iter % 10)==0:
            print(total_acc)
#             break
        
    print('total_acc_final',total_acc_final/(iter+1),iter)
    
#     showAttention(color_list[0], decoded_color[0], attentions[0])
    
    return attentions, total_acc_final/(iter+1)


def video_evaluateAll(dataloader, decoder):
    
    total_acc_final = 0
    
    for iter, sample_batched in enumerate(dataloader):
        
        total_acc = 0
        
        hidden_state, last_hidden, color_list, shape_list, size_list, texture_list, motion_list, length = sample_batched

        decoded_color, decoded_size, decoded_shape, decoded_material, decoded_motion, attentions = \
                    eval.video_evaluate(last_hidden, hidden_state, decoder)
        
        Batch_size = hidden_state.size()[0]
        
#         print("new",iter)
        
        for i in range(0,Batch_size):
            
            running_acc_color = (decoded_color[i][:length[i]].eq(torch.tensor(color_list[i][:length[i]], device=device))).sum().item()
            running_acc_size = (decoded_size[i][:length[i]].eq(torch.tensor(size_list[i][:length[i]], device=device))).sum().item()
            running_acc_shape = (decoded_shape[i][:length[i]].eq(torch.tensor(shape_list[i][:length[i]], device=device))).sum().item()
            running_acc_mat = (decoded_material[i][:length[i]].eq(torch.tensor(texture_list[i][:length[i]], device=device))).sum().item()
            running_acc_motion = (decoded_motion[i][:length[i]].eq(torch.tensor(motion_list[i][:length[i]], device=device))).sum().item()
            running_acc = running_acc_color+running_acc_size+running_acc_shape+running_acc_mat+running_acc_motion
            total_acc += 100*running_acc/(5*length[i].item())
            
#             print(decoded_material[i][:length[i]],texture_list[i][:length[i]],length[i],running_acc_mat)
            print("mat", running_acc_mat, "shape",running_acc_shape, "motion", running_acc_motion, "size", running_acc_size,
                  "color", running_acc_color, "length", length[i])
        
        total_acc = total_acc/Batch_size
#         print(total_acc)
        total_acc_final += total_acc
        
        if (iter % 10)==0:
            print(total_acc)
#             break
        
    print('total_acc_final',total_acc_final/(iter+1),iter)
    
#     showAttention(color_list[0], decoded_color[0], attentions[0])
    
    return attentions, total_acc_final/(iter+1)

def combined_evaluateAll(dataloader, decoder):
    
    total_acc_final = 0
    
    pad_token = 16
    t = (torch.empty(11).fill_(pad_token)).long()
    
    for iter, sample_batched in enumerate(dataloader):
        
        total_acc = 0
        
        hidden_state, last_hidden, color_list, shape_list, size_list, texture_list, motion_list, length = sample_batched

        decoded_color, decoded_size, decoded_shape, decoded_material, decoded_motion, attentions = \
                    eval.video_evaluate(last_hidden, hidden_state, decoder)
        
        Batch_size = hidden_state.size()[0]
        
#         print("new",iter)
        
        for i in range(0,Batch_size):
            
            running_acc_color = (decoded_color[i][:length[i]].eq(torch.tensor(color_list[i][:length[i]], device=device))).sum().item()
            running_acc_size = (decoded_size[i][:length[i]].eq(torch.tensor(size_list[i][:length[i]], device=device))).sum().item()
            running_acc_shape = (decoded_shape[i][:length[i]].eq(torch.tensor(shape_list[i][:length[i]], device=device))).sum().item()
            running_acc_mat = (decoded_material[i][:length[i]].eq(torch.tensor(texture_list[i][:length[i]], device=device))).sum().item()
            
            # image
            if torch.all(motion_list[i].eq(t)).item():
                running_acc = running_acc_color+running_acc_size+running_acc_shape+running_acc_mat
                total_acc += 100*running_acc/(4*length[i].item())
            # video
            else:  
                running_acc_motion = (decoded_motion[i][:length[i]].eq(torch.tensor(motion_list[i][:length[i]], device=device))).sum().item()
                running_acc = running_acc_color+running_acc_size+running_acc_shape+running_acc_mat+running_acc_motion
                total_acc += 100*running_acc/(5*length[i].item())

#             print(decoded_material[i][:length[i]],texture_list[i][:length[i]],length[i],running_acc_mat)
        
        total_acc = total_acc/Batch_size
#         print(total_acc)
        total_acc_final += total_acc
        
        if (iter % 10)==0:
            print(total_acc)
#             break
        
    print('total_acc_final',total_acc_final/(iter+1),iter)
    
#     showAttention(color_list[0], decoded_color[0], attentions[0])
    
    return attentions, total_acc_final/(iter+1)   