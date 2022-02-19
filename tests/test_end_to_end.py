from collections import namedtuple
from glob import glob
from pathlib import Path


def test_end_to_end(script_runner, mocker, request):
    package_versions = {
        "librosa": "0.9.1",
        "pillow": "9.0.1",
        "pesq": "0.0.3",
    }
    mock_release = namedtuple("MockRelease", ["latest_release_id"])
    mocker.patch(
        "yarg.get",
        side_effect=lambda arg: mock_release(package_versions[arg]),
    )

    cwd = Path(__file__).parent
    fixture_dirs = glob(str(cwd / "fixtures" / "*"))
    for fixture_dir in fixture_dirs:
        fixture_dir = Path(fixture_dir)
        project_dir = fixture_dir / "project"
        script_runner.run("cogreqs", str(project_dir))
        config_path = project_dir / "cog.yaml"
        assert_files_match(config_path, fixture_dir / "expected" / "cog.yaml")
        assert (project_dir / "predict.py").exists()

        request.addfinalizer(lambda: delete_generated_files(project_dir))


def assert_files_match(path1, path2):
    with open(path1) as f1:
        contents1 = f1.read()
    with open(path2) as f2:
        contents2 = f2.read()
    assert contents1 == contents2


def delete_generated_files(project_dir):
    if (project_dir / "cog.yaml").exists():
        (project_dir / "cog.yaml").unlink()
    if (project_dir / "predict.py").exists():
        (project_dir / "predict.py").unlink()
