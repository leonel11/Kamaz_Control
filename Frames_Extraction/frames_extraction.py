import cv2
import os
import re
from argparse import ArgumentParser


def get_video_paths(data_path):
    video_paths = []
    for root, _, files in os.walk(data_path): # get all paths to avi-videos
        for file in files:
            if file.endswith('.avi'):
                video_paths.append(os.path.join(root, file))
    return video_paths


def get_class_number(file_name):
    if file_name.find('ekranturb') >= 0:
        return '0'
    if file_name.find('kkomp') >= 0:
        return '1'
    if file_name.find('kol') >= 0:
        return '2'
    if file_name.find('krysh') >= 0:
        return '3'
    if file_name.find('perehodnik') >= 0:
        return '4'
    if file_name.find('pod') >= 0:
        return '5'
    if file_name.find('turbokompressor') >= 0:
        return '7'
    if file_name.find('turb') >= 0:
        return '6'
    if file_name.find('usel') >= 0:
        return '8'
    if file_name.find('val') >= 0:
        return '9'
    return ''


def extract_frames(video_path, missed_frames, freq_frames, save_path):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    class_number = get_class_number(str.lower(video_name))
    video_number = '{:0>2}'.format(int(re.sub('[^0-9]', '', video_name[video_name.rfind('.'):])))
    if len(video_number) > 2:
        video_number = video_number[1:]
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
    except OSError:
        print('Error: Creating directory of data')
        return
    cap = cv2.VideoCapture(video_path)  # open video
    cur_frame = 1 # number of current frame
    while (cap.isOpened()):
        frame = cap.read()[1] # capture frame
        if frame is None: # frame haven't been read or the video was finished
            break
        if (cur_frame > missed_frames) and ((cur_frame-missed_frames) % freq_frames == 0):
            # save current frame in jpg file
            jpg_file = '{}_{}_{:0>4}.jpg'.format(class_number, video_number, cur_frame - missed_frames)
            file_name = os.path.join(save_path,  jpg_file)
            print('Creating \t ' + file_name)
            cv2.imwrite(file_name, frame)
        cur_frame += 1
    cap.release() # close video
    cv2.destroyAllWindows()


def init_argparse():
    # Initialize params of argparse
    parser = ArgumentParser(description='Frames Extraction script')
    parser.add_argument(
        '-data',
        '--data_path',
        nargs='?',
        help='path to folder with embedded videos',
        default='/train',
        type=str)
    parser.add_argument(
        '-freq',
        '--freq_frames',
        nargs='?',
        help='frequency of frames, whick would be extracted',
        default=1,
        type=int)
    parser.add_argument(
        '-miss',
        '--missed_frames',
        nargs='?',
        help='count of frames, which will be missed in the beggining of every video',
        default=0,
        type=int)
    parser.add_argument(
        '-savepath',
        '--save_path',
        nargs='?',
        help='path to folder, for saving frames',
        default='/frames',
        type=str)
    return parser


def main():
    args = init_argparse().parse_args()
    data_path = args.data_path
    freq_frames = args.freq_frames
    missed_frames = args.missed_frames
    save_path = args.save_path
    video_paths = get_video_paths(data_path)
    for path_to_avi in video_paths:
        extract_frames(path_to_avi, missed_frames, freq_frames, save_path)


if __name__ == '__main__':
    main()