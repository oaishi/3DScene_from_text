# Holistic static and animated 3D scene generation from diverse text descriptions

We propose a novel approach to generate 3D scenes (both animated and static) from text using a Transformer based NLP architecture and non-differential renderer.

## Dependencies

1. Blender (version 2.78c) (Please see details  from [here](https://github.com/facebookresearch/clevr-dataset-gen))
2. Pytorch
3. [Transformers](https://huggingface.co/transformers/)
4. Numpy
5. Pickel
6. OpenCV

## Few Examples


Description | Ground truth | Generated Scene
------------ |------------ | -------------
"A rocking cyan matte sphere, a small rocking gray <br> matte object, a small rocking shiny cylinder,<br> a large rocking blue matte object, a spinning blue matte cube,<br>  a small moving brown sphere <br> and a rocking blue shiny cube." | ![](https://github.com/oaishi/3DScene_from_text/blob/master/output/video_dir/testA/3/3.gif) | ![](https://github.com/oaishi/3DScene_from_text/blob/master/output/video_dir/testA/3/output.gif)
"Draw a large yellow colored cylinder of matte texture, a large cyan colored cube of  <br> matte texture, a large brown colored cylinder of shiny texture, a large red colored <br> cube of matte texture and a large brown colored <br> cylinder of shiny texture." | ![](https://github.com/oaishi/3DScene_from_text/blob/master/output/image_dir/images_testB/1/CLEVR_valB_004166.png) | ![](https://github.com/oaishi/3DScene_from_text/blob/master/output/image_dir/images_testB/1/CLEVR_new_000001.png)


All other examples are under '\Output\' folder.
## Run Prediction

To run prediction on the model, M<sub>static</sub> - 
```
cd scripts
python runner.py --type "image" --target "image" --pred_count 15
```

Here, pred_count specifies number of prediction to run. For evaluation, 64 sample test files have been attached.

To run prediction on the model, M<sub>animated</sub> - 
```
cd scripts
python runner.py --type "video" --target "video" --pred_count 15
```

To run prediction on the model, M<sub>full</sub> -
```
cd scripts
python runner.py --type "combined" --target "image" --pred_count 15
```
Replace target with video to generate videos instead. An image takes around 3-4 seconds to be rendered. A video takes around 2-4 minutes to be rendered. 

All generated images(static scenes) and videos(animated scenes) are saved in the output folder.

## Run Evaluation
To run evaluation on the model, M<sub>static</sub> - 
```
cd scripts
python runner.py --type "image" --sector "evaluate"
```

To run evaluation on the model, M<sub>animated</sub> - 
```
cd scripts
python runner.py --type "video" --sector "evaluate" 
```

To run evaluation on the model, M<sub>full</sub> -
```
cd scripts
python runner.py --type "combined" --sector "evaluate"
```

## Run Prediction on user given input 
For the model, M<sub>static</sub> - 
```
cd scripts
python runner.py --type "image" --sector "predict_single" --description <YOUR_DESCRIPTION> 
```

For the model, M<sub>animated</sub> - 
```
cd scripts
python runner.py --type "video" --sector "predict_single" --description <YOUR_DESCRIPTION> 
```

For the model, M<sub>full</sub> -
```
cd scripts
python runner.py --type "combined" --sector "predict_single" --description <YOUR_DESCRIPTION> 
```
