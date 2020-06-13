# Darknet Container Image

## Getting Started
```bash
# Make working directory
mkdir Darknet && cd Darknet && mkdir data # data directory to store data/models

# Clone Project
git clone https://github.com/limwenyao/darknet-container.git

# Add data files
cd darknet-container/data/train
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2008/VOCtrainval_14-Jul-2008.tar
tar xvf VOCtrainval_14-Jul-2008.tar
cd ../pre-trained/
wget https://pjreddie.com/media/files/darknet53.conv.74

# Run pascalVOC to Yolo annotation conversion
cd ../src/
python pascalvoc-to-yolo.py -n ../data/cfg/voc.names -d ../data/train/VOCdevkit/VOC2008/ -t ../data/cfg/train.txt -rt /data/train/VOCdevkit/VOC2008/

# Build container (optional, if already in repository)
cd darknet-container
git submodule update --init --recursive
docker-compose build

# Run container
docker-compose up -d
docker attach <container_name>

# Run training
root@abc123:/darknet# ./darknet detector train /data/cfg/voc.data /data/cfg/yolov3-voc.cfg /data/pre-trained/darknet53.conv.74 -dont_show <optional -gpus 0,1,2,3>

```

## Credits
Following darknet installation from https://github.com/AlexeyAB/darknet & opencv installation from https://linuxize.com/post/how-to-install-opencv-on-ubuntu-18-04/
