import subprocess


try:
    result = subprocess.run(
        "echo 'hi' && sleep 30",
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=5,
        shell=True,
    )
except subprocess.TimeoutExpired as exc:
    pass
