# NMT Training Configuration (EXP-NMT-SAN-001)

## Overview
This document specifies the intended hyperparameter configuration for the first fine-tuning experiment of MatriVaani's Hindi-Santhali translation engine, assuming sufficient verified parallel data becomes available.

## Base Model
- **Model**: `AI4Bharat/IndicTrans2` (en-indic / indic-en family adapted)
- **Parameters**: ~1.1 Billion
- **Target Precision**: `bfloat16` or `INT8` (via bitsandbytes)

## Dataset
- **Version**: `MATRI-NMT-HI-SAT-v0.1` (Currently Blocked: 0 verified pairs)
- **Target Size**: Minimum 1,000 verified educational pairs required to begin.

## Training Hyperparameters (LoRA/PEFT)
To avoid catastrophic forgetting and manage GPU memory, Low-Rank Adaptation (LoRA) will be utilized for fine-tuning.

| Parameter | Value |
|-----------|-------|
| `learning_rate` | 2e-5 |
| `batch_size` | 4 (per device) |
| `gradient_accumulation` | 8 |
| `epochs` | 10 |
| `optimizer` | AdamW (8-bit) |
| `scheduler` | linear (with warmup) |
| `warmup_ratio` | 0.1 |
| `max_seq_length` | 128 (Optimized for short classroom commands) |
| `lora_r` | 16 |
| `lora_alpha` | 32 |
| `lora_dropout` | 0.05 |

## Hardware Requirements
- Minimum 16GB VRAM (e.g., T4/V100/A10G) for INT8 LoRA training.
- 32GB system RAM.

## Status
**BLOCKED** due to insufficient data. Waiting for dataset acquisition.
