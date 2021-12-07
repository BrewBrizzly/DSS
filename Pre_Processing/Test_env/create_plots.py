import numpy as np 

arr = np.load('/home/s3690970/Desktop/Bachelor_Project/DSS/Pre_Processing/Test_env/Lists/Paths_15.npy', allow_pickle = True)
sm = 0
for ls in arr:
    sm = sm + len(ls)

print(sm)


