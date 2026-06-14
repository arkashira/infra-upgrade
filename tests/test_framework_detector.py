import pytest
from framework_detector import detect_framework, Framework

def test_detect_framework_pytorch_shebang(tmp_path):
    script_path = tmp_path / 'script.py'
    with open(script_path, 'w') as f:
        f.write('#!/usr/bin/env pytorch\n')
    framework = detect_framework(script_path)
    assert framework.name == 'PyTorch'
    assert framework.docker_image == 'pytorch/pytorch'
    assert framework.env_vars == {'CUDA_VISIBLE_DEVICES': '0'}

def test_detect_framework_tensorflow_shebang(tmp_path):
    script_path = tmp_path / 'script.py'
    with open(script_path, 'w') as f:
        f.write('#!/usr/bin/env tensorflow\n')
    framework = detect_framework(script_path)
    assert framework.name == 'TensorFlow'
    assert framework.docker_image == 'tensorflow/tensorflow'
    assert framework.env_vars == {'CUDA_VISIBLE_DEVICES': '0'}

def test_detect_framework_pytorch_metadata(tmp_path):
    script_path = tmp_path / 'script.py'
    with open(script_path, 'w') as f:
        f.write('{"framework": "PyTorch"}\n')
    framework = detect_framework(script_path)
    assert framework.name == 'PyTorch'
    assert framework.docker_image == 'pytorch/pytorch'
    assert framework.env_vars == {'CUDA_VISIBLE_DEVICES': '0'}

def test_detect_framework_tensorflow_metadata(tmp_path):
    script_path = tmp_path / 'script.py'
    with open(script_path, 'w') as f:
        f.write('{"framework": "TensorFlow"}\n')
    framework = detect_framework(script_path)
    assert framework.name == 'TensorFlow'
    assert framework.docker_image == 'tensorflow/tensorflow'
    assert framework.env_vars == {'CUDA_VISIBLE_DEVICES': '0'}

def test_detect_framework_none(tmp_path):
    script_path = tmp_path / 'script.py'
    with open(script_path, 'w') as f:
        f.write('Hello World!\n')
    framework = detect_framework(script_path)
    assert framework is None
