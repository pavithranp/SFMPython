import numpy as np
import scipy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def findRandC(essential_matrix):
    U, s, V = np.linalg.svd(essential_matrix, full_matrices=True)
    W = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])

    R1 = np.dot(np.dot(U, W), V)
    R2 = np.dot(np.dot(U, np.transpose(W)), V)

    C1 = U[:, -1]
    C2 = -1 * U[:, -1]
    print(int(np.linalg.det(R1)))
    R1 = np.sign(np.linalg.det(R1)) * R1
    R2 = np.sign(np.linalg.det(R2)) * R2
    return R1, R2, C1, C2
    # Rotation and centers can be combinations of any of the above two - 4 possibilities


def essentialMatrix(F, K):
    E = K.T.dot(F).dot(K)
    return E


def getIfromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    RGBint = (red << 16) + (green << 8) + blue
    return RGBint


def keypointColor(img1, img2, pts1, pts2):
    # x=np.array()
    colors = []

    for x, y in zip(pts1, pts2):
        k = img1[x[1], x[0]]
        # inte = getIfromRGB(k)
        # h = "#"+hex(inte).upper()[2:]

        colors.append([k[2], k[1], k[0]])
        # if any(img1[x[1],x[0]] != img2[y[1],y[0]]):
        #     print("image1:",img1[x[1],x[0]])
        #     print("image2:",img2[y[1], y[0]])
    return np.array(colors)


def cameraPose(E):
    U, S, V = np.linalg.svd(E)
    m = S[:2].mean()
    E = U.dot(np.array([[m, 0, 0], [0, m, 0], [0, 0, 0]])).dot(V)
    U, S, V = np.linalg.svd(E)
    W = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])

    if np.linalg.det(U.dot(W).dot(V)) < 0:
        W = -W

    # possible orientations of the camera
    M2s = np.zeros([3, 4, 4])
    M2s[:, :, 0] = np.concatenate([U.dot(W).dot(V), U[:, 2].reshape([-1, 1]) / abs(U[:, 2]).max()], axis=1)
    M2s[:, :, 1] = np.concatenate([U.dot(W).dot(V), -U[:, 2].reshape([-1, 1]) / abs(U[:, 2]).max()], axis=1)
    M2s[:, :, 2] = np.concatenate([U.dot(W.T).dot(V), U[:, 2].reshape([-1, 1]) / abs(U[:, 2]).max()], axis=1)
    M2s[:, :, 3] = np.concatenate([U.dot(W.T).dot(V), -U[:, 2].reshape([-1, 1]) / abs(U[:, 2]).max()], axis=1)
    return M2s


def triangulate(C1, pts1, C2, pts2):
    # Subtract RHS from LHS and equate to 0
    # Take X common to get AX=0
    # Solve for X with SVD
    # for 2 points we have four equation

    P_i = []

    for i in range(pts1.shape[0]):
        A = np.array([pts1[i, 0] * C1[2, :] - C1[0, :],
                      pts1[i, 1] * C1[2, :] - C1[1, :],
                      pts2[i, 0] * C2[2, :] - C2[0, :],
                      pts2[i, 1] * C2[2, :] - C2[1, :]])

        # SVD to solve for 3D coordinate
        u, s, v = np.linalg.svd(A)
        X = v.T[:, -1]
        # 4->3 coordinates removing homogenous coordinates
        X = X / X[-1]
        P_i.append(X)

    P_i = np.asarray(P_i)

    # print('P_i: ', P_i)

    # For reprojection error calculation
    pts1_out = np.matmul(C1, P_i.T).T
    pts2_out = np.matmul(C2, P_i.T).T

    for i in range(pts1_out.shape[0]):
        pts1_out[i, :] = pts1_out[i, :] / pts1_out[i, -1]
        pts2_out[i, :] = pts2_out[i, :] / pts2_out[i, -1]

    # NON - HOMOGENIZING
    pts1_out = pts1_out[:, :-1]
    pts2_out = pts2_out[:, :-1]

    # cumulative reprojection error
    reprojection_err = 0
    for i in range(pts1_out.shape[0]):
        reprojection_err = reprojection_err + np.linalg.norm(pts1[i, :] - pts1_out[i, :]) ** 2 + np.linalg.norm(
            pts2[i, :] - pts2_out[i, :]) ** 2
    # print(reprojection_err)

    # NON-HOMOGENIZING
    P_i = P_i[:, :-1]

    return P_i, reprojection_err


def points_3d_visualize(P_best, colors, s):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect('auto')

    X = P_best[:, 0]
    Y = P_best[:, 1]
    Z = P_best[:, 2]

    ax.scatter(X, Y, Z, s=s, c=colors / 255.0)

    max_range = np.array([X.max() - X.min(), Y.max() - Y.min(), Z.max() - Z.min()]).max() / 2.0

    mid_x = (X.max() + X.min()) * 0.5
    mid_y = (Y.max() + Y.min()) * 0.5
    mid_z = (Z.max() + Z.min()) * 0.5
    # ax.set_xlim(mid_x - max_range, mid_x + max_range)
    # ax.set_ylim(mid_y - max_range, mid_y + max_range)
    # ax.set_zlim(mid_z - max_range, mid_z + max_range)

    plt.show()
