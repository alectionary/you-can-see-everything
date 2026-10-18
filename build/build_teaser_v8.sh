#!/bin/bash
# Breakdown cut (v8) — picture only. Per EDIT_PLAN.md.
# Sources: v7 clean master (no burned subs), v4 Fielder reaction raw, clips/inserts/*.
set -e
cd ~/workspace/you-can-see-anything-teaser
B=build/v8; mkdir -p $B/seg $B/cards
ENC="-c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -r 24 -an"
BASE=build/v7/video_raw.mp4
REACT=$(ls clips/v4/*fielder-reaction-*.mp4)
SEDAN=$(ls clips/inserts/*rainy-lot-sedan-*.mp4)
FOOD=$(ls clips/inserts/*food-bank-*.mp4)
LOT=$(ls clips/inserts/*empty-lot-after-*.mp4)
DEMO=$(ls clips/inserts/*demolition-*.mp4)
FONT=/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf

seg() { # name start dur filter inputs...
  local name=$1; shift
  ffmpeg -y -v error "$@" $ENC $B/seg/$name.mp4
}
basetrim() { # start dur -> input args for BASE
  echo "-ss $1 -t $2 -i $BASE"
}

# --- plain base windows ---
ffmpeg -y -v error -ss 0 -t 4.5 -i $BASE $ENC $B/seg/w01.mp4
ffmpeg -y -v error -ss 5.75 -t 0.25 -i $BASE $ENC $B/seg/w02.mp4
ffmpeg -y -v error -ss 7.5 -t 2.5 -i $BASE $ENC $B/seg/w03.mp4
ffmpeg -y -v error -ss 12.5 -t 2 -i $BASE $ENC $B/seg/w04.mp4
ffmpeg -y -v error -ss 17.5 -t 3 -i $BASE $ENC $B/seg/w05.mp4
ffmpeg -y -v error -ss 21.75 -t 0.25 -i $BASE $ENC $B/seg/w06.mp4
ffmpeg -y -v error -ss 55 -t 1 -i $BASE $ENC $B/seg/w30.mp4
ffmpeg -y -v error -ss 56 -t 4 -i $BASE $ENC $B/seg/w31.mp4

# --- full-frame inserts (1280x720 -> 1920x1080) ---
ffmpeg -y -v error -ss 1 -t 1.5 -i "$SEDAN" -vf "scale=1920:1080" $ENC $B/seg/insA.mp4
ffmpeg -y -v error -ss 2 -t 2.5 -i "$LOT" -vf "scale=1920:1080" $ENC $B/seg/insB.mp4
ffmpeg -y -v error -ss 1 -t 3 -i "$FOOD" -vf "scale=1920:1080" $ENC $B/seg/insC.mp4

# --- two-panel Roy(right 960) + Fielder(left 960), 22-27.25 ---
ffmpeg -y -v error -ss 0 -t 5.25 -i "$REACT" -ss 22 -t 5.25 -i $BASE -filter_complex "\
[0:v]scale=1920:2880,crop=1920:1080:0:700,crop=960:1080:480:0[L];\
[1:v]crop=960:1080:480:0[R];[L][R]hstack=inputs=2" $ENC $B/seg/panA.mp4
# --- two-panel demolition(left) + Roy(right), 27.25-29.75 ---
ffmpeg -y -v error -ss 3 -t 2.5 -i "$DEMO" -ss 27.25 -t 2.5 -i $BASE -filter_complex "\
[0:v]scale=1920:1080,crop=960:1080:480:0[L];\
[1:v]crop=960:1080:480:0[R];[L][R]hstack=inputs=2" $ENC $B/seg/panB.mp4
# --- two-panel Fielder + Roy, 29.75-30 ---
ffmpeg -y -v error -ss 5.25 -t 0.25 -i "$REACT" -ss 29.75 -t 0.25 -i $BASE -filter_complex "\
[0:v]scale=1920:2880,crop=1920:1080:0:700,crop=960:1080:480:0[L];\
[1:v]crop=960:1080:480:0[R];[L][R]hstack=inputs=2" $ENC $B/seg/panA2.mp4
# --- Dan dominant 1280 + Fielder 640, 30-30.5 and 31.75-34.5 ---
ffmpeg -y -v error -ss 30 -t 0.5 -i $BASE -ss 5.5 -t 0.5 -i "$REACT" -filter_complex "\
[0:v]crop=1280:1080:320:0[L];\
[1:v]scale=1920:2880,crop=1920:1080:0:700,crop=640:1080:640:0[R];[L][R]hstack=inputs=2" $ENC $B/seg/panC.mp4
ffmpeg -y -v error -ss 31.75 -t 2.75 -i $BASE -ss 6 -t 2.75 -i "$REACT" -filter_complex "\
[0:v]crop=1280:1080:320:0[L];\
[1:v]scale=1920:2880,crop=1920:1080:0:700,crop=640:1080:640:0[R];[L][R]hstack=inputs=2" $ENC $B/seg/panC2.mp4
# --- three-panel 34.5-40: food-bank 480 | Fielder reaction 960 | empty lot 480 ---
ffmpeg -y -v error -ss 4 -t 5.5 -i "$FOOD" -ss 34.5 -t 5.5 -i $BASE -ss 5 -t 5.5 -i "$LOT" -filter_complex "\
[0:v]scale=1920:1080,crop=480:1080:720:0[L];\
[1:v]crop=960:1080:480:0[C];\
[2:v]scale=1920:1080,crop=480:1080:720:0[R];[L][C][R]hstack=inputs=3" $ENC $B/seg/panD.mp4
# --- three-panel 41.75-42: lot 480 | Dan 960 | demolition 480 ---
ffmpeg -y -v error -ss 8 -t 0.25 -i "$LOT" -ss 41.75 -t 0.25 -i $BASE -ss 6 -t 0.25 -i "$DEMO" -filter_complex "\
[0:v]scale=1920:1080,crop=480:1080:720:0[L];\
[1:v]crop=960:1080:480:0[C];\
[2:v]scale=1920:1080,crop=480:1080:720:0[R];[L][C][R]hstack=inputs=3" $ENC $B/seg/panE.mp4
# --- stare split with 8px seam offset, 42-47 ---
ffmpeg -y -v error -ss 42 -t 5 -i $BASE -filter_complex "\
[0:v]split=2[a][b];[a]crop=960:1080:0:0[L];[b]crop=960:1072:960:8,scale=960:1080[R];[L][R]hstack=inputs=2" $ENC $B/seg/stare2.mp4
# --- 2x2 grid, 47-48 and 49.75-50 ---
grid4() { # start dur out
  ffmpeg -y -v error -ss $1 -t $2 -i $BASE -filter_complex "\
[0:v]split=4[a][b][c][d];\
[a]crop=1600:900:0:0,scale=960:540[p0];\
[b]crop=1600:900:320:180,scale=960:540[p1];\
[c]crop=1600:900:160:90,scale=960:540[p2];\
[d]crop=1600:900:320:0,scale=960:540[p3];\
[p0][p1][p2][p3]xstack=inputs=4:layout=0_0|960_0|0_540|960_540" $ENC $3
}
grid4 47 1 $B/seg/grid4.mp4
grid4 49.75 0.25 $B/seg/grid4b.mp4
# --- 3x3 grid, 50-50.5 and 51.75-52.5 ---
grid9() { # start dur out
  ffmpeg -y -v error -ss $1 -t $2 -i $BASE -filter_complex "\
[0:v]split=9[a][b][c][d][e][f][g][h][i];\
[a]crop=1600:900:0:0,scale=640:360[p0];\
[b]crop=1600:900:160:90,scale=640:360[p1];\
[c]crop=1600:900:320:180,scale=640:360[p2];\
[d]crop=1600:900:320:0,scale=640:360[p3];\
[e]crop=1600:900:160:45,scale=640:360[p4];\
[f]crop=1600:900:0:180,scale=640:360[p5];\
[g]crop=1600:900:80:135,scale=640:360[p6];\
[h]crop=1600:900:240:90,scale=640:360[p7];\
[i]crop=1600:900:160:180,scale=640:360[p8];\
[p0][p1][p2][p3][p4][p5][p6][p7][p8]xstack=inputs=9:layout=0_0|640_0|1280_0|0_360|640_360|1280_360|0_720|640_720|1280_720" $ENC $3
}
grid9 50 0.5 $B/seg/grid9.mp4
grid9 51.75 0.75 $B/seg/grid9b.mp4
# --- 4x4 mixed grid, 53.5-54 (cells 5=lot, 10=demolition, rest Dan) ---
ffmpeg -y -v error -ss 53.5 -t 0.5 -i $BASE -ss 7 -t 0.5 -i "$LOT" -ss 8 -t 0.5 -i "$DEMO" -filter_complex "\
[0:v]split=14[a][b][c][d][e][f][g][h][i][j][k][l][m][n];\
[a]crop=1600:900:0:0,scale=480:270[p0];\
[b]crop=1600:900:320:180,scale=480:270[p1];\
[c]crop=1600:900:160:0,scale=480:270[p2];\
[d]crop=1600:900:0:180,scale=480:270[p3];\
[e]crop=1600:900:240:90,scale=480:270[p4];\
[f]crop=1600:900:80:45,scale=480:270[p6];\
[g]crop=1600:900:320:90,scale=480:270[p7];\
[h]crop=1600:900:160:180,scale=480:270[p8];\
[i]crop=1600:900:0:90,scale=480:270[p9];\
[j]crop=1600:900:200:135,scale=480:270[p11];\
[k]crop=1600:900:40:0,scale=480:270[p12];\
[l]crop=1600:900:280:45,scale=480:270[p13];\
[m]crop=1600:900:120:180,scale=480:270[p14];\
[n]crop=1600:900:320:135,scale=480:270[p15];\
[1:v]scale=1920:1080,crop=1600:900:160:90,scale=480:270[p5];\
[2:v]scale=1920:1080,crop=1600:900:160:90,scale=480:270[p10];\
[p0][p1][p2][p3][p4][p5][p6][p7][p8][p9][p10][p11][p12][p13][p14][p15]xstack=inputs=16:layout=0_0|480_0|960_0|1440_0|0_270|480_270|960_270|1440_270|0_540|480_540|960_540|1440_540|0_810|480_810|960_810|1440_810" $ENC $B/seg/grid16.mp4

# --- praise cards ---
card() { # out dur text fontsize [linespacing]
  printf '%s' "$3" > $B/cards/$1.txt
  ffmpeg -y -v error -f lavfi -i "color=c=black:s=1920x1080:r=24:d=$2" \
    -vf "drawtext=fontfile=$FONT:textfile=$B/cards/$1.txt:fontsize=$4:fontcolor=0xF5F2EA:x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=${5:-10}" \
    $ENC $B/seg/$1.mp4
}
card card1 1.25 "A NEW DOCUMENTARY BY NATHAN FIELDER" 58
card card2 1.25 "AN EXTRAORDINARY ACT OF LISTENING" 64
card card3 1.25 "A BRAVE NEW LANGUAGE OF TRUTH" 68
card card4 1.75 "CINEMA WILL NEVER BE THE SAME" 76
card card5 1.75 "BEYOND TRUTH. BEYOND CINEMA." 80
card card6 1.25 "A WORK OF IMPOSSIBLE GENIUS" 88
card card7 1.0 "A POSTMODERN MASTERPIECE" 96
printf 'THE GREATEST FILM\nYOU WILL\nEVER SEE IN\nYOUR LIFE' > $B/cards/card8.txt
ffmpeg -y -v error -f lavfi -i "color=c=black:s=1920x1080:r=24:d=1" \
  -vf "drawtext=fontfile=$FONT:textfile=$B/cards/card8.txt:fontsize=110:fontcolor=0xF5F2EA:x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=16" \
  $ENC $B/seg/card8.mp4

# --- concat in master order ---
ORDER="w01 card1 w02 insA w03 insB w04 insC w05 card2 w06 panA panB panA2 panC card3 panC2a panC2b panD card4 panE stare2 grid4 card5 grid4b grid9 card6 grid9b card7 grid16 card8 w30 w31"
: > $B/concat.txt
for s in $ORDER; do echo "file 'seg/$s.mp4'" >> $B/concat.txt; done
ffmpeg -y -v error -f concat -safe 0 -i $B/concat.txt -c copy $B/video_raw.mp4
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 $B/video_raw.mp4
echo "segment durations:"
for s in $ORDER; do printf "%s %s\n" "$s" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 $B/seg/$s.mp4)"; done
