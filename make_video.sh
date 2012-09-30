#!/bin/bash
if [ $# -ne 4 ]; then
    echo "usage: `basename $0` art.jpg input.wav duration_seconds song_name"
    exit 1
fi
# example: ./artwork/SGFs_digital_art_movie_704_576.jpg
art_src=$1
input=$2
duration=$3
song=$4
art="${song}_art.mpg"
vid="${song}.mpg"
ffmpeg -loop_input -t $duration -i "$art_src" "$art"
ffmpeg -i "$input" -i "$art" -vcodec copy "$vid"
rm "$art"
echo "ready: $vid"
