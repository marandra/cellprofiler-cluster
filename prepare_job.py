#!/usr/bin/env python
import os
import sys
import glob
import shutil


def transfer_images(REPO_PATH, IMAGE_PATH):
    '''
    '''
    shutil.copytree(REPO_PATH, IMAGE_PATH)


def create_image_sets_file(ROOT_PATH, IMAGE_PATH):
    '''
    specific image set for this pipeline
    creates image sets file from images in local repository
    '''
    pattern_b = '*d0.tif'
    pattern_g = '*d1.tif'
    pattern_r = '*d2.tif'

    blue = glob.glob(os.path.join(IMAGE_PATH, pattern_b))
    green = glob.glob(os.path.join(IMAGE_PATH, pattern_g))
    red = glob.glob(os.path.join(IMAGE_PATH, pattern_r))
    
    f = open(os.path.join(ROOT_PATH, 'image_sets.csv'), 'w')

    # some test to detect unexpected images
    if len(blue) != len(red) or len(blue) != len(green):
        raise Exception("Nr of images not equal")
    line = '"Group_Number","Group_Index","URL_OrigBlue","URL_OrigGreen","URL_OrigRed","PathName_OrigBlue","PathName_OrigGreen","PathName_OrigRed","FileName_OrigBlue","FileName_OrigGreen","FileName_OrigRed","Series_OrigBlue","Series_OrigGreen","Series_OrigRed","Frame_OrigBlue","Frame_OrigGreen","Frame_OrigRed","Channel_OrigBlue","Channel_OrigGreen","Channel_OrigRed","Metadata_Frame","Metadata_Series","Metadata_SizeC","Metadata_SizeT","Metadata_SizeZ"'
    f.write(line + '\n')
    blue.sort()
    for i, nb in enumerate(blue):
        ng = nb[:-6]+'d1.tif'
        nr = nb[:-6]+'d2.tif'
        
        if ng not in green or nr not in red:
            raise Exception("Mismatched image")
        line = '1,{},"file:{}","file:{}","file:{}","{}","{}","{}","{}","{}","{}",0,0,0,0,0,0,-1,-1,-1,"0","0","1","1","1"'.format(i + 1, nb, ng, nr, IMAGE_PATH, IMAGE_PATH, IMAGE_PATH, nb.split('/')[-1], ng.split('/')[-1], nr.split('/')[-1])
        f.write(line + '\n')
    f.close()

######################3
if __name__ == '__main__':

    if len(sys.argv) != 2:
        raise Exception('Usage: {} {}'.format(sys.argv[0], 'path_to_assay'))
    
    ASSAY_PATH = sys.argv[1]
    IMAGE_PATH = os.path.join(ASSAY_PATH, 'images')
    REPO_PATH = '/scicore/home/scicore/raschi/remoterepository'

    #try:
    #    os.makedirs(IMAGE_PATH)
    #except:
    #    if not os.path.isdir(IMAGE_PATH):
    #        raise
    
    transfer_images(REPO_PATH, IMAGE_PATH)
    create_image_sets_file(ASSAY_PATH, IMAGE_PATH)
