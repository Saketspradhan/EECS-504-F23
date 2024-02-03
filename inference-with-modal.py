import os
import modal

volume = modal.NetworkFileSystem.new().persist("EECS-504-F23-modal-app-vol")

OUTPUT_DIR = "/Users/saketpradhan/Desktop/EECS-504-F23/"
CACHE_PATH = "/root/model_cache"


image = (
    modal.Image.debian_slim(python_version="3.9")  
    .run_commands(
        "pip install torch --extra-index-url https://download.pytorch.org/whl/cu118",
        "pip install torchvision --extra-index-url https://download.pytorch.org/whl/cu118",
        "pip install torchaudio --extra-index-url https://download.pytorch.org/whl/cu118",
        "pip install --upgrade --no-cache-dir gdown",
    )
    .apt_install("git", "ffmpeg", "cmake")
    .pip_install(
        "cmake", 
        "dlib==19.24.0",
        "numpy==1.23.4",
        "resampy==0.4.2",
        "scipy==1.10.1", 
        "tqdm==4.65.0", 
        "numba==0.56.4", 
        "requests==2.28.2",
        "tqdm==4.65.0", 
        "PyYAML==6.0",
        "xarray-einstats",  
        "ffmpy==0.3.0",
        "ffmpeg-python==0.2.0",
        "boost==0.1",
        "face_alignment==1.3.5", 
        "imageio==2.19.3", 
        "imageio-ffmpeg==0.4.7",
        "librosa==0.8.0",
        "pydub==0.25.1",
        "kornia==0.6.8",
        "yacs==0.1.8",
    )
    .run_commands(
        f"cd /root && git clone https://github.com/Saketspradhan/EECS-504-F23 \
            && cd EECS-504-F23 && dir && gdown --id 1xJGTJlPBJT6bf0JHMR1Nj1p63FjzvW3k -O checkpoints/auido2exp_00300-model.pth \
            && gdown --id 172qU4ID21IQdxbpZZxcZSeHKZB8k2eo8 -O checkpoints/auido2pose_00140-model.pth \
            && gdown --id 1ysJ6TO0QfymcrTZRO6PwFUtipErVM0RO -O checkpoints/epoch_20.pth \
            && gdown --id 1VNMYP7NQTwwlcIt1XfkFg-diXGekfJD2 -O checkpoints/facevid2vid_00189-model.pth.tar \
            && gdown --id 19dbOveGqLNomh5kOB7rRdtzIyGwu_Zlr -O checkpoints/mapping_00229-model.pth.tar \
            && gdown --id 1r_fOD_zBhNhfKWvnZjoBSRA551_8M89p -O checkpoints/shape_predictor_68_face_landmarks.dat \
            && gdown --id 1ctg4fF2mjK4pz7leubuKV6aXmTKgOTWT -O checkpoints/wav2lip.pth \
            && gdown --id 1qQblUd0vio6PG5VQ4PeUq5vDQC0Sbg0T -O checkpoints/BFM_Fitting/BFM_exp_idx.mat \
            && gdown --id 1p40eBV49KbGzAOCf7irDvReIe2MHqLhy -O checkpoints/BFM_Fitting/BFM_front_idx.mat \
            && gdown --id 1QJhdOZAIQeecSpHFkKnTjXV7NSJ3Yl6g -O checkpoints/BFM_Fitting/facemodel_info.mat \
            && gdown --id 1kDa7ZITEFJkJqvhET7FsG2g6OetwPmLo -O checkpoints/BFM_Fitting/select_vertex_id.mat \
            && gdown --id 1AInaOSwBGznDFVLAIlHZ-72qu9HgX01_ -O checkpoints/BFM_Fitting/similarity_Lm3D_all.mat \
            && gdown --id 1GZ0Ern34g2FRd1Szdf3K7CDTqD85U2XP -O checkpoints/BFM_Fitting/std_exp.txt \
            && gdown --id 1kYir4-a4CUsAIFLNZqmkx-yOEI2qwet0 -O checkpoints/hub/checkpoints/2DFAN4-cd938726ad.zip \
            && gdown --id 1EwGG1bS0EQA_R6yGoWm9BJVzli-erVpG -O checkpoints/hub/checkpoints/s3fd-619a316812.pth \
            && dir"
        
    )
)

stub = modal.Stub("EECS-504-F23-modal-app", image=image) 
print("Stub created with defined environment image")

@stub.function(gpu="A10G")
async def EECS504():
    print('Process 1 completed')
    import os
    script_name = "EECS-504-F23/inference.py"

    os.system("dir")
    os.chdir("EECS-504-F23")
    os.system("dir")

    os.system(
        "python inference.py"
        + " --driven_audio english_v1.wav"
        + " --source_image kajal.jpg"
        + " --result_dir EECS-504-F23/results"
    )

    final_fn = "EECS-504-F23/results/EECS-504-F23-results/kajal##english_v1.mp4"
    with open(final_fn, "rb") as f:
        return f.read()
    

@stub.local_entrypoint()
def main():
    video_data = EECS504.remote()
    abs_fn = os.path.join(OUTPUT_DIR, 'output_video.mp4')
    print(f"Downloading file at location: {abs_fn}")
    with open(abs_fn, "wb") as f:
        f.write(video_data)