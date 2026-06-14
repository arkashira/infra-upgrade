import pytest
from infra_cli import InfraCLI, Script
import io
import sys

def test_import_script(tmp_path):
    script_path = tmp_path / "script.py"
    script_path.write_text("print('Hello World')")
    infra_cli = InfraCLI()
    infra_cli.import_script(str(script_path))
    # Check logs
    logs = infra_cli.get_logs()
    assert "Importing script from" in logs
    assert "Uploading script" in logs
    assert "Uploaded script to cluster" in logs
    assert "Streaming logs for script" in logs
    assert "Log 1" in logs
    assert "Log 2" in logs
    assert "Log 3" in logs

def test_upload_script(tmp_path):
    script_path = tmp_path / "script.py"
    script_path.write_text("print('Hello World')")
    infra_cli = InfraCLI()
    script = Script(path=str(script_path), framework_version="latest")
    infra_cli.upload_script(script)
    # Check logs
    logs = infra_cli.get_logs()
    assert "Uploading script" in logs
    assert "Uploaded script to cluster" in logs

def test_stream_logs(tmp_path):
    script_path = tmp_path / "script.py"
    script_path.write_text("print('Hello World')")
    infra_cli = InfraCLI()
    script = Script(path=str(script_path), framework_version="latest")
    infra_cli.stream_logs(script)
    # Check logs
    logs = infra_cli.get_logs()
    assert "Streaming logs for script" in logs
    assert "Log 1" in logs
    assert "Log 2" in logs
    assert "Log 3" in logs

def test_create_docker_container():
    infra_cli = InfraCLI()
    script_content = "print('Hello World')"
    framework_version = "latest"
    docker_container = infra_cli.create_docker_container(script_content, framework_version)
    assert docker_container == "docker-container-latest"
