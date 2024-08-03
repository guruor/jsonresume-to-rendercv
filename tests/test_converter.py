import os
import subprocess
import requests
import yaml

# Sample resume from resume-schema repo
SAMPLE_RESUME_URL = "https://raw.githubusercontent.com/jsonresume/resume-schema/master/sample.resume.json"

INPUT_FILE = "sample.resume.json"
OUTPUT_FILE = "output.resume.yaml"


def download_sample_resume():
    response = requests.get(SAMPLE_RESUME_URL)
    response.raise_for_status()
    with open(INPUT_FILE, "wb") as file:
        file.write(response.content)


def run_converter():
    result = subprocess.run(
        ["jsonresume_to_rendercv", INPUT_FILE, OUTPUT_FILE],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result.returncode == 0


def validate_output():
    with open(OUTPUT_FILE, "rb") as file:
        content = yaml.safe_load(file.read().decode('utf-8'))

    # Perform basic validation checks on the output content
    assert "cv" in content, "Output does not contain 'cv' section"
    assert "name" in content["cv"], "Output does not contain 'name' field"


def setup_module(module):
    """Setup any state specific to the execution of the given module."""
    download_sample_resume()


def teardown_module(module):
    """Teardown any state that was previously setup with a setup_module
    method.
    """
    if os.path.exists(INPUT_FILE):
        os.remove(INPUT_FILE)
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)


def test_download_sample_resume():
    download_sample_resume()
    assert os.path.exists(INPUT_FILE), "Sample resume file was not downloaded."


def test_run_converter():
    assert run_converter(), "Conversion failed."


def test_validate_output():
    validate_output()
