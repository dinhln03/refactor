from dataclasses import dataclass
import torch

@dataclass
class ClipConfig:
    device: str = "cpu"
    clip_model: str = "ViT-B/16"
    clipv2_model: str = "ViT-L-14"
    clipv2_pretrained: str = "datacomp_xl_s13b_b90k"
