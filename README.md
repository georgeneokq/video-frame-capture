## Overview

A simple console program to capture and export the frames of a video.

## Usage

{FILE_PATH} is a required positional argument.

`-c` is an optional argument specifying frames to capture per second. Default: 2

`-q` is an optional argument, specifying quality of frames exported, in percentage. Default: 100

```
python main.py {FILE_PATH} -c {CAPTURES_PER_SECOND}
```