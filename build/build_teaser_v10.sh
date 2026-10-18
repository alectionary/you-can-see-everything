#!/bin/bash
# V10 picture build — per EDIT_PLAN_V10.md (71.000s, 26 segments, all >= 2.000s).
set -e
cd ~/workspace/you-can-see-anything-teaser
B=build/v10; mkdir -p $B/seg $B/cards $B/tmp
ENC="-c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -r 24 -an"
F01=$(ls clips/v2/*shot01-*.mp4)
D02=$(ls clips/v3/*shot02-*.mp4)
D03=$(ls clips/v3/*shot03-*.mp4)
ROY=$(ls clips/v4/*shot04-*.mp4)
D05=$(ls clips/v3/*shot05-*.mp4)
D06=$(ls clips/v3/*shot06-*.mp4)
REACT=$(ls clips/v4/*fielder-reaction-*.mp4)
SEDAN=$(ls clips/inserts/*rainy-lot-sedan-*.mp4)
FOOD=$(ls clips/inserts/*food-bank-*.mp4)
LOT=$(ls clips/inserts/*empty-lot-after-*.mp4)
DEMO=$(ls clips/inserts/*demolition-*.mp4)
FONT=/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf
DANFRAME="scale=1920:1920,crop=1920:1080:0:420"
TALLFRAME="scale=1920:2880,crop=1920:1080:0:700"

# corrected head streams (v7 glitch fixes), reused by several segments
ffmpeg -y -v error -ss 0.35 -i "$F01" -vf "scale=1920:2880,crop=1920:1080:0:420,tpad=start_mode=clone:start_duration=0.35,trim=0:8,setpts=PTS-STARTPTS" $ENC $B/tmp/f01c.mp4
ffmpeg -y -v error -ss 0.30 -i "$ROY" -vf "$TALLFRAME,tpad=start_mode=clone:start_duration=0.30,trim=0:8,setpts=PTS-STARTPTS" $ENC $B/tmp/royc.mp4

# S01 0-4 Fielder full frame (corrected source 0-4)
ffmpeg -y -v error -ss 0 -t 4 -i $B/tmp/f01c.mp4 $ENC $B/seg/S01.mp4
# S03 6-8 sedan insert, source 1-3
ffmpeg -y -v error -ss 1 -t 2 -i "$SEDAN" -vf "scale=1920:1080" $ENC $B/seg/S03.mp4
# S04 8-10 Dan (shot02 source 2-4)
ffmpeg -y -v error -ss 2 -t 2 -i "$D02" -vf "$DANFRAME" $ENC $B/seg/S04.mp4
# S05 10-12.5 empty lot, source 2-4.5
ffmpeg -y -v error -ss 2 -t 2.5 -i "$LOT" -vf "scale=1920:1080" $ENC $B/seg/S05.mp4
# S06 12.5-14.5 Dan (shot03 source 0-2)
ffmpeg -y -v error -ss 0 -t 2 -i "$D03" -vf "$DANFRAME" $ENC $B/seg/S06.mp4
# S07 14.5-17 food bank, source 1-3.5
ffmpeg -y -v error -ss 1 -t 2.5 -i "$FOOD" -vf "scale=1920:1080" $ENC $B/seg/S07.mp4
# S08 17-20 Dan (shot03 source 3-6)
ffmpeg -y -v error -ss 3 -t 3 -i "$D03" -vf "$DANFRAME" $ENC $B/seg/S08.mp4
# S10 22-27 two-panel: Fielder reaction L (0-5) | Roy R blurred-pad full frame (corrected 0-5)
ffmpeg -y -v error -ss 0 -t 5 -i "$REACT" -ss 0 -t 5 -i $B/tmp/royc.mp4 -filter_complex "\
[0:v]scale=1920:2880,crop=1920:1080:0:700,crop=960:1080:480:0[L];\
[1:v]split=2[ra][rb];[ra]scale=960:1080,gblur=sigma=40,eq=brightness=-0.3[bg];[rb]scale=960:540[fg];[bg][fg]overlay=0:270[R];[L][R]hstack=inputs=2" $ENC $B/seg/S10.mp4
# S11 27-30 two-panel: demolition L (3-6) | Roy R (corrected 5-8)
ffmpeg -y -v error -ss 3 -t 3 -i "$DEMO" -ss 5 -t 3 -i $B/tmp/royc.mp4 -filter_complex "\
[0:v]scale=1920:1080,crop=960:1080:480:0[L];\
[1:v]split=2[ra][rb];[ra]scale=960:1080,gblur=sigma=40,eq=brightness=-0.3[bg];[rb]scale=960:540[fg];[bg][fg]overlay=0:270[R];[L][R]hstack=inputs=2" $ENC $B/seg/S11.mp4
# S13 32-34.5 Dan dominant 1280 (shot05 source 2-4.5) + reaction 640 (0-2.5)
ffmpeg -y -v error -ss 2 -t 2.5 -i "$D05" -ss 0 -t 2.5 -i "$REACT" -filter_complex "\
[0:v]scale=1920:1920,crop=1920:1080:0:420,crop=1280:1080:320:0[L];\
[1:v]scale=1920:2880,crop=1920:1080:0:700,crop=640:1080:640:0[R];[L][R]hstack=inputs=2" $ENC $B/seg/S13.mp4
# S14 34.5-39.5 three-panel: food 480 (4-9) | reaction 960 (0-5) | lot 480 (5-10)
ffmpeg -y -v error -ss 4 -t 5 -i "$FOOD" -ss 0 -t 5 -i "$REACT" -ss 5 -t 5 -i "$LOT" -filter_complex "\
[0:v]scale=1920:1080,crop=480:1080:720:0[L];\
[1:v]scale=1920:2880,crop=1920:1080:0:700,crop=960:1080:480:0[C];\
[2:v]scale=1920:1080,crop=480:1080:720:0[R];[L][C][R]hstack=inputs=3" $ENC $B/seg/S14.mp4
# S16 42-47 split stare, 8px seam (shot06 source 0-5)
ffmpeg -y -v error -ss 0 -t 5 -i "$D06" -filter_complex "\
[0:v]scale=1920:1920,crop=1920:1080:0:420,split=2[a][b];[a]crop=960:1080:0:0[L];[b]crop=960:1072:960:8,scale=960:1080[R];[L][R]hstack=inputs=2" $ENC $B/seg/S16.mp4
# grids from framed Dan stare take
grid4() { ffmpeg -y -v error -ss $1 -t $2 -i "$D06" -filter_complex "\
[0:v]scale=1920:1920,crop=1920:1080:0:420,split=4[a][b][c][d];\
[a]crop=1600:900:0:0,scale=960:540[p0];[b]crop=1600:900:320:180,scale=960:540[p1];\
[c]crop=1600:900:160:90,scale=960:540[p2];[d]crop=1600:900:320:0,scale=960:540[p3];\
[p0][p1][p2][p3]xstack=inputs=4:layout=0_0|960_0|0_540|960_540" $ENC $3; }
grid9() { ffmpeg -y -v error -ss $1 -t $2 -i "$D06" -filter_complex "\
[0:v]scale=1920:1920,crop=1920:1080:0:420,split=9[a][b][c][d][e][f][g][h][i];\
[a]crop=1600:900:0:0,scale=640:360[p0];[b]crop=1600:900:160:90,scale=640:360[p1];\
[c]crop=1600:900:320:180,scale=640:360[p2];[d]crop=1600:900:320:0,scale=640:360[p3];\
[e]crop=1600:900:160:45,scale=640:360[p4];[f]crop=1600:900:0:180,scale=640:360[p5];\
[g]crop=1600:900:80:135,scale=640:360[p6];[h]crop=1600:900:240:90,scale=640:360[p7];\
[i]crop=1600:900:160:180,scale=640:360[p8];\
[p0][p1][p2][p3][p4][p5][p6][p7][p8]xstack=inputs=9:layout=0_0|640_0|1280_0|0_360|640_360|1280_360|0_720|640_720|1280_720" $ENC $3; }
grid16() { # dan_ss dan_dur lot_ss demo_ss out
  ffmpeg -y -v error -ss $1 -t $2 -i "$D06" -ss $3 -t $2 -i "$LOT" -ss $4 -t $2 -i "$DEMO" -filter_complex "\
[0:v]scale=1920:1920,crop=1920:1080:0:420,split=14[a][b][c][d][e][f][g][h][i][j][k][l][m][n];\
[a]crop=1600:900:0:0,scale=480:270[p0];[b]crop=1600:900:320:180,scale=480:270[p1];\
[c]crop=1600:900:160:0,scale=480:270[p2];[d]crop=1600:900:0:180,scale=480:270[p3];\
[e]crop=1600:900:240:90,scale=480:270[p4];[f]crop=1600:900:80:45,scale=480:270[p6];\
[g]crop=1600:900:320:90,scale=480:270[p7];[h]crop=1600:900:160:180,scale=480:270[p8];\
[i]crop=1600:900:0:90,scale=480:270[p9];[j]crop=1600:900:200:135,scale=480:270[p11];\
[k]crop=1600:900:40:0,scale=480:270[p12];[l]crop=1600:900:280:45,scale=480:270[p13];\
[m]crop=1600:900:120:180,scale=480:270[p14];[n]crop=1600:900:320:135,scale=480:270[p15];\
[1:v]scale=1920:1080,crop=1600:900:160:90,scale=480:270[p5];\
[2:v]scale=1920:1080,crop=1600:900:160:90,scale=480:270[p10];\
[p0][p1][p2][p3][p4][p5][p6][p7][p8][p9][p10][p11][p12][p13][p14][p15]xstack=inputs=16:layout=0_0|480_0|960_0|1440_0|0_270|480_270|960_270|1440_270|0_540|480_540|960_540|1440_540|0_810|480_810|960_810|1440_810" $ENC $5; }
grid4 5 2 $B/seg/S17.mp4
grid9 7 3 $B/seg/S19.mp4
grid16 7 2.5 5 3 $B/seg/S21.mp4
grid16 5 2 7.5 5.5 $B/seg/S23.mp4

# cards (white on black, sizes escalate as v8)
card() { printf '%s' "$3" > $B/cards/$1.txt; ffmpeg -y -v error -f lavfi -i "color=c=black:s=1920x1080:r=24:d=$2" \
  -vf "drawtext=fontfile=$FONT:textfile=$B/cards/$1.txt:fontsize=$4:fontcolor=0xF5F2EA:x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=${5:-10}" $ENC $B/seg/$1.mp4; }
card S02 2 "A NEW DOCUMENTARY BY NATHAN FIELDER" 58
card S09 2 "AN EXTRAORDINARY ACT OF LISTENING" 64
card S12 2 "A BRAVE NEW LANGUAGE OF TRUTH" 68
card S15 2.5 "CINEMA WILL NEVER BE THE SAME" 76
card S18 2 "BEYOND TRUTH. BEYOND CINEMA." 80
card S20 2 "A WORK OF IMPOSSIBLE GENIUS" 88
card S22 2 "A POSTMODERN MASTERPIECE" 96
printf 'THE GREATEST FILM\nYOU WILL\nEVER SEE IN\nYOUR LIFE' > $B/cards/S24.txt
ffmpeg -y -v error -f lavfi -i "color=c=black:s=1920x1080:r=24:d=2.5" \
  -vf "drawtext=fontfile=$FONT:textfile=$B/cards/S24.txt:fontsize=110:fontcolor=0xF5F2EA:x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=16" $ENC $B/seg/S24.mp4
# S25 black 2s; S26 title 4s (v7 title recipe, new text)
ffmpeg -y -v error -f lavfi -i "color=c=black:s=1920x1080:r=24:d=2" $ENC $B/seg/S25.mp4
ffmpeg -y -v error -f lavfi -i "color=black:s=1920x1080:r=24:d=4" -vf "drawtext=fontfile=/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf:text='YOU CAN SEE EVERYTHING':fontsize=64:fontcolor=0xE6E4DF:x=(w-text_w)/2:y=(h-text_h)/2" $ENC $B/seg/S26.mp4

ORDER="S01 S02 S03 S04 S05 S06 S07 S08 S09 S10 S11 S12 S13 S14 S15 S16 S17 S18 S19 S20 S21 S22 S23 S24 S25 S26"
: > $B/concat.txt
for s in $ORDER; do echo "file 'seg/$s.mp4'" >> $B/concat.txt; done
ffmpeg -y -v error -f concat -safe 0 -i $B/concat.txt -c copy $B/video_raw.mp4
echo "total: $(ffprobe -v error -show_entries format=duration -of csv=p=0 $B/video_raw.mp4)"
for s in $ORDER; do printf "%s %s\n" "$s" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 $B/seg/$s.mp4)"; done
