# https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet
import os
import sys
import argparse
import math
import numpy as np
import cv2
import pyvirtualcam
import datetime


def resourcePath(filename):
    '''pyinstallerでEXE化した場合に必要'''
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return filename


def setup():
    parser = argparse.ArgumentParser(description='Mekakushi Virtual Camera.')
    parser.add_argument(
        '--cam', help='Camera device number.', type=int, default=0)
    args = parser.parse_args()
    camera_device = args.cam
    cap = cv2.VideoCapture(camera_device)
    if not cap.isOpened:
        print('--(!)Error opening video capture')
        exit(0)
    vcam = pyvirtualcam.Camera(width=640, height=480, fps=30)
    face_detector = cv2.FaceDetectorYN_create(
        resourcePath('assets/face_detection_yunet_2023mar.onnx'), '', (0, 0))
    nofacedetected_frame = cv2.imread(
        resourcePath('assets/shibaraku-omachi-kudasai.png'))
    return cap, vcam, face_detector, nofacedetected_frame


def get_mean_of_eyes(eyes_list, reye, leye):
    if len(eyes_list) == 0:
        last_rx, last_ry, last_lx, last_ly = reye[0], reye[1], leye[0], leye[1]
    else:
        (last_rx, last_ry), (last_lx, last_ly) = eyes_list[-1]
    eyes_list.append([reye, leye])
    if (reye[0]-last_rx)**2+(reye[1]-last_ry)**2 > 64 or (leye[0]-last_lx)**2+(leye[1]-last_ly)**2 > 64:
        eyes_list = eyes_list[-3:]
    else:
        eyes_list = eyes_list[-10:]
    m = np.array([[eyes[0][0], eyes[0][1], eyes[1][0], eyes[1][1]]
                  for eyes in eyes_list])
    rx, ry, lx, ly = np.mean(m, axis=0).astype(np.int32)
    return eyes_list, (rx, ry), (lx, ly)


def draw_mekakushi(frame, reye, leye):
    ox = (reye[0]+leye[0])//2
    oy = (reye[1]+leye[1])//2
    harf_w = (((leye[0]-reye[0])**2+(leye[1]-reye[1])**2)**0.5)/2*1.8
    harf_w = max(harf_w, 30)
    harf_h = max(harf_w / 4, 16)
    theta = math.atan2(leye[1]-reye[1], leye[0]-reye[0])
    pos = np.array([[-harf_w, -harf_h*0.8], [+harf_w, -harf_h*0.8],
                   [+harf_w, +harf_h*1.2], [-harf_w, +harf_h*1.2]])
    pos = np.dot(pos, np.array([[math.cos(theta), math.sin(theta)],
                                [-math.sin(theta), math.cos(theta)]]))
    pos = pos + np.array([[ox, oy]])
    pos = pos.astype(np.int32)
    frame = cv2.fillConvexPoly(frame, pos, (0, 0, 0), lineType=cv2.LINE_AA)
    return frame


def capture_loop(cap, vcam, face_detector, nofacedetected_frame):
    eyes_list = []
    frame_before = np.zeros((480, 640, 3), np.uint8)
    facedetected_time = None
    nofacedetected_time = datetime.datetime.now() - datetime.timedelta(seconds=60)
    while True:
        _, frame = cap.read()
        if frame is None:
            print('--(!) No captured frame -- Break!')
            return
        fh, fw, _ = frame.shape
        face_detector.setInputSize((fw, fh))
        _, faces = face_detector.detect(frame)
        faces = faces if faces is not None else []
        faces = list(filter(lambda x: x[-1] >= 0.5, faces))
        faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
        if faces is None or len(faces) == 0:
            if not nofacedetected_time:
                nofacedetected_time = datetime.datetime.now()
            if nofacedetected_time < datetime.datetime.now() - datetime.timedelta(seconds=3):
                facedetected_time = None
                frame = nofacedetected_frame
            else:
                frame = frame_before
        else:
            if not facedetected_time:
                facedetected_time = datetime.datetime.now()
                eyes_list = []
            if facedetected_time < datetime.datetime.now() - datetime.timedelta(seconds=1):
                nofacedetected_time = None
                face = faces[0]
                reye = tuple(map(int, face[4:4+2]))
                leye = tuple(map(int, face[6:6+2]))
                eyes_list, reye, leye = get_mean_of_eyes(eyes_list, reye, leye)
                frame = draw_mekakushi(frame, reye, leye)
                frame_before = frame
            else:
                frame = nofacedetected_frame
        cv2.imshow("face detection", frame)
        vcam.send(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        vcam.sleep_until_next_frame()
        if cv2.waitKey(1) == ord('q'):
            return


def main():
    cap, vcam, face_detector, nofacedetected_frame = setup()
    try:
        capture_loop(cap, vcam, face_detector, nofacedetected_frame)
    except Exception as e:
        print(e.with_traceback())
    cv2.destroyAllWindows()
    vcam.close()
    cap.release()


if __name__ == '__main__':
    main()
