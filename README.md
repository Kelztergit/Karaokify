# Karaokify

A simple CLI tool written in Python to strip out vocals from audio tracks, effectively creating a karaoke version of your favorite songs.

## How It Works

Karaokify uses a technique called phase inversion to remove vocals from stereo audio tracks. It works by:
1. **Splitting** the audio into left and right channels.
2. **Inverting** the phase of the left channel.
3. **Recombining** the channels into a mono track, where the vocals (usually centered) are significantly attenuated.

This results in that cheap old karaoke effect you've probably heard all too many times before.
### Why It Works

This method is effective because it exploits the fact that vocals are typically centered in the stereo mix, while instruments are often panned to the left or right. By inverting the phase of one channel and combining it with the other, the central vocals cancel out due to phase interference, leaving behind the instrumental tracks.

### When It Doesn’t Work

This technique may not be effective in the following scenarios:
- **Non-Centered Vocals:** If the vocals are panned to one side, they will not be adequately removed.
- **Mono Tracks:** If the audio is mono or does not have distinct left and right channels, phase inversion cannot be applied.
- **Instrumental Centering:** If instrumental parts are also centered, they will be attenuated along with the vocals.
- **Uneven Mixing:** Variations in how the original audio is mixed can impact the effectiveness of this method.



## Getting started
To check for and install prerequisites before using the program for the first time run the `setup.py` script

i.e. `python setup.py`

This script will Install necessary Python packages (pydub, numpy) if they are not already installed.
Check for the presence of ffmpeg and prompt you to install it if it's not found.

## Usage
To process an audiofile and create a 'karaoke version', use the following command `python karaokify.py InputFile.mp3`

This will process the file and add the _karaoked suffix to the output file's name `InputFile_karaoked.mp3`.

If the Input file is located in a different location use the full location within quotation marks `python karaokify.py "C:\MusicLocation\InputFile.mp3"`
It will output the song next to it.

If you wish to specify a different name for the output file you can use the `--output` option 

e.g. `python karaokify.py InputFile.mp3 --output CustomName` 

Which would then output `CustomName.mp3`

If you wish to specify a different output format than mp3, which is the default, you can do this using the `--format`  option
Which would let you pick, according to the pydub documentations, ["anything ffmpeg supports"](https://ffmpeg.org//general.html#File-Formats) 
but most importantly, formats like wav, flac, ogg and mp3 are all supported.
E.g. `python karaokify.py InputFile.mp3 --format ogg`
would output `InputFile_karaoked.ogg`

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Dependencies

- **pydub**: MIT License. [Link to pydub license](https://github.com/jiaaro/pydub/blob/master/LICENSE)
- **numpy**: BSD License. [Link to numpy license](https://numpy.org/doc/stable/license.html)
- **ffmpeg**: LGPL/GPL. [Link to ffmpeg license](https://ffmpeg.org/legal.html)


