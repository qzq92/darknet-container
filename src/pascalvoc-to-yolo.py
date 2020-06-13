import glob
import os
import pickle
import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join
import argparse


def parse_names_file(filename):
    with open(filename, 'r') as f:
        return list(filter(None, f.read().split('\n')))


def get_images_in_dir(dir_path):
    image_list = []
    for filename in glob.glob(dir_path + '/*.jpg'):
        image_list.append(filename)
    return image_list


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


def convert_annotation(dir_pascal_anno, dir_yolo_anno, image_path, classes):
    basename = os.path.basename(image_path)
    basename_no_ext = os.path.splitext(basename)[0]

    in_file = open(os.path.join(dir_pascal_anno, (basename_no_ext+'.xml')), 'r')
    out_file = open(os.path.join(dir_yolo_anno, (basename_no_ext+'.txt')), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    out_file.close()
    in_file.close()


def main():
    parser = argparse.ArgumentParser(description='Convert pascalVOC to darknet labels')
    parser.add_argument('-n', '--names', type=str, required=True,
                        help='A darknet .names file containing class names')
    parser.add_argument('-d', '--dir', type=str, help='Other main directory')
    parser.add_argument('-s', '--subdir', type=str,
                        help='Specify multiple sub-directories of pascalVOC folders. NOT IN USE')
    parser.add_argument('-t', '--textfile', type=str,
                        help='Path to save text file of images for training. Default does not generate')
    parser.add_argument('-rt', '--textfileroot', type=str,
                        help='Use only if running in container. Specify container path to data root. Default is host root')

    args = parser.parse_args()
    classes = parse_names_file(args.names)
    main_dir = os.path.abspath(args.dir) if (args.dir and os.path.exists(args.dir)) else os.getcwd()
    dirs = [main_dir]
    if args.textfile is not None:
        save_textfile = os.path.join(os.path.abspath(args.textfile), 'train.txt') if os.path.isdir(args.textfile) else \
            os.path.abspath(args.textfile)
        list_file = open(save_textfile, 'w')
    else:
        save_textfile = None
        list_file = None
    textfileroot = os.path.abspath(args.textfileroot) if args.textfileroot else None

    for directory in dirs:
        dir_pascal = os.path.join(directory, 'Annotations')
        dir_images = os.path.join(directory, 'JPEGImages')
        dir_yolo = os.path.join(directory, 'labels')
        if not (os.path.exists(dir_images) and os.path.exists(dir_pascal)):
            print(directory + ' does not contain pascal images or labels')
            continue

        if not os.path.exists(dir_yolo):
            os.makedirs(dir_yolo)

        image_paths = get_images_in_dir(dir_images)

        for image_path in image_paths:
            convert_annotation(dir_pascal, dir_yolo, image_path, classes)
            if save_textfile:
                if textfileroot:
                    list_file.write(os.path.join(textfileroot, os.path.relpath(image_path, start=main_dir)) + '\n')
                else:
                    list_file.write(image_path + '\n')
    if args.textfile:
        list_file.close()


if __name__ == '__main__':
    main()
