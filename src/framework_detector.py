import argparse
import json
import os
from dataclasses import dataclass

@dataclass
class Framework:
    name: str
    docker_image: str
    env_vars: dict

def detect_framework(script_path):
    with open(script_path, 'r') as f:
        content = f.read()
        try:
            metadata = json.loads(content)
            if 'framework' in metadata:
                if metadata['framework'] == 'PyTorch':
                    return Framework('PyTorch', 'pytorch/pytorch', {'CUDA_VISIBLE_DEVICES': '0'})
                elif metadata['framework'] == 'TensorFlow':
                    return Framework('TensorFlow', 'tensorflow/tensorflow', {'CUDA_VISIBLE_DEVICES': '0'})
        except json.JSONDecodeError:
            pass

        lines = content.splitlines()
        for line in lines:
            if line.startswith('#!'):
                if 'pytorch' in line:
                    return Framework('PyTorch', 'pytorch/pytorch', {'CUDA_VISIBLE_DEVICES': '0'})
                elif 'tensorflow' in line:
                    return Framework('TensorFlow', 'tensorflow/tensorflow', {'CUDA_VISIBLE_DEVICES': '0'})

    return None

def run_job(framework, script_path):
    if framework:
        print(f"Running {framework.name} job with Docker image {framework.docker_image}")
        print(f"Setting environment variables: {framework.env_vars}")
        # Run the job using the detected framework and Docker image
        # For simplicity, this example just prints the command
        print(f"docker run -it --env {','.join(f'{k}={v}' for k, v in framework.env_vars.items())} {framework.docker_image} python {script_path}")
    else:
        print("Failed to detect framework")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('script_path', help='Path to the script')
    args = parser.parse_args()
    framework = detect_framework(args.script_path)
    run_job(framework, args.script_path)
