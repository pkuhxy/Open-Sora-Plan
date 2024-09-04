import os

import torch
from torchvision.io import write_video

IMG_FPS = 120


def save_videos(videos, save_path, fps, value_range=(-1, 1), normalize=True):
    os.makedirs(save_path, exist_ok=True)
    if isinstance(videos, (list, tuple)) or videos.ndim == 5:  # b,c,t,h,w
        for i, video in enumerate(videos):
            save_path_i = os.path.join(save_path, str(i) + ".mp4")
            _sava_video(video, save_path_i, fps, value_range, normalize)

    elif videos.ndim == 4:
        _sava_video(videos, os.path.join(save_path, "0" + ".mp4"), fps, value_range, normalize)
    else:
        raise ValueError("The video must be in either [b,c,t,h,w] or [c,t,h,w] format.")


def _sava_video(video, save_path, fps, value_range=(-1, 1), normalize=True):
    if video.ndim != 4:  # [c,t,h,w]
        raise Exception("video must be 4D array")
    if normalize:
        low, high = value_range
        video.clamp_(min=low, max=high)
        video.sub_(low).div_(max(high - low, 1e-5))
    video = video.mul(255).add_(0.5).clamp_(0, 255).permute(1, 2, 3, 0).to("cpu", torch.uint8)
    write_video(save_path, video, fps=fps, video_codec="h264")
    print(f"Saved video to {save_path}")


def prepare_multi_resolution_info(info_type, batch_size, image_size, num_frames, fps, device, dtype):
    if info_type is None:
        return dict()
    elif info_type == "PixArtMS":
        hw = torch.tensor([image_size], device=device, dtype=dtype).repeat(batch_size, 1)
        ar = torch.tensor([[image_size[0] / image_size[1]]], device=device, dtype=dtype).repeat(batch_size, 1)
        return dict(ar=ar, hw=hw)
    elif info_type in ["STDiT2", "OpenSora"]:
        fps = fps if num_frames > 1 else IMG_FPS
        fps = torch.tensor([fps], device=device, dtype=dtype).repeat(batch_size)
        height = torch.tensor([image_size[0]], device=device, dtype=dtype).repeat(batch_size)
        width = torch.tensor([image_size[1]], device=device, dtype=dtype).repeat(batch_size)
        num_frames = torch.tensor([num_frames], device=device, dtype=dtype).repeat(batch_size)
        ar = torch.tensor([image_size[0] / image_size[1]], device=device, dtype=dtype).repeat(batch_size)
        return dict(height=height, width=width, num_frames=num_frames, ar=ar, fps=fps)
    else:
        raise NotImplementedError("only support PixArtMS, OpenSora, STDiT2 Model")