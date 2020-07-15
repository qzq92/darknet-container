# Darknet Container Image

## Getting Started
```bash
# 1) Make working directory
mkdir Darknet && cd Darknet && mkdir data # data directory to store data/models

# 2) Clone Project
git clone https://github.com/limwenyao/darknet-container.git

# 3) Build container (optional, if already in repository)
cd darknet-container
git submodule update --init --recursive
docker-compose build

# 4) Add data files
cd darknet-container/data/train
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2008/VOCtrainval_14-Jul-2008.tar
tar xvf VOCtrainval_14-Jul-2008.tar
cd ../pre-trained/
wget https://pjreddie.com/media/files/darknet53.conv.74

# 5a) Run container (DOCKER-COMPOSE)
docker-compose up -d
docker attach <container_name>

# 5b) Run container (KUBERNETES)
kubectl create -f kubernetes-deployment-nfspvc.yml
kubectl get svc # Find externalIP/NodePortIP to access jupyter notebook directly
kubectl logs darknet-container-pascal #Get the jupyter token key

# A) Run the end to end pre-processing/training in example jupyter notebook
root@abc123:/darknet# cd /
root@abc123:/# jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root # Navigate to /mnt/src/ to find the .ipynb

# B) OR From container cmd line:
# Run pascalVOC to Yolo annotation conversion (if your data is already not in Yolo annotation)
root@abc123:/darknet# cd ../src/
root@abc123:/src# python pascalvoc-to-yolo.py -n ../data/cfg/voc.names -d ../data/train/VOCdevkit/VOC2008/ -t ../data/cfg/train.txt

# Run training
root@abc123:/darknet# ./darknet detector train /mnt/data/cfg/voc.data /mnt/data/cfg/yolov3-voc.cfg /mnt/data/pre-trained/darknet53.conv.74 -dont_show <optional -gpus 0,1,2,3>

```

## Credits
Following darknet installation from https://github.com/AlexeyAB/darknet & opencv installation from https://linuxize.com/post/how-to-install-opencv-on-ubuntu-18-04/
