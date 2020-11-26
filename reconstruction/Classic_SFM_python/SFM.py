import cv2 as cv
import numpy as np
from Classic_SFM_python.util import triangulate, essentialMatrix, points_3d_visualize, cameraPose, keypointColor
import os
# camera intrinsics
f = 720

k = np.eye(3)
k[0][0] = f
k[1][1] = f
k[0][2] = 640
k[1][2] = 360

init_cam = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0]])
camera_pos = []
camera_pos.append(init_cam)
dir = 'example_data/hampi/'
# place images in this directory
images = os.listdir(dir)

# images = ['vlcsnap-2020-10-26-10h32m43s388.png',
#           'vlcsnap-2020-10-26-10h32m50s487.png', 'vlcsnap-2020-10-26-10h32m56s617.png']
keypoints = np.empty((0, 3))
pointcolor = np.empty((0, 3))

for j in range(len(images) - 1): # loop through images and compare two at a time
    print("matching ",images[j],"and",images[j + 1])
    img1 = cv.imread(dir + images[0], 1)  # queryimage # left image
    img2 = cv.imread(dir + images[j + 1], 1)  # trainimage # right image
    sift = cv.xfeatures2d.SIFT_create()
    # akaze = cv.AKAZE_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    # kp1, des1 = akaze.detectAndCompute(img1, None)
    # kp2, des2 = akaze.detectAndCompute(img2, None)
    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    # bf = cv.BFMatcher(cv.NORM_HAMMING)
    # matches = bf.knnMatch(des1,des2, k=2)
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    good = []
    pts1 = []
    pts2 = []
    # filter points that are too far away
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            good.append(m)
            pts2.append(kp2[m.trainIdx].pt)
            pts1.append(kp1[m.queryIdx].pt)

    pts1 = np.int32(pts1)
    pts2 = np.int32(pts2)
    # get fundamental matrix from matched points
    F, mask = cv.findFundamentalMat(pts1, pts2, cv.FM_LMEDS)
    # We select only inlier points
    pts1 = pts1[mask.ravel() == 1]
    pts2 = pts2[mask.ravel() == 1]
    print("     found ",len(pts1)," points")
    dst = cv.addWeighted(img1, 0.5, img2, 0.5, 5)

    E = essentialMatrix(F, k)
    # Calculate M1 and M2 , M2 could be any of the 4 possible relative orientation pair of cameras
    M1 = camera_pos[0]
    M2_list = cameraPose(E)

    C1 = k.dot(M1)

    P_best = np.zeros((pts1.shape[0], 3))
    M2_best = np.zeros((3, 4))
    C2_best = np.zeros((3, 4))
    err_best = np.inf
    error_list = []

    # get_color
    # colors = keypointColor(img1, img2, pts1, pts2)
    cmin =0
    # try all possible orientations and choose the one with most points in front of both the cameras
    for i in range(M2_list.shape[2]):
        c=0
        M2 = M2_list[:, :, i]
        C2 = k.dot(M2)
        P_i, err, color = triangulate(C1, pts1, C2, pts2,img1)

        error_list.append(err)
        z_list = P_i[:, 2]
        for i,z in enumerate(z_list):
            if z > 0:
                # np.delete(P_i,i)
                c+=1

        if c > cmin:
            cmin = c
            colors=color
            err_best = err
            P_best = P_i
            M2_best = M2
            C2_best = C2
    print(cmin)
    # P_best = P_best[np.where(P_best[:,2]<100)]
    # keypoints.append(P_best)
    keypoints = np.vstack((keypoints, P_best))
    pointcolor = np.vstack((pointcolor, colors))
    camera_pos.append(M2_best)
# matplot lib visualization, not recommended when there are more than 3000 points, visualization may become choppy
points_3d_visualize(keypoints, pointcolor,camera_pos, f,img1,s=1.7)


# for x,y in zip(pts1,pts2):
#     dst = cv.line(dst, tuple(x),tuple(y) , (0,255,0), 1)
#     dst = cv.circle(dst, tuple(x), 5, (255,255,0), 1)
#     dst = cv.drawMarker(dst, tuple(y), (0, 0, 255),1)
#                    # markerType=mt, markerSize=30, thickness=2, line_type=cv2.LINE_AA)
#
# while(1):
#     cv.imshow("weighted",dst)
#
#     k = cv.waitKey(33)
#     if k==27:    # Esc key to stop
#         break
#     elif k==-1:  # normally -1 returned,so don't print it
#         continue
