import cv2 as cv
import numpy as np
from Classic_SFM_python.util import triangulate,findRandC, essentialMatrix,points_3d_visualize,cameraPose
#camera intrinsics
f = 720

k =np.eye(3)
k[0][0] = f
k[1][1] = f
k[0][2] = 640
k[1][2] = 390

img1 = cv.imread('example_data/vlcsnap-2020-10-26-10h32m50s487.png', 1)  #queryimage # left image
img2 = cv.imread('example_data/vlcsnap-2020-10-26-10h32m56s617.png', 1) #trainimage # right image
sift = cv.xfeatures2d.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)
flann = cv.FlannBasedMatcher(index_params,search_params)
matches = flann.knnMatch(des1,des2,k=2)
good = []
pts1 = []
pts2 = []
# ratio test as per Lowe's paper
for i,(m,n) in enumerate(matches):
    if m.distance < 0.8*n.distance:
        good.append(m)
        pts2.append(kp2[m.trainIdx].pt)
        pts1.append(kp1[m.queryIdx].pt)


pts1 = np.int32(pts1)
pts2 = np.int32(pts2)
F, mask = cv.findFundamentalMat(pts1,pts2,cv.FM_LMEDS)
# We select only inlier points
pts1 = pts1[mask.ravel()==1]
pts2 = pts2[mask.ravel()==1]

dst = cv.addWeighted(img1,0.5,img2,0.5,5)

E = essentialMatrix(F, k)
# CALCULATE M1 and M2
M1 = np.array([[1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 1, 0]])
M2_list = cameraPose(E)
#  TRIANGULATION
C1 = k.dot(M1)

P_best = np.zeros((pts1.shape[0], 3))
M2_best = np.zeros((3, 4))
C2_best = np.zeros((3, 4))
err_best = np.inf
error_list = []

for i in range(M2_list.shape[2]):
    M2 = M2_list[:, :, i]
    C2 = k.dot(M2)
    P_i, err = triangulate(C1, pts1, C2, pts2)
    error_list.append(err)
    z_list = P_i[:, 2]
    if all(z > 0 for z in z_list):
        err_best = err
        P_best = P_i
        M2_best = M2
        C2_best = C2



points_3d_visualize(P_best)

# for x,y in zip(pts1,pts2):
#     dst = cv.line(dst, tuple(x),tuple(y) , (0,255,0), 1)
#     dst = cv.circle(dst, tuple(x), 5, (255,255,0), 1)
#     dst = cv.circle(dst, tuple(y), 5, (0,255,255), 1)
#
# while(1):
#     cv.imshow("weighted",dst)
#     k = cv.waitKey(33)
#     if k==27:    # Esc key to stop
#         break
#     elif k==-1:  # normally -1 returned,so don't print it
#         continue




