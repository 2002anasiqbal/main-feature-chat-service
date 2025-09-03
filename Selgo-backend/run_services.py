# run_services.py (patched)
import os
import subprocess
import sys
import venv
from pathlib import Path

SERVICES = {
    "auth-service": {"db": "selgo_auth", "port": 8001},
    "boat-service": {"db": "selgo_boat", "port": 8002},
    "car-service": {"db": "selgo_car", "port": 8003},
    "job-service": {"db": "selgo_job", "port": 8004},
    "motorcycle-service": {"db": "selgo_motorcycle", "port": 8005},
    "square-service": {"db": "selgo_square", "port": 8006},
}

PYTHON = sys.executable
BASE_DIR = Path(__file__).resolve().parent

def ensure_pip(venv_python):
    """Ensure pip is installed in the venv."""
    try:
        subprocess.run([str(venv_python), "-m", "pip", "--version"], check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print(f"[WARN] pip missing in {venv_python}, bootstrapping...")
        subprocess.run([str(venv_python), "-m", "ensurepip", "--upgrade"], check=True)
        subprocess.run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], check=True)

def setup_and_run_service(service_name, config):
    service_dir = BASE_DIR / service_name
    venv_dir = service_dir / "venv"
    requirements = service_dir / "requirements.txt"
    main_file = service_dir / "main.py"

    if not venv_dir.exists():
        print(f"[INFO] Creating venv for {service_name}...")
        venv.EnvBuilder(with_pip=True).create(venv_dir)

    venv_python = venv_dir / "Scripts" / "python.exe"

    # 🔑 Ensure pip is available
    ensure_pip(venv_python)

    if requirements.exists():
        print(f"[INFO] Installing requirements for {service_name}...")
        subprocess.run([str(venv_python), "-m", "pip", "install", "-r", str(requirements)], check=True)

    env = os.environ.copy()
    env["DATABASE_URL"] = f"postgresql://postgres:selgo123@localhost:5432/{config['db']}"

    print(f"[INFO] Starting {service_name} on port {config['port']}...")
    subprocess.Popen([str(venv_python), str(main_file)], cwd=service_dir, env=env)

def main():
    for service_name, config in SERVICES.items():
        setup_and_run_service(service_name, config)

    print("[INFO] All services started successfully. (CTRL+C to stop)")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down services...")

if __name__ == "__main__":
    main()
