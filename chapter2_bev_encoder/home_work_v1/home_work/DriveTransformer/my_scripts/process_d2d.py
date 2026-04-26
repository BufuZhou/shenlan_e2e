import os


root_path = "/data/Bench2Drive/bench2drive-base"
dest_ln_base = "/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/data/bench2drive/v1"

_ANNO = "anno"
_CAMERA = "camera"

for root, dirs, files in os.walk(root_path):
    if _ANNO in dirs and _CAMERA in dirs:
        print(f"root:{root}")
        case_name = root.split('/')[-1]
        dest_path = os.path.join(dest_ln_base, case_name)
        os.system(f"ln -s {root} {dest_ln_base}")