# Karaokify

A simple CLI tool written in Python to strip out vocals from audio tracks, effectively creating a karaoke version of your favorite songs.

## How It Works

Karaokify uses a technique called phase inversion to remove vocals from stereo audio tracks. It works by:
1. **Splitting** the audio into left and right channels.
2. **Inverting** the phase of the left channel.
3. **Recombining** the channels into a mono track, where the vocals (usually centered) are significantly attenuated.

This results in that cheap old karaoke effect you've probably heard all too many times before.

## Getting started
To check for and install prerequisites before using the program for the first rime run it using the `--setup` option

i.e. `python karaokify.py --setup`

This command will Install necessary Python packages (pydub, numpy) if they are not already installed.
Check for the presence of ffmpeg and prompt you to install it if it's not found.

## Usage
To process an audiofile and create a 'karaoke version', use the following command "python karaokify InputFile.mp3" 
This will add the _karaoked suffix to the output file.

If you wish to specify a different name for the output file you can use the `--output` option 

e.g. `python karaokify.py InputFile.mp3 --output CustomName` 

Which would then output `CustomName.mp3`

If you wish to specify a different output format you can do this using the `--format`  option
Which would let you pick, according to the pydub documentations, ["anything ffmpeg supports"](https://ffmpeg.org//general.html#File-Formats) 
but most importantly, formats like wav, flac, ogg and mp3 are supported.
E.g. `python karaokify.py InputFile.mp3 --format ogg`

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Dependencies

- **pydub**: MIT License. [Link to pydub license](https://github.com/jiaaro/pydub/blob/master/LICENSE)
- **numpy**: BSD License. [Link to numpy license](https://numpy.org/doc/stable/license.html)
- **ffmpeg**: LGPL/GPL. [Link to ffmpeg license](https://ffmpeg.org/legal.html)


