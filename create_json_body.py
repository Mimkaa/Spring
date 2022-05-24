from copy import deepcopy
from PIL import Image
import os
import json
import math

def get_dis_array(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def find_all_images(name='img', path=os.path.dirname(__file__)):
        result = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if name in file:
                    result.append(os.path.join(root, file))

        return result


def get_connections_grid(points):
    connections = []
    # finding of second smallest distance (diagonal)
    distances = []
    for i, p in enumerate(points):
        others = deepcopy(points)
        others.pop(i)
        for o in others:
            distances.append(get_dis_array(p, o))

    second_smallest = sorted(set(distances))[1]
    for i, p in enumerate(points):
        others = deepcopy(points)
        others.pop(i)
        for o in others:
            j = points.index(o)
            if get_dis_array(p, o)<second_smallest+1 and ([i,j] not in connections and [j,i] not in connections):
                connections.append([i,j])


    return connections


def make_json_from_an_image(image,scale,color):
    im = Image.open(image)
    pixels=list(im.getdata())
    width, height = im.size

    # points extraction
    points=[]
    grounded=[]

    for n,p in enumerate(pixels):
        x = n % width
        y = n// width
        if p[3]!=0:
            if sum(p[:3])<300:
                points.append([x,y])
            if sum(p[:3])<300 and sum(p[:3])>100 :
                grounded.append([x,y])
    grounded=[points.index(p) for p in grounded]
    connections = get_connections_grid(points)
    print(connections)
    return {"points":points,"connections":connections,"grounded":grounded,"scale":scale,"color":color}



def make_a_new_body(name,dict):
    curr_dir=os.getcwd()
    file_path=os.path.join(curr_dir,'bodies',name)
    with open(file_path,"w",encoding='utf-8') as fp:
        json.dump(dict, fp)



def read_json(path):

    f = open(path, 'r')
    dat = f.read()

    f.close()
    return json.loads(dat)



def load_rags(path):
    rag_list = os.listdir(path)

    rags = {}
    for rag in rag_list:
        rags[rag.split('.')[0]] = read_json(path + '/' + rag)
    return rags

images=find_all_images()
new_rag=make_json_from_an_image(images[2],13,(255,255,255))
make_a_new_body("vine1.txt",new_rag)