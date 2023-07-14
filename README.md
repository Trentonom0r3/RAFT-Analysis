# RAFT-Analysis
Simple analysis script 'demotest.py' using RAFT optical flow to get flow vectors, occlusion masks, and Information on keyframes with significant motion changes 

```# Get list of images
image_dir = r"C:\\Users\\tjerf\\Desktop\\Testing\\src\\Testvids\\Input"
image_files = [os.path.join(image_dir, file) for file in sorted(os.listdir(image_dir))]

# Find significant motion in all pairs of images
find_significant_motion(image_files)
```

If you replace the file path  in demotest.py with the path to your frames, you can use the raft script. 


> Looking at the statistics, you can see the details about the distribution of motion within each frame:

- `mean`: The average magnitude of motion across the frame.
- `std_dev`: The standard deviation of motion magnitudes. This value can give you an idea of how much variability there is in the motion across the frame. A high standard deviation means that some parts of the frame are moving a lot more than others.
- `max`: The maximum magnitude of motion detected in the frame. This tells you the highest amount of movement detected in any single part of the frame.
- `min`: The minimum magnitude of motion detected in the frame. This tells you the least amount of movement detected in any single part of the frame.

With this information, you can start to understand more about what's happening in your video. For example, if you see a high maximum value and a high standard deviation, it could indicate that there's one specific area of the frame where a lot of movement is happening. On the other hand, if the maximum and mean values are similar and the standard deviation is low, it could indicate that motion is distributed fairly evenly across the whole frame.
>
