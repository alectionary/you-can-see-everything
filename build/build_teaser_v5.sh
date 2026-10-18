#!/bin/bash
set -e
cd ~/workspace/you-can-see-anything-teaser
B=build/v5; mkdir -p $B
C1=$(ls clips/v3/*shot01-*.mp4); C2=$(ls clips/v3/*shot02-*.mp4); C3=$(ls clips/v3/*shot03-*.mp4)
C4=$(ls clips/v4/*shot04-*.mp4)
CR=$(ls clips/v4/*fielder-reaction-*.mp4); C5=$(ls clips/v3/*shot05-*.mp4); C6=$(ls clips/v3/*shot06-*.mp4)
ENC="-c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -r 24 -an"

# --- video segments (1920x1080, 24fps, no audio) ---
ffmpeg -y -v error -i "$C1" -vf "scale=1920:2880,crop=1920:1080:0:700,trim=0:6,setpts=PTS-STARTPTS" $ENC $B/seg01.mp4
ffmpeg -y -v error -i "$C2" -vf "scale=1920:1920,crop=1920:1080:0:420,trim=0:8,setpts=PTS-STARTPTS" $ENC $B/seg02.mp4
ffmpeg -y -v error -i "$C3" -vf "scale=1920:1920,crop=1920:1080:0:420,trim=0:8,setpts=PTS-STARTPTS" $ENC $B/seg03.mp4
ffmpeg -y -v error -i "$C4" -vf "scale=1920:2880,crop=1920:1080:0:700,trim=0:8,setpts=PTS-STARTPTS" $ENC $B/seg04.mp4
ffmpeg -y -v error -i "$C5" -vf "scale=1920:1920,crop=1920:1080:0:420,trim=0:4,setpts=PTS-STARTPTS" $ENC $B/seg05a.mp4
ffmpeg -y -v error -i "$CR" -vf "scale=1920:2880,crop=1920:1080:0:700,trim=0:6,setpts=PTS-STARTPTS" $ENC $B/seg05b.mp4
ffmpeg -y -v error -ss 8 -i "$C5" -vf "scale=1920:1920,crop=1920:1080:0:420,trim=0:2,setpts=PTS-STARTPTS" $ENC $B/seg05c.mp4
ffmpeg -y -v error -i "$C6" -vf "scale=1920:1920,crop=1920:1080:0:420,tpad=stop_mode=clone:stop_duration=3,trim=0:13,setpts=PTS-STARTPTS" $ENC $B/seg06.mp4
ffmpeg -y -v error -f lavfi -i color=black:s=1920x1080:r=24:d=1 $ENC $B/seg07.mp4
ffmpeg -y -v error -f lavfi -i color=black:s=1920x1080:r=24:d=4 -vf "drawtext=fontfile=/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf:text='YOU CAN SEE ANYTHING':fontsize=64:fontcolor=0xE6E4DF:x=(w-text_w)/2:y=(h-text_h)/2" $ENC $B/seg08.mp4
printf "file 'seg01.mp4'\nfile 'seg02.mp4'\nfile 'seg03.mp4'\nfile 'seg04.mp4'\nfile 'seg05a.mp4'\nfile 'seg05b.mp4'\nfile 'seg05c.mp4'\nfile 'seg06.mp4'\nfile 'seg07.mp4'\nfile 'seg08.mp4'\n" > $B/concat.txt
ffmpeg -y -v error -f concat -safe 0 -i $B/concat.txt -c copy $B/video_raw.mp4

# --- captions ---
cat > $B/teaser.srt <<'SRT'
1
00:00:01,500 --> 00:00:03,265
And the county approved the parking?

2
00:00:08,000 --> 00:00:09,161
The use was permitted.

3
00:00:14,500 --> 00:00:16,125
The building was a food bank.

4
00:00:18,000 --> 00:00:19,858
I can't account for their interpretation.

5
00:00:23,000 --> 00:00:24,950
It says here the neighbors objected.

6
00:00:26,000 --> 00:00:26,975
Never. Not once.

7
00:00:32,000 --> 00:00:34,136
I'm engaging with you as a human being.

8
00:00:35,000 --> 00:00:36,161
Why would I deceive you?

9
00:00:37,500 --> 00:00:39,265
There's no reason for me to do that.

10
00:00:42,500 --> 00:00:44,125
Are you being real right now?

11
00:00:45,000 --> 00:00:46,161
I'm always being real.
SRT

# --- audio: dramatic minimal score + dialogue ---
ffmpeg -y -v error \
 -f lavfi -i "anoisesrc=color=white:seed=2718:d=55" \
 -f lavfi -i "sine=frequency=60:d=55" \
 -f lavfi -i "sine=frequency=43.65:d=22" \
 -f lavfi -i "aevalsrc=exprs='(sin(2*PI*87.31*t)+0.35*sin(2*PI*174.62*t)+0.12*sin(2*PI*261.93*t)+0.04*sin(2*PI*349.24*t))/1.51*if(lt(t\,0.008)\,t/0.008\,exp(-(t-0.008)/1.10))*if(gt(t\,3.85)\,(4.00-t)/0.15\,1)':d=4:s=48000" \
 -f lavfi -i "aevalsrc=exprs='(sin(2*PI*77.78*t)+0.35*sin(2*PI*155.56*t)+0.12*sin(2*PI*233.34*t)+0.04*sin(2*PI*311.12*t))/1.51*if(lt(t\,0.008)\,t/0.008\,exp(-(t-0.008)/1.20))*if(gt(t\,3.85)\,(4.00-t)/0.15\,1)':d=4:s=48000" \
 -f lavfi -i "aevalsrc=exprs='(sin(2*PI*58.27*t)+0.35*sin(2*PI*116.54*t)+0.12*sin(2*PI*174.81*t)+0.04*sin(2*PI*233.08*t))/1.51*if(lt(t\,0.008)\,t/0.008\,exp(-(t-0.008)/1.00))*if(gt(t\,3.35)\,(3.50-t)/0.15\,1)':d=3.5:s=48000" \
 -f lavfi -i "aevalsrc=exprs='(sin(2*PI*130.81*t)+0.35*sin(2*PI*261.62*t)+0.12*sin(2*PI*392.43*t)+0.04*sin(2*PI*523.24*t))/1.51*if(lt(t\,0.008)\,t/0.008\,exp(-(t-0.008)/0.90))*if(gt(t\,2.85)\,(3.00-t)/0.15\,1)':d=3:s=48000" \
 -f lavfi -i "aevalsrc=exprs='(sin(2*PI*55*t)+0.6*sin(2*PI*82.41*t)+0.5*sin(2*PI*110*t)+0.25*sin(2*PI*164.81*t))/2.35':d=13:s=48000" \
 -f lavfi -i "aevalsrc=exprs='(sin(2*PI*43.65*t)+0.35*sin(2*PI*87.30*t)+0.12*sin(2*PI*130.95*t)+0.04*sin(2*PI*174.60*t))/1.51*if(lt(t\,0.008)\,t/0.008\,exp(-(t-0.008)/1.60))*if(gt(t\,3.85)\,(4.00-t)/0.15\,1)':d=4:s=48000" \
 -i dialogue/v2/f01.mp3 -i dialogue/v2/d01.mp3 -i dialogue/v2/f02.mp3 -i dialogue/v2/d02.mp3 \
 -i dialogue/v2/f03.mp3 -i dialogue/v2/r01.mp3 -i dialogue/v2/d03.mp3 -i dialogue/v2/d04.mp3 \
 -i dialogue/v2/d05.mp3 -i dialogue/v2/f04.mp3 -i dialogue/v2/d06.mp3 \
 -filter_complex "\
[0:a]highpass=f=100,lowpass=f=3000,volume=-48dB,aresample=48000[a0]; \
[1:a]volume=-66dB,aresample=48000[a1]; \
[2:a]volume='if(lt(t,6),(1-cos(PI*t/6))/2,if(gt(t,16),(1-cos(PI*(22-t)/6))/2,1))':eval=frame,volume=-42dB,adelay=18000|18000[a2]; \
[3:a]volume=-20dB,adelay=11000|11000,aresample=48000[a3]; \
[4:a]volume=-20dB,adelay=27200|27200,aresample=48000[a4]; \
[5:a]volume=-21dB,adelay=34600|34600,aresample=48000[a5]; \
[6:a]volume=-20dB,adelay=40000|40000,aresample=48000[a6]; \
[7:a]lowpass=f=500,volume='if(lt(t,3),t/3,if(gt(t,12.7),(13-t)/0.3,1))':eval=frame,volume=-27dB,adelay=42000|42000,aresample=48000[a7]; \
[8:a]volume=-15dB,adelay=56000|56000,aresample=48000[a8]; \
[9:a]aresample=48000,adelay=1500|1500[a9]; \
[10:a]aresample=48000,adelay=8000|8000[a10]; \
[11:a]aresample=48000,adelay=14500|14500[a11]; \
[12:a]aresample=48000,adelay=18000|18000[a12]; \
[13:a]aresample=48000,adelay=23000|23000[a13]; \
[14:a]aresample=48000,adelay=26000|26000[a14]; \
[15:a]aresample=48000,adelay=32000|32000[a15]; \
[16:a]aresample=48000,adelay=35000|35000[a16]; \
[17:a]aresample=48000,adelay=37500|37500[a17]; \
[18:a]aresample=48000,adelay=42500|42500[a18]; \
[19:a]aresample=48000,adelay=45000|45000[a19]; \
[a0][a1][a2][a3][a4][a5][a6][a7][a8][a9][a10][a11][a12][a13][a14][a15][a16][a17][a18][a19]amix=inputs=20:normalize=0,apad,atrim=0:60[aout]" \
 -map "[aout]" -c:a pcm_s16le $B/audio_mix.wav

# --- final: burn captions, mux ---
ffmpeg -y -v error -i $B/video_raw.mp4 -i $B/audio_mix.wav \
 -vf "subtitles=$B/teaser.srt:force_style='FontName=Liberation Sans,FontSize=20,PrimaryColour=&HFFFFFF,OutlineColour=&H80000000,BorderStyle=1,Outline=1,Shadow=0,Alignment=2,MarginV=36'" \
 -map 0:v -map 1:a -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -t 60 \
 you-can-see-anything-teaser-v5.mp4
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 you-can-see-anything-teaser-v5.mp4
