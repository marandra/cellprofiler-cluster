#!/usr/bin/env python
import sys
import re
'''
Converts original CellProfiler pipeline to CLI LoadData + CreateBatch modules
'''
if len(sys.argv) != 2:
    raise Exception('Usage: {} {} {}'.format(sys.argv[0], 'pipeline'))
    

ifile = 'image_sets.csv'
ipath = '.'
fn = sys.argv[1]
with open(fn, 'r') as fi:
    # replace hex codes
    text = fi.read()
    #text = re.sub('\\\\x5B', '[', text)
    #text = re.sub('\\\\x5D', ']', text)
    #text = re.sub('\\\\x7C', '|', text)
    #text = re.sub('\\\\x3A', '', text)

with open(fn + '.tmp', 'wb') as fi:
    fi.write(text)

fi = open(fn + '.tmp', 'r')
fo = open('HeadlessCreateBatch.cppipe', 'wb')

add_load_module = '''
LoadData:[module_num:1|svn_version:\\'Unknown\\'|variable_revision_number:6|show_window:True|notes:[]|batch_state:array([], dtype=uint8)|enabled:True|wants_pause:False]
    Input data file location:Default Input Folder|None
    Name of the file:{}
    Load images based on this data?:Yes
    Base image location:None|
    Process just a range of rows?:No
    Rows to process:1,100000
    Group images by metadata?:No
    Select metadata tags for grouping:
    Rescale intensities?:Yes
'''.format(ifile)

# remove input images module
flag = False
for line in fi:
    
    line = line.strip('\r\n')

    kmodule = 'ModuleCount'
    if line.split(':')[0] == kmodule:
        nmodule = int(line.split(':')[1]) - 2
        fo.write(kmodule + ':' + str(nmodule) + '\n')
        continue
    
    kmodule = 'MessageForUser'
    if line.split(':')[0] == kmodule:
        fo.write(add_load_module)
        continue

    kmodule = 'Images'
    if line.split(':')[0] == kmodule:
        flag = True
        continue

    kmodule = 'Metadata'
    if line.split(':')[0] == kmodule:
        flag = True
        continue

    kmodule = 'NamesAndTypes'
    if line.split(':')[0] == kmodule:
        flag = True
        continue

    kmodule = 'Groups'
    if line.split(':')[0] == kmodule:
        flag = True
        continue

    if flag:
        if line[:4] != '    ':
            flag = False
        continue

    if line.find('module_num:') >= 0:
        npre = line.split('module_num:')[0]
        nmod = int(line.split('module_num:')[1].split('|svn_version')[0]) - 3
        npos = line.split('module_num:')[1].split('|svn_version')[1]
        line = npre + 'module_num:' + str(nmod) + '|svn_version' + npos
    
    fo.write(line + '\n')

#add_create_module_p1 = '\nCreateBatchFiles:[module_num:{}|svn_version:\\\'Unknown\\\'|variable_revision_number:6|show_window:True|notes:\\x5B\\x5D|batch_state:array(\\x5B\\x5D, dtype=uint8)|enabled:True|wants_pause:False]'.format(nmod + 1)
#add_create_module_p2 = '''
#    Store batch files in default output folder?:No
#    Output folder path:/import/bc2/home/schwede/raschi/Projects/CellProfilerDemo
#    Are the cluster computers running Windows?:No
#    Hidden\\x3A in batch mode:No
#    Hidden\\x3A in distributed mode:No
#    Hidden\\x3A default input folder at time of save:/home/raschi/
#    Hidden\\x3A revision number:0
#    Hidden\\x3A from old matlab:No
#'''


add_create_module_p1 = '\nCreateBatchFiles:[module_num:{}|svn_version:\\\'Unknown\\\'|variable_revision_number:6|show_window:True|notes:[]|batch_state:array([], dtype=uint8)|enabled:True|wants_pause:False]'.format(nmod + 1)
add_create_module_p2 = '''
    Store batch files in default output folder?:No
    Output folder path:.
    Are the cluster computers running Windows?:No
    Hidden\\x3A in batch mode:No
    Hidden\\x3A in distributed mode:No
    Hidden\\x3A default input folder at time of save:.
    Hidden\\x3A revision number:0
    Hidden\\x3A from old matlab:No
'''

fo.write(add_create_module_p1)
fo.write(add_create_module_p2)
fo.close()
