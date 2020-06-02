# Darknet Container Image

## Getting Started
```bash
# Make working directory
mkdir Darknet && cd Darknet && mkdir data # data directory to store data/models

# Clone Project
git clone https://github.com/limwenyao/darknet-container.git

# Build container (optional, if already in repository)
cd darknet-container
git submodule update --init --recursive
docker-compose build

# Run container
docker-compose up -d
docker attach <container_name>

```

## Credits
Following darknet installation from https://github.com/AlexeyAB/darknet & opencv installation from https://linuxize.com/post/how-to-install-opencv-on-ubuntu-18-04/
