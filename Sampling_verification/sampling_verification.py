import os
from argparse import ArgumentParser


#TODO: comment code!!!


def get_files(dir_path):
    contained_files = []
    file_names = set()
    for root, _, files in os.walk(dir_path):
        for file in files:
            contained_files.append(file)
            file_name = os.path.splitext(os.path.basename(file))[0]
            file_names.add(file_name)
    return contained_files, file_names


def clean_folder(data_path, files_list, excess):
    for file in files_list:
        file_name = os.path.splitext(os.path.basename(file))[0]
        if file_name in excess:
            os.remove(os.path.join(data_path, file))


def make_verification(sampling_path, marking_path):
    sampling_files, sampling_filenames = get_files(sampling_path)
    marking_files, marking_filenames = get_files(marking_path)
    excess = sampling_filenames.symmetric_difference(marking_filenames)
    print('Excess filenames: \n', sorted(excess))
    clean_folder(sampling_path, sampling_files, excess)
    clean_folder(marking_path, marking_files, excess)


def init_argparse():
    # Initialize params of argparse
    parser = ArgumentParser(description='Sampling verification script')
    parser.add_argument(
        '-samples',
        '--sampling_path',
        nargs='?',
        help='path to folder with pictures of sampling',
        required = True,
        type=str)
    parser.add_argument(
        '-marks',
        '--marking_path',
        nargs='?',
        help='path to folder with marking of sampling',
        required=True,
        default=1,
        type=str)
    return parser


def main():
    args = init_argparse().parse_args()
    sampling_path = args.sampling_path
    marking_path = args.marking_path
    make_verification(sampling_path, marking_path)


if __name__ == '__main__':
    main()