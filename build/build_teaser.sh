#!/bin/bash
set -e
cd ~/workspace/you-can-see-anything-teaser
B=build; mkdir -p $B
C1=$(ls clips/*shot01-*.mp4); C2=$(ls clips/*shot02-*.mp4); C3=$(ls clips/*shot03-*.mp4)
C4=$(ls clips/*shot04-*.mp4); C5=$(ls clips/*shot05-*.mp4); C6=$(ls clips/*shot06-*.mp4)
ENC="-c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -r 24 -an"

# --- video segments (1920x1080, 24fps, no audio) ---
ffmpeg -y -v error -i "$C1" -vf "scale=1920:2880,crop=1920:1080:0:700,trim=0:6,setpts=PTS-STARTPTS" $ENC $B/seg01.mp4
ffmpeg -y -v error -i "$C2" -vf "scale=1920:1920,crop=1920:1080:0:420,trim=0:8,setpts=PTS-STARTPTS" $ENC $B/seg02.mp4
ffmpeg -y -v error -i "$C3" -vf "scale=1920:1080,trim=0:8,setpts=PTS-STARTPTS" $ENC $B/seg03.mp4
ffmpeg -y -v error -i "$C4" -vf "scale=1920:2880,crop=1920:1080:0:700,trim=0:8,setpts=PTS-STARTPTS" $ENC $B/seg04.mp4
ffmpeg -y -v error -i "$C5" -vf "scale=1920:1920,crop=1920:1080:0:420,tpad=stop_mode=clone:stop_duration=2,trim=0:12,setpts=PTS-STARTPTS" $ENC $B/seg05.mp4
ffmpeg -y -v error -i "$C6" -vf "scale=1920:1920,crop=1920:1080:0:420,tpad=stop_mode=clone:stop_duration=3,trim=0:13,setpts=PTS-STARTPTS" $ENC $B/seg06.mp4
ffmpeg -y -v error -f lavfi -i color=black:s=1920x1080:r=24:d=1 $ENC $B/seg07.mp4
ffmpeg -y -v error -f lavfi -i color=black:s=1920x1080:r=24:d=4 -vf "drawtext=fontfile=/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf:text='YOU CAN SEE ANYTHING':fontsize=64:fontcolor=0xE6E4DF:x=(w-text_w)/2:y=(h-text_h)/2" $ENC $B/seg08.mp4
printf "file 'seg01.mp4'\nfile 'seg02.mp4'\nfile 'seg03.mp4'\nfile 'seg04.mp4'\nfile 'seg05.mp4'\nfile 'seg06.mp4'\nfile 'seg07.mp4'\nfile 'seg08.mp4'\n" > $B/concat.txt
ffmpeg -y -v error -f concat -safe 0 -i $B/concat.txt -c copy $B/video_raw.mp4

# --- captions ---
cat > $B/teaser.srt <<'SRT'
1
00:00:01,500 --> 00:00:04,380
Removing the food bank was justified?

2
00:00:08,000 --> 00:00:09,488
The use was permitted.

3
00:00:14,400 --> 00:00:16,430
Why did people lose access?

4
00:00:18,000 --> 00:00:19,968
I can't account for their interpretation.

5
00:00:23,000 --> 00:00:25,688
Ever wondered if Dan was misleading you?

6
00:00:26,000 --> 00:00:27,774
Never. Not once.

7
00:00:32,000 --> 00:00:33,608
I'm answering you personally.

8
00:00:35,000 --> 00:00:36,160
Why misrepresent it?

9
00:00:37,000 --> 00:00:38,968
The space accommodates my sedan.

10
00:00:42,500 --> 00:00:44,468
Is that your honest answer?

11
00:00:45,000 --> 00:00:46,608
My answer hasn't changed.
SRT

# --- audio: score (per MUSIC_CUES.md) + dialogue ---
ffmpeg -y -v error \
 -f lavfi -i "anoisesrc=color=white:seed=2718:d=55" \
 -f lavfi -i "sine=frequency=60:d=55" \
 -f lavfi -i "sine=frequency=43.65:d=22" \
 -f lavfi -i "aevalsrc=exprs='(sin(2*PI*174.61*t)+0.35*sin(2*PI*349.22*t)+0.12*sin(2*PI*523.83*t)+0.04*sin(2*PI*698.44*t))/1.51*if(lt(t\,0.008)\,t/0.008\,exp(-(t-0.008)/0.65))*if(gt(t\,2.85)\,(3-t)/0.15\,1)':d=3:s=48000" \
 -f lavfi -i "aevalsrc=exprs='(sin(2*PI*130.81*t)+0.35*sin(2*PI*261.62*t)+0.12*sin(2*PI*392.43*t)+0.04*sin(2*PI*523.24*t))/1.51*if(lt(t\,0.008)\,t/0.008\,exp(-(t-0.008)/0.45))*if(gt(t\,1.85)\,(2-t)/0.15\,1)':d=2:s=48000" \
 -i dialogue/f01.mp3 -i dialogue/d01.mp3 -i dialogue/f02.mp3 -i dialogue/d02.mp3 \
 -i dialogue/f03.mp3 -i dialogue/r01.mp3 -i dialogue/d03.mp3 -i dialogue/d04.mp3 \
 -i dialogue/d05.mp3 -i dialogue/f04.mp3 -i dialogue/d06.mp3 \
 -filter_complex "\
[0:a]highpass=f=100,lowpass=f=3000,volume=-48dB,aresample=48000[a0]; \
[1:a]volume=-66dB,aresample=48000[a1]; \
[2:a]volume='if(lt(t,6),(1-cos(PI*t/6))/2,if(gt(t,16),(1-cos(PI*(22-t)/6))/2,1))':eval=frame,volume=-42dB,adelay=18000|18000[a2]; \
[3:a]volume=-35dB,adelay=11000|11000[a3]; \
[4:a]volume=-38dB,adelay=40000|40000[a4]; \
[5:a]aresample=48000,adelay=1500|1500[a5]; \
[6:a]aresample=48000,adelay=8000|8000[a6]; \
[7:a]aresample=48000,atempo=1.1,adelay=14400|14400[a7]; \
[8:a]aresample=48000,adelay=18000|18000[a8]; \
[9:a]aresample=48000,adelay=23000|23000[a9]; \
[10:a]aresample=48000,atempo=1.15,adelay=26000|26000[a10]; \
[11:a]aresample=48000,adelay=32000|32000[a11]; \
[12:a]aresample=48000,atempo=1.2,adelay=35000|35000[a12]; \
[13:a]aresample=48000,adelay=37000|37000[a13]; \
[14:a]aresample=48000,adelay=42500|42500[a14]; \
[15:a]aresample=48000,adelay=45000|45000[a15]; \
[a0][a1][a2][a3][a4][a5][a6][a7][a8][a9][a10][a11][a12][a13][a14][a15]amix=inputs=16:normalize=0,apad,atrim=0:60[aout]" \
 -map "[aout]" -c:a pcm_s16le $B/audio_mix.wav

# --- final: burn captions, mux ---
ffmpeg -y -v error -i $B/video_raw.mp4 -i $B/audio_mix.wav \
 -vf "subtitles=$B/teaser.srt:force_style='FontName=Liberation Sans,FontSize=20,PrimaryColour=&HFFFFFF,OutlineColour=&H80000000,BorderStyle=1,Outline=1,Shadow=0,Alignment=2,MarginV=36'" \
 -map 0:v -map 1:a -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -t 60 \
 you-can-see-anything-teaser.mp4
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 you-can-see-anything-teaser.mp4
