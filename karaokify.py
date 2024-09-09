import argparse
import subprocess
import sys
import importlib.util
import numpy as np
from pydub import AudioSegment

__description__ = "Karaokify - a tool to make songs ready for karaoke, quick and lazy "

def check_and_install_package(package_name):
    """Check if a package is installed, and install it if not."""
    if importlib.util.find_spec(package_name) is None:
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
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
    check_and_install_package('pydub')
    check_and_install_package('numpy')
    check_ffmpeg_installed()

def invert_left_channel_and_recombine(audio):
    """Invert the left channel and recombine it with the right channel."""
    left_channel, right_channel = audio.split_to_mono()
    
    # Invert the left channel
    inverted_left_channel = np.array(left_channel.get_array_of_samples()) * -1
    inverted_left_channel = left_channel._spawn(inverted_left_channel.tobytes())
    
    # Recombine left and right channels
    return AudioSegment.from_mono_audiosegments(inverted_left_channel, right_channel)

def process_audio(input_file, output_file, output_format):
    """Process the input audio file: invert left channel, mix to mono, and save the output."""
    audio = AudioSegment.from_file(input_file)

    if audio.channels != 2:
        print(f"Error: {input_file} is not a stereo audio file.")
        return

    # Invert left channel and recombine
    stereo_output = invert_left_channel_and_recombine(audio)
    
    # Mix stereo to mono
    mono_output = stereo_output.set_channels(1)

    # Ensure the output file has the correct format suffix
    if not output_file.lower().endswith(f".{output_format}"):
        output_file += f".{output_format}"

    # Export the output file
    mono_output.export(output_file, format=output_format)
    print(f"Processed mono audio saved as: {output_file}")

def main():
    """Main function to parse arguments and run the appropriate functions."""
    parser = argparse.ArgumentParser(description="Karaokify : A simple karaoke audio processor using phase inversion.\n\n"
                    "Usage examples:\n"
                    "  python karaokify.py InputSong.mp3\n"
                    "  which outputs InputSong_karaoked.mp3\n" 
                    "  python karaokify.py InputSong.mp3 --output OutputSong --format wav\n"
                    "  which outputs OutputSong.wav",
            
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("input_file", nargs='?', help="Input audio file (e.g., InputSong.mp3)")
    parser.add_argument("--output", help="Optional output file name (e.g. --output OutputSong)", default=None)
    parser.add_argument("--format", help="Output audio format (e.g., mp3, wav, see : https://ffmpeg.org//general.html#File-Formats) mp3 is selected by default", default="mp3")
    parser.add_argument("--setup", action="store_true", help="Check for and then install dependencies if required")

    args = parser.parse_args()

    # Handle --setup argument
    if args.setup:
        install_prerequisites()
        print("Dependencies have been installed.")
        return  # Exit after installing prerequisites

    # Ensure an input file is provided if not setting up prerequisites
    if not args.input_file:
        print("Error: Input file is required unless using --setup. For more information on usage use the -h argument")
        sys.exit(1)

    # Default output file name with '_karaoked' suffix if not provided
    output_file = args.output or args.input_file.rsplit(".", 1)[0] + "_karaoked"

    # Process the audio file
    process_audio(args.input_file, output_file, args.format)

if __name__ == "__main__":
    main()
