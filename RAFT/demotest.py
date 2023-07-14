import os
import sys
sys.path.append('core')

from argparse import Namespace
import torch
import numpy as np
import cv2
from raft import RAFT
from utils import flow_viz
from utils.utils import InputPadder
from PIL import Image

DEVICE = 'cuda'

def load_image(imfile, max_size=384):
    from PIL import Image
    img = Image.open(imfile).convert("RGB")
    
    # Proportionally resize the image
    width, height = img.size
    if width < height:
        new_width = max_size
        new_height = int(max_size * height / width)
    else:
        new_height = max_size
        new_width = int(max_size * width / height)
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    
    img = np.array(img).astype(np.uint8)
    img = torch.from_numpy(img).permute(2, 0, 1).float()
    return img.to(DEVICE)


def compute_optical_flow(args):
    model = torch.nn.DataParallel(RAFT(args))
    model.load_state_dict(torch.load(args.model))

    model = model.module
    model.to(DEVICE)
    model.eval()

    with torch.no_grad():
        images = [load_image(frame) for frame in args.images]
        padder = InputPadder(images[0].shape)
        images = [padder.pad(im)[0] for im in images]

        flow_low, flow_up = model(images[0].unsqueeze(0), images[1].unsqueeze(0), iters=20, test_mode=True)

        flow_np = flow_up[0].permute(1,2,0).cpu().numpy()
        u = flow_np[:,:,0]
        v = flow_np[:,:,1]

        viz_flow = flow_viz.flow_uv_to_colors(u, v, convert_to_bgr=False)

    return flow_up, viz_flow

def create_occlusion_mask(flow, threshold=1.0):
    magnitude = torch.norm(flow, dim=1)[0]
    mask = (magnitude > threshold).float()
    return mask

def calculate_motion_score(flow):
    magnitude = torch.norm(flow, dim=1)[0]
    return magnitude.mean().item()

import statistics

def calculate_motion_statistics(flow):
    magnitude = torch.norm(flow, dim=1)[0].cpu().numpy()
    return {
        'mean': np.mean(magnitude),
        'std_dev': np.std(magnitude),
        'max': np.max(magnitude),
        'min': np.min(magnitude),
    }

def find_significant_motion(frames, threshold=1.2):
    scores = []
    stats = []
    for i in range(len(frames)-1):
        args = Namespace()
        args.model = 'models/raft-things.pth'
        args.images = [frames[i], frames[i+1]]
        args.small = False
        args.mixed_precision = False

        flow, viz_flow = compute_optical_flow(args)
        score = calculate_motion_score(flow)
        scores.append(score)
        stat = calculate_motion_statistics(flow)
        stats.append(stat)

        # If this is not the first frame and the score increased significantly, mark it
        if i > 0 and score > scores[-2] * threshold:
            print(f"Significant motion between frames {i} and {i+1}")
            print(f"Score: {score}")
            print(f"Statistics: {stat}")
            mask = create_occlusion_mask(flow)

            # Save the mask and flow visualization
            mask_np = mask.cpu().numpy()
            cv2.imwrite(f"mask_{i}_{i+1}.png", mask_np * 255)
            cv2.imwrite(f"flow_{i}_{i+1}.png", viz_flow)


# Get list of images
image_dir = r"C:\\Users\\tjerf\\Desktop\\Testing\\src\\Testvids\\Input"
image_files = [os.path.join(image_dir, file) for file in sorted(os.listdir(image_dir))]

# Find significant motion in all pairs of images
find_significant_motion(image_files)
