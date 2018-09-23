import os
import shutil
import random
from argparse import ArgumentParser


def func(marks_path):
    dict_classes = dict()
    for root, _, files in os.walk(marks_path):
        for file in files:
            if file.endswith('.xml'):
                key = os.path.basename(file)[0]
                file_name = os.path.splitext(os.path.basename(file))[0]
                if key not in dict_classes.keys():
                    dict_classes[key] = [file_name]
                else:
                    dict_classes[key].append(file_name)
    return dict_classes


def prepare_data(frames_path, marks_path):
    annotation_folder = 'Annotations'
    jpeg_folder = 'JPEGImages'
    imagesets_folder = 'ImageSets'
    if not os.path.exists(annotation_folder):
        os.makedirs(annotation_folder)
    if not os.path.exists(jpeg_folder):
        os.makedirs(jpeg_folder)
    if not os.path.exists(imagesets_folder):
        os.makedirs(imagesets_folder)
    dict_classes = func(marks_path)
    train = []
    test = []
    for key in dict_classes.keys():
        if key == '5':
            train_count = 600
            test_count = 60
        else:
            train_count = 1100
            test_count = 100
        traintest_lst = random.sample(dict_classes[key], train_count+test_count)
        test_lst = random.sample(traintest_lst, test_count)
        train_lst = list(sorted(set(traintest_lst).symmetric_difference(set(test_lst))))
        train.extend(train_lst)
        test.extend(test_lst)
    train = sorted(train)
    test = sorted(test)
    dict_files = dict()
    files = set(train).union(set(test))
    cur_number = 1
    for el in files:
        dict_files[el] = '{:0>6}'.format(cur_number)
        cur_number += 1
    trainval_file = open(os.path.join(imagesets_folder, 'trainval.txt'), 'w')
    trainval_filenames = []
    test_file = open(os.path.join(imagesets_folder, 'test.txt'), 'w')
    test_filenames = []
    for el in dict_files.keys():
        shutil.copy(os.path.join(frames_path, el+'.jpg'), os.path.join(jpeg_folder, dict_files[el]+'.jpg'))
        new_xml = os.path.join(annotation_folder, dict_files[el]+'.xml')
        shutil.copy(os.path.join(marks_path, el + '.xml'), new_xml)
        with open(new_xml, 'r+') as f:
            line = f.read()
            line = line.replace(line[(line.find('_')-1):line.rfind('jpg')], str(dict_files[el])+'.')
            f.write(line)
            f.seek(0)
            f.write(line)
            f.truncate()
        if el in train:
            trainval_filenames.append(str(dict_files[el]))
        if el in test:
            test_filenames.append(str(dict_files[el]))
    for el in sorted(trainval_filenames):
        trainval_file.write(el + '\n')
    for el in sorted(test_filenames):
        test_file.write(el + '\n')
    trainval_file.close()
    test_file.close()
    print('Done')


def init_argparse():
    # Initialize params of argparse
    parser = ArgumentParser(description='Renaming files in the order')
    parser.add_argument(
        '-frames',
        '--frames_path',
        nargs='?',
        help='path to folder with frames',
        required = True,
        type=str)
    parser.add_argument(
        '-marks',
        '--marks_path',
        nargs='?',
        help='path to folder with marks',
        required=True,
        type=str)
    return parser


def main():
    args = init_argparse().parse_args()
    frames_path = args.frames_path
    marks_path = args.marks_path
    prepare_data(frames_path, marks_path)


if __name__ == '__main__':
    main()