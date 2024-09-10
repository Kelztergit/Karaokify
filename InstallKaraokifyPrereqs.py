import subprocess
import sys
import importlib.util

__description__ = "Karaokify prerequisite installer - a tool to check for and install the prerequisites."

def check_and_install_package(package_name):
    """Check if a package is installed, and install it if not."""
    if importlib.util.find_spec(package_name) is None:
        print(f"Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package_name}: {e}")
            sys.exit(1)
    else:
        print(f"{package_name} is already installed.")

def check_ffmpeg_installed():
    """Check if ffmpeg is installed, required for audio format processing."""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("ffmpeg is installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ffmpeg not found. Please install it from https://ffmpeg.org/download.html.")
        sys.exit(1)

def install_prerequisites():
    """Install required Python packages and ensure ffmpeg is present."""
    print("Checking and installing Python packages...")
    check_and_install_package('pydub')
    check_and_install_package('numpy')
    print("Checking for ffmpeg...")
    check_ffmpeg_installed()

def main():
    """Main function to handle the execution."""
    install_prerequisites()

if __name__ == "__main__":
    main()
