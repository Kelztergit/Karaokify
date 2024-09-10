import argparse
import subprocess
import sys
import importlib.util
from pydub import AudioSegment
import numpy as np

__description__ = "Karaokify - a tool to make songs ready for karaoke, quick and lazy "



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
    parser.add_argument("--format", help="Output audio format (e.g., mp3, wav, see : https://ffmpeg.org//general.html#File-Formats). mp3 is selected by default", default="mp3")
   #removed --setup argument, this hybrid approach didn't work as intended and was just a headache, now using seperate prereq installer script.

    args = parser.parse_args()

    
    # Ensure an input file is provided (before processing audio)
    if not args.input_file:
        print("Error: Input file is required For more information, use the -h argument.")
        sys.exit(1)

   
    # Default output file name with '_karaoked' suffix if not provided
    output_file = args.output or args.input_file.rsplit(".", 1)[0] + "_karaoked"

    # Process the audio file
    process_audio(args.input_file, output_file, args.format)

def invert_left_channel_and_recombine(audio):
    """Invert the left channel and recombine it with the right channel."""
    
    left_channel, right_channel = audio.split_to_mono()

    # Invert the left channel
    inverted_left_channel = np.array(left_channel.get_array_of_samples()) * -1
    inverted_left_channel = left_channel._spawn(inverted_left_channel.tobytes())

    # Recombine left and right channels
    return AudioSegment.from_mono_audiosegments(inverted_left_channel, right_channel)

if __name__ == "__main__":
    main()
