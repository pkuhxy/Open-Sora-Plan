LCALIB_PACKAGE_PATH=$(python -c "import lcalib; print(lcalib.__path__[0])")
export LD_LIBRARY_PATH=${LCALIB_PACKAGE_PATH}:$LD_LIBRARY_PATH
rm -rf /dev/shm/sem.lccl*
rm -rf /tmp/.lccl*
NUM_FRAME=61
PROJECT_NAME="sora_plan"
export PROJECT=$PROJECT_NAME
WEIGHT_PATH="/home/opensora/pre_weights/"
env
export WANDB_MODE='offline'
accelerate launch \
    --config_file scripts/accelerate_configs/multi_node_example.yaml \
    --machine_rank=${MACHINE_RANK} \
    --main_process_ip=${MAIN_PROCESS_IP_VALUE} \
    opensora/train/train_t2v.py \
    --model LatteT2V-XL/122 \
    --text_encoder_name ${WEIGHT_PATH}/DeepFloyd/t5-v1_1-xxl \
    --cache_dir "../cache_dir" \
    --dataset t2v \
    --ae CausalVAEModel_4x8x8 \
    --ae_path "${WEIGHT_PATH}/CausalVAEModel_4x8x8_0430/" \
    --video_data "./scripts/train_data/video_data.txt" \
    --image_data "./scripts/train_data/image_data.txt" \
    --sample_rate 1 \
    --num_frames ${NUM_FRAME} \
    --max_image_size 512 \
    --gradient_checkpointing \
    --attention_mode="xformers" \
    --mixed_precision="bf16" \
    --train_batch_size=1 \
    --dataloader_num_workers 10 \
    --gradient_accumulation_steps=1 \
    --max_train_steps=1000000 \
    --learning_rate=1e-5 \
    --lr_scheduler="cosine" \
    --lr_warmup_steps=500 \
    --report_to="wandb" \
    --checkpointing_steps=250 \
    --output_dir="/home/image_data/checkpoints/${PROJECT}/" \
    --allow_tf32 \
    --num_sampling_steps=50 \
    --pretrained "/home/image_data/checkpoints/512_based_linbin_lr1e-5_node46_ddp/checkpoint-23000/model/diffusion_pytorch_model.safetensors" \
    --model_max_length 300 \
    --use_image_num 2 \
    --enable_tiling \
    --sp_size 1 \
    --resume_from_checkpoint="latest" \
    --train_sp_batch_size 1
