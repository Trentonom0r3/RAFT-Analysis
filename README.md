# RAFT-Analysis
Simple analysis script 'demotest.py' using RAFT optical flow to get flow vectors, occlusion masks, and Information on keyframes with significant motion changes 

```# Get list of images
image_dir = r"C:\\Users\\tjerf\\Desktop\\Testing\\src\\Testvids\\Input"
image_files = [os.path.join(image_dir, file) for file in sorted(os.listdir(image_dir))]

# Find significant motion in all pairs of images
find_significant_motion(image_files)
```

If you replace the file path  in demotest.py with the path to your frames, you can use the raft script. 

