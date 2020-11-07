# Simplified SFM
| Frame1    | Frame2       |
| -------------- | -------------- |
![frame1](reconstruction/example_data/vlcsnap-2020-10-26-10h32m50s487.png) |   ![frame2](reconstruction/example_data/vlcsnap-2020-10-26-10h32m56s617.png)

##### 1. Keypoints matching: SIFT , Flann based matching

##### 2. Estimate Fundamental matrix, Essential matix

##### 3. Recover Camera pose and triangulate the matched points in world coordinates, camera chirality

##### 4. !!!Missing Bundle Adjustment

### Key points matched
![](reconstruction/example_data/keypointsmatched.png)

### matplotlib visualization
![](reconstruction/example_data/matplotpreview.png)

