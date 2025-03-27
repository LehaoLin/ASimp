Here is attachment files for submission:

### Files and Directories

- `3Ds` directory is for raw 3D GLB models
- `ae-model` and `mlp-model` are directory for NN models
- `output` directory is for output 3D GLB models
- `pipeline.py` is the full simplification pipeline
- `ae_model.py` and `mlp_model.py` are model structures used.
- `data.csv` is for the Name, median, mean, faces of the 3D models dataset from the user study

The total size of the 3D models is too big, so that we only keep 3D model's names here. 3D data used website: https://threedscans.com/

### How to run

- Make sure the environment: python 3.9, blender 3.6.10 and other packages used
- To download the pretrained models from `https://drive.google.com/drive/folders/1SFntMCPCaKN7TMF1-qfhxlxc-zSIuBjf?usp=sharing` under the root directory
- Put raw 3D models into `input/`
- `python pipeline.py`
- Find product 3D models in `output/`

### How to train

- Make sure .glb 3D files prepared in `3Ds`
- `python generate_pointcloud.py` to generate the point cloud files of the 3D models
- `python ae_train.py` to train the autoencoder model
- `python emb.py` to generate the embedding tensors
- `python mlp_train.py` to train the mlp model
- Make sure `ae-model/model.pth` and `mlp-model/model.pth` are ready
- Put original 3D models into `input/`
- `python pipeline.py` and find the ASimp output inside `output/`
