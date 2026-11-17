---
id: 2026-nexusai-kevin-vesuvius-ink-bench-volumetric-ink
title: "vesuvius-ink-bench: volumetric ink-detection benchmarking and low-VRAM inference for Herculaneum scroll CT"
year: 2026
backend: pymupdf
---

vesuvius-ink-bench: volumetric ink-detection benchmarking and low-VRAM inference for Herculaneum scroll CT

nexusai-kevin

GitHub repository https://github.com/nexusai-kevin/vesuvius-ink-bench — commit 6bd16ff893 (2026-11-16). Documents: README.md, reports/benchmark_report.md. Community code repository (Vesuvius Challenge), not peer reviewed; all figures self-reported by the authors. Images omitted.

File: README.md

vesuvius-ink-bench

Volumetric ink-detection benchmarking and low-VRAM inference workspace compatible with

ScrollPrize/villa OME-Zarr conventions, the official scrollprize/ink_canonical_2um Hugging Face checkpoint, and public AWS Open Data Herculaneum scroll Zarr volumes (s3://vesuvius-

challenge-open-data/).

Installation

git clone https://github.com/nexusai-kevin/vesuvius-ink-bench.git cd vesuvius-ink-bench uv venv --python 3.12

# Standard install (CPU or default PyPI PyTorch wheel) uv pip install -e .

# Optional: NVIDIA CUDA 12.8 PyTorch wheel index (recommended for RTX 50-series / Blackwell) uv pip install torch --index-url https://download.pytorch.org/whl/cu128 uv pip install -e .

Quick Start: Production Low-VRAM Inference (vesuvius-infer)

vesuvius-infer streams any public AWS Open Data Herculaneum OME-Zarr URL (or local .zarr v2/v3 volume) through a budgeted host DDR5 RAM LRU cache, runs bfloat16 mixed-precision ResNet3D- 152 + 3D FPN decoder (i3d) inference in under 3 GiB VRAM with strictly separable 3D + Z- Hann overlap blending, and exports:

Primary Output Product — 2D Ink Surface Probability Map:

ink_surface_16bit.tiff — 16-bit grayscale TIFF surface projection (uint16)

ink_surface.png — 2D ink surface probability heatmap

ink_predictions.zarr/surface_prob_2d — Blosc/Zstd-compressed 2D Zarr array Depth-Slab Predictions:

ink_predictions.zarr/0 — Blosc/Zstd-compressed 3D OME-Zarr array storing the 3D Hannblended depth-slab predictions across (Z, Y, X)

On first run, vesuvius-infer (and vesuvius-bench) automatically downloads the pretrained

scrollprize/ink_canonical_2um checkpoint (r152_3ddec_v2_l5_epoch13.ckpt) from Hugging Face into

checkpoints/ink_canonical_2um/ (git-ignored) if not already present, and verifies weights_only=True +

strict=True.

# 1. Custom (z, y, x) bounding-box inference on AWS Open Data PHerc0332 .venv\Scripts\vesuvius-infer.exe `

--uri s3://vesuvius-challenge-open-data/PHerc0332/volumes/20251211183505-2.399um-0.2m-78keVmasked.zarr ` --level 2 ` --origin 4096 1792 1792 ` --shape 128 384 384 ` --output-dir outputs

# 2. Or full-level inference on a local or remote OME-Zarr level .venv\Scripts\vesuvius-infer.exe --uri path/to/scroll.zarr --level 2 --full-level --output-dir outputs

Reproducible Validation Suite (vesuvius-bench)

vesuvius-bench runs the full end-to-end verification pass: 1. Cold AWS Open Data S3 stream vs. warm host DDR5 RAM cache read (PHerc0332, level 2) 2. RTX 5080 bfloat16 throughput & peak VRAM profiling ([0, 1] input normalization) 3. Unblended vs. separable 3D + Z-Hann seam-blending discontinuity quantification 4. Ground-truth validation against labeled

PHercParis4/segments/20230702185753 (2.4 µm surface volume + inklabels.zarr + supervision.zarr) 5. Markdown (reports/benchmark_report.md), JSON (reports/benchmark_report.json), and PNG exports

.venv\Scripts\python.exe -m pytest -v .venv\Scripts\vesuvius-bench.exe --output-dir reports

Key Architecture & Features

Exact ScrollPrize/villa Architecture (model.py): VillaInkResNet3D matches ink-

detection/optimized_inference/model_resnet3d_3d_decoder.py (ResNet3DBackbone, DecoderResBlock3D with GroupNorm(min(32, C), C) + ReLU, DepthAttentionCollapse, and BatchNorm3d(1) normalization), loading all 976 checkpoint tensors via torch.load(..., weights_only=True) with strict=True. Streaming OME-Zarr Loader & DDR5 Cache (zarr_loader.py): Supports both Zarr v2 and Zarr v3 (FsspecStore) over s3:// (anonymous), https://, or local storage with a thread-safe

DDR5ChunkCache. Separable 3D + Z-Hann Blending (windowing.py): Per-axis raised-Hann weights preserve smooth (Y, X) tapering across every depth slice, and Z-Hann depth aggregation eliminates rectangular Z-slab footprints. RTX 5080 Mixed-Precision Pipeline (pipeline.py): bfloat16 autocast, pinned host staging buffers, optional channels_last_3d for 3D convolutions, deterministic seeding, CUDA event timing, and peak VRAM monitoring.

Verified RTX 5080 Benchmark & Ground-Truth Validation

Benchmark Value

PHerc0332 (Level 2, bfloat16) Tile Throughput 83,196,727.9 voxels/s (79.34 tiles/s; 19,385,945.7 ROI voxels/s)

PHerc0332 (Level 2, bfloat16) Peak VRAM 2,506.13 MiB allocated / 2,912.0 MiB reserved (< 3 GiB)

PHerc0332 (3D + Z-Hann Blending)

Seam Discontinuity Reduction

99.42% (122.4066x unblended vs. 0.3466x Hannblended)

PHercParis4 (2.4 µm, inklabels.zarr) ROC-AUC 0.9546

PHercParis4 (2.4 µm, inklabels.zarr)

F0.5 / Dice-F1 / IoU (th=0.50)

0.7903 / 0.8271 / 0.7052 (best F0.5 0.8724 at th=0.70)

License & Dataset Attribution

Code License: Released under the MIT License (see LICENSE). Dataset Attribution: Tomographic sub-volume benchmarks and validation use the EduceLab-Scrolls / Herculaneum CT scan datasets (PHerc0332 and PHercParis4) hosted on AWS Open Data (s3://vesuvius-challenge-open-data/) in accordance with the Vesuvius

Challenge Data Agreement (underlying tomographic data distributed under CC BY-NC 4.0 by EduceLab / Vesuvius Challenge). Pretrained Weights: scrollprize/ink_canonical_2um (r152_3ddec_v2_l5_epoch13.ckpt), released under the MIT License by the Vesuvius Challenge.

File: reports/benchmark_report.md

Vesuvius Ink-Detection Benchmark Report

Generated: 2026-11-16T22:36:14.358884+00:00

## 1. Environment & Pretrained Checkpoint

Component Value

Platform Windows-11-10.0.26200-SP0

Python / PyTorch 3.12.13 / 2.11.0+cu128

CUDA 12.8 (cuda_available=True)

GPU NVIDIA GeForce RTX 5080

Precision / AMP bfloat16 (pin_staging_buffer=True, channels_last_3d=False, seed=42)

HF Registry Repo scrollprize/ink_canonical_2um

Checkpoint File checkpoints\ink_canonical_2um\r152_3ddec_v2_l5_epoch13.ckpt (epoch 13, step 113246, weights_only=True)

Architecture ResNet3D-152 + 3D FPN Decoder (i3d) (976 tensors, strict=True)

## 2. Streaming OME-Zarr & Host DDR5 RAM Cache

Source URI: s3://vesuvius-challenge-open-data/PHerc0332/volumes/20251211183505-2.399um-0.2m-

78keV-masked.zarr (level 2) Full Level Shape: (8398, 3941, 3941) | Chunk Shape: (128, 128, 128) | Dtype: uint8 | Input Scaling: [0, 1] (uint8 / 255.0) Streamed Sub-Volume ROI: origin [4096, 1792, 1792], shape [128, 384, 384] (18.00 MiB, non-zero voxel fraction 100.00%) DDR5 Cache Budget: 16.0 GiB Cold Stream Time (AWS S3 -> DDR5): 1.7517 s (fetched 18.00 MiB) Warm Cache Read Time (DDR5 -> Host): 0.00886 s (2.13 GB/s, hit rate 50.00%)

## 3. Mixed-Precision Inference Throughput & VRAM (RTX 5080 16GB)

Value

Tile Shape / Stride [64, 128, 128] / [32, 64, 64]

Total 3D Tiles / Batch Size 75 / 8

GPU Inference Time 0.9453 s (wall 0.9736 s)

Throughput (Tile Voxels/sec) 83,196,727.9 voxels/s

Throughput (ROI Voxels/sec) 19,385,945.7 voxels/s

Tile Rate 79.34 tiles/s

Peak VRAM Allocated 2506.13 MiB

Peak VRAM Reserved 2912.0 MiB (budget 14.5 GiB, within budget: True)

2D Ink Surface Probability Range min=0.140929, mean=0.36425, p99=0.615562, max=0.635512 (std=0.140087)

4. 3D + Z-Hann Seam-Blending Quality

Unblended Tiling 3D + Z-Hann Blending

Seam Boundary Gradient 0.114695 0.000661

Interior Gradient 0.000937 0.001906

Seam-to-Interior Gradient Ratio 122.4066x 0.3466x

Seam Discontinuity Reduction — 99.42%

## 5. Ground-Truth Validation (PHercParis4/segments/20230702185753 (2.4 um))

Surface Volume URI: s3://vesuvius-challenge-opendata/PHercParis4/segments/20230702185753/surface-volumes/2.4um-0.22m-78keV-volume- 20260411134726.zarr Ground-Truth Labels URI: s3://vesuvius-challenge-opendata/PHercParis4/segments/20230702185753/ink-labels/2.4um-volume- 20260411134726/20260918/inklabels.zarr ROI: origin [0, 46080, 9728], shape [109, 512, 512] (supervised fraction 100.00%, ink fraction

27.98%) Inference Throughput / VRAM: 87,244,423.5 tile voxels/s in 1.7668 s | Peak VRAM 3121.41 MiB allocated / 3444.0 MiB reserved

Score (th=0.50) Optimal F0.5 (th=0.7)

ROC-AUC 0.9546 0.9546

F0.5 Score 0.7903 0.8724

Dice / F1 0.8271 0.8491

IoU (Jaccard) 0.7052 0.7377

## 6. Exported Visualizations

Predicted 2D Ink Surface: reports\ink_surface_prediction.png Seam-Blending Comparison: reports\seam_blending_comparison.png Ground-Truth Validation Comparison: reports\ground_truth_validation.png
