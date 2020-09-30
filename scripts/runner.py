import argparse, json, os
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument('--type', default='image', help= "select which model you want to work on.")
parser.add_argument('--sector', default='predict', help ="select whether you want to evaluate, predict or train.")
parser.add_argument('--target', default='none', help ="select which you want to render")
parser.add_argument('--pred_count', default=1, type= int, help = "how many testpoint you want to work on.")
parser.add_argument('--description', default="A large spinning yellow shiny sphere.", help = "description you want to run prediction on.")
parser.add_argument('--view', default=0, type= int, help = "view the last rendered scene.")


def main(args):
    cur_dir = os.getcwd()
    
    if args.sector  == 'predict':
    
        print("starting prediction")
        from predict_precalculated import start_predict
        if args.type == 'video':
            start_predict(args.type, args.pred_count, os.getcwd()+ "/model_weight_video/model_120_195")
        elif args.type == 'image': 
            start_predict(args.type, args.pred_count, os.getcwd()+ "/model_weight_check/model_120_194")
        else:
            start_predict(args.type, args.pred_count, os.getcwd()+ "/model_weight_comb/model_120_195")
    
        print("prediction done")
        
    if args.sector  == 'predict_single':
        
        print("starting prediction")
        from predict import start_predict
        args.pred_count = 1
        if args.type == 'video':
            start_predict(args.type, args.description, os.getcwd()+ "/model_weight_video/model_120_195")
        elif args.type == 'image': 
            start_predict(args.type, args.description, os.getcwd()+ "/model_weight_check/model_120_194")
        else:
            start_predict(args.type, args.description, os.getcwd()+ "/model_weight_comb/model_120_195")
        
        print("prediction done")
        
        
    if args.sector  == 'evaluate':
        
        print("starting evaluation")
        from evaluate import start_eval
        if args.type == 'video':
            start_eval(args.type, os.getcwd()+ "/model_weight_video/model_120_195")
        elif args.type == 'image': 
            start_eval(args.type, os.getcwd()+ "/model_weight_check/model_120_194")
        else:
            start_eval(args.type, os.getcwd()+ "/model_weight_comb/model_120_195")
        
        print("evaluation done")
        
    if args.target != 'none':
    
        output_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) 
        json_dir = output_dir + '/output/generated_jsons/' + args.type + '/testA/'    
        vid_str = ' --output_image_dir "/output/video_dir/testA/videos/" --output_scene_dir "/output/video_dir/testA/scenes_vid/" --output_scene_file "../output/video_dir/testA/CLEVR_scenes_vid.json" '
        img_str = ' --output_image_dir "/output/image_dir/testA/images/" --output_scene_dir "/output/image_dir/testA/scenes_img/" --output_scene_file "../output/image_dir/testA/CLEVR_scenes_img.json" '
    
        os.chdir(output_dir + '/image_generation')
        print("rendering starting in "+ os.getcwd() )
        import time    

        for iter in range(0,args.pred_count):
            
            start = time.time()
            if args.target  == 'video':
                cmd = 'blender data/base_scene.blend --background --python single_video_remove_collision.py --  --num_videos 1 --start_idx ' + str(iter) + ' --suppress_blender_logs --input_file_json ' + json_dir + str(iter) + '.json' + vid_str
                os.system(cmd)
            elif args.target  == 'image':
                cmd = 'blender --background --python single_image.py -- --num_images 1 --use_gpu 1 --start_idx ' + str(iter) +' --input_file_json ' + json_dir + str(iter) + '.json' + img_str
                os.system(cmd)
            end = time.time()
            print("total time elapsed in rendering, ", end-start)
        os.chdir(cur_dir)
        
    if args.view == 1: 
        
        import cv2
        output_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) 
              
        # view last video
        if args.target  == 'video':
            
            prefix = '%s_%s_' % ('CLEVR', 'new')
            vid_template = '%s%%0%dd.avi' % (prefix, 6)
            vid_path = vid_template % (args.pred_count-1)            
            file = output_dir + "\output\\video_dir\\videos\\" + vid_path            
            cap = cv2.VideoCapture(file)
            if (cap.isOpened()== False):
                print("Error opening video stream or file")
            
            import time
            while(cap.isOpened()):
                ret, frame = cap.read()
#                 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if ret  ==  True:
                    cv2.imshow('frame',frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break
                time.sleep(0.05)
            cap.release()
            cv2.destroyAllWindows() 
       
        # view last image
        elif args.target  == 'image':
            prefix = '%s_%s_' % ('CLEVR', 'new')
            img_template = '%s%%0%dd.png' % (prefix, 6)
            img_path = img_template % (args.pred_count-1)
            file = output_dir + "\output\\image_dir\\images\\" + img_path
            img = cv2.imread(file,1)
            cv2.imshow('image',img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
           
        
if __name__ == '__main__':
  args = parser.parse_args()
  main(args)

