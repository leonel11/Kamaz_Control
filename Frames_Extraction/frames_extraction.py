import cv2
import os
import shutil
import re
from pathlib import Path
from argparse import ArgumentParser


def get_video_paths(data_path):
    video_paths = []
    for root, _, files in os.walk(data_path): # get all paths to avi-videos
        for file in files:
            if file.endswith('.avi'):
                video_paths.append(os.path.join(root, file))
    return video_paths


def extract_frames(video_path, missed_frames, freq_frames):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    # dir_frames = os.path.join(os.path.dirname(video_path), video_name)
    # FIXME: bad bypassing the problem of Russian lettres in the path for saving
    # creating empty folder for frames
    dir_class = os.path.join(os.path.dirname(Path(video_path).parent), re.sub('[^a-zA-Z]', '', video_name))
    # path to folder, conforming the name of video
    dir_frames = os.path.join(dir_class, video_name)
    try:
        if not os.path.exists(dir_class):
            os.makedirs(dir_class)
        if os.path.exists(dir_frames):
            shutil.rmtree(dir_frames)
        os.makedirs(dir_frames)
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
            name = os.path.join(dir_frames, '{:0>4}.jpg'.format(cur_frame - missed_frames))
            print('Creating \t ' + name)
            cv2.imwrite(name, frame)
        cur_frame += 1
    cap.release() # close video
    cv2.destroyAllWindows()


def init_argparse():
    # Initialize params of argparse
    parser = ArgumentParser(description='Trains toxic comment classifier')
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
    return parser


def main():
    args = init_argparse().parse_args()
    data_path = args.data_path
    freq_frames = args.freq_frames
    missed_frames = args.missed_frames
    video_paths = get_video_paths(data_path)
    for path_to_avi in video_paths:
        extract_frames(path_to_avi, missed_frames, freq_frames)


if __name__ == '__main__':
    main()