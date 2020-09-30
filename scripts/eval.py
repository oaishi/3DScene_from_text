import torch

MAX_LENGTH = 11

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(torch.cuda.is_available())

def image_evaluate(encoder_hidden, encoder_outputs, decoder, max_length=MAX_LENGTH):
    with torch.no_grad():
        
        SOS_token = 15
        EOS_token = 0

        Batch_size = encoder_hidden.size()[0]

        t = (torch.empty(Batch_size).fill_(SOS_token)).long()
        input_color = torch.tensor(t, device=device)
        input_shape = torch.tensor(t, device=device)
        input_size = torch.tensor(t, device=device)
        input_mat = torch.tensor(t, device=device)

        t = (torch.empty(Batch_size).fill_(EOS_token)).long()
        decoder_eos = torch.tensor(t, device=device)
               
        decoder_hidden = torch.tensor(encoder_hidden.view(Batch_size,1,-1), device=device) # encoder_hidden
        cell_state = torch.zeros((1,Batch_size,1024), device=device)
        encoder_outputs = torch.tensor(encoder_outputs.view(Batch_size,93,-1), device=device)

        decoded_color = torch.zeros((Batch_size,max_length), device=device)
        decoded_size = torch.zeros((Batch_size,max_length), device=device)
        decoded_shape = torch.zeros((Batch_size,max_length), device=device)
        decoded_material = torch.zeros((Batch_size,max_length), device=device)
        decoder_attentions = []

         
        for di in range(max_length):
            
            output_color, output_shape, output_material, output_size, decoder_hidden, cell_state, decoder_attention = decoder(
                input_color, input_shape, input_size, input_mat, decoder_hidden, cell_state, encoder_outputs)
            
#             print(decoder_attention.data.size())
            
#             decoder_attentions[:,di,:] = decoder_attention.data
            decoder_attentions.append(decoder_attention.data)
            
            _, topi_color = output_color.topk(1)
            _, topi_shape = output_shape.topk(1)
            _, topi_material = output_material.topk(1)
            _, topi_size = output_size.topk(1)
            
            input_color, input_shape, input_size, input_mat = topi_color.squeeze().detach(), topi_shape.squeeze().detach(), \
                                topi_size.squeeze().detach(), topi_material.squeeze().detach()
            
            decoded_color[:,di]=input_color
            decoded_size[:,di]=input_size
            decoded_shape[:,di]=input_shape
            decoded_material[:,di]=input_mat
            
            
            if torch.all(torch.eq(input_color, decoder_eos)) or torch.all(torch.eq(input_shape, decoder_eos)) or torch.all(torch.eq(input_size, decoder_eos)) or torch.all(torch.eq(input_mat, decoder_eos)):
                   break
                

        return decoded_color.long(), decoded_size.long(), decoded_shape.long(), decoded_material.long(), decoder_attentions
    

def video_evaluate(encoder_hidden, encoder_outputs, decoder, max_length=MAX_LENGTH):
    with torch.no_grad():
        
        SOS_token = 15
        EOS_token = 0

        Batch_size = encoder_hidden.size()[0]

        t = (torch.empty(Batch_size).fill_(SOS_token)).long()
        input_color = torch.tensor(t, device=device)
        input_shape = torch.tensor(t, device=device)
        input_size = torch.tensor(t, device=device)
        input_mat = torch.tensor(t, device=device)
        input_motion = torch.tensor(t, device=device)

        t = (torch.empty(Batch_size).fill_(EOS_token)).long()
        decoder_eos = torch.tensor(t, device=device)
               
        decoder_hidden = torch.tensor(encoder_hidden.view(Batch_size,1,-1), device=device) # encoder_hidden
        cell_state = torch.zeros((1,Batch_size,1024), device=device)
        encoder_outputs = torch.tensor(encoder_outputs.view(Batch_size,110,-1), device=device)

        decoded_color = torch.zeros((Batch_size,max_length), device=device)
        decoded_size = torch.zeros((Batch_size,max_length), device=device)
        decoded_shape = torch.zeros((Batch_size,max_length), device=device)
        decoded_material = torch.zeros((Batch_size,max_length), device=device)
        decoded_motion = torch.zeros((Batch_size,max_length), device=device)
        decoder_attentions = []

         
        for di in range(max_length):
            
            
            output_color, output_shape, output_material, output_size, output_motion, decoder_hidden, cell_state, decoder_attention = decoder(
                input_color, input_shape, input_size, input_mat, input_motion, decoder_hidden, cell_state, encoder_outputs)
         
            
#             print(decoder_attention.data.size())
            
#             decoder_attentions[:,di,:] = decoder_attention.data
            decoder_attentions.append(decoder_attention.data)
            
            _, topi_color = output_color.topk(1)
            _, topi_shape = output_shape.topk(1)
            _, topi_material = output_material.topk(1)
            _, topi_size = output_size.topk(1)
            _, topi_motion = output_motion.topk(1)
            
            input_color, input_shape, input_size, input_mat, input_motion = topi_color.squeeze().detach(), topi_shape.squeeze().detach(), \
                                topi_size.squeeze().detach(), topi_material.squeeze().detach(), topi_motion.squeeze().detach()

            decoded_color[:,di]=input_color
            decoded_size[:,di]=input_size
            decoded_shape[:,di]=input_shape
            decoded_material[:,di]=input_mat
            decoded_motion[:,di]=input_motion
            
            
            if torch.all(torch.eq(input_color, decoder_eos)) or torch.all(torch.eq(input_shape, decoder_eos)) or torch.all(torch.eq(input_size, decoder_eos)) or torch.all(torch.eq(input_mat, decoder_eos)):
                   break
                

        return decoded_color.long(), decoded_size.long(), decoded_shape.long(), decoded_material.long(), decoded_motion.long(), decoder_attentions