#!/bin/bash
set -e
cd ~/workspace/you-can-see-anything-teaser
B=build/v7; mkdir -p $B
ENC="-c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -r 24 -an"

# --- video: reuse v5 segments except seg01 (clean v2 take, no 2s glitch) ---
cp build/v6/seg02.mp4 build/v6/seg03.mp4 build/v6/seg05a.mp4 build/v6/seg05b.mp4 build/v6/seg05c.mp4 build/v6/seg06.mp4 build/v6/seg07.mp4 build/v6/seg08.mp4 $B/
cp build/v6/teaser.srt $B/teaser.srt
C1=$(ls clips/v2/*shot01-*.mp4)
ffmpeg -y -v error -ss 0.35 -i "$C1" -vf "scale=1920:2880,crop=1920:1080:0:420,tpad=start_mode=clone:start_duration=0.35,trim=0:6,setpts=PTS-STARTPTS" $ENC $B/seg01.mp4
C4=$(ls clips/v4/*shot04-*.mp4)
ffmpeg -y -v error -ss 0.30 -i "$C4" -vf "scale=1920:2880,crop=1920:1080:0:700,tpad=start_mode=clone:start_duration=0.30,trim=0:8,setpts=PTS-STARTPTS" $ENC $B/seg04.mp4
printf "file 'seg01.mp4'\nfile 'seg02.mp4'\nfile 'seg03.mp4'\nfile 'seg04.mp4'\nfile 'seg05a.mp4'\nfile 'seg05b.mp4'\nfile 'seg05c.mp4'\nfile 'seg06.mp4'\nfile 'seg07.mp4'\nfile 'seg08.mp4'\n" > $B/concat.txt
ffmpeg -y -v error -f concat -safe 0 -i $B/concat.txt -c copy $B/video_raw.mp4

# --- audio: mid-register piano motif (survives phone speakers) + dialogue ---
ffmpeg -y -v error \
 -f lavfi -i "anoisesrc=color=white:seed=2718:d=55" \
 -f lavfi -i "sine=frequency=60:d=55" \
 -f lavfi -i "sine=frequency=43.65:d=22" \
 -f lavfi -i "aevalsrc=exprs='(sin(2*PI*220*t)+0.5*sin(2*PI*440*t)+0.3*sin(2*PI*660*t)+0.18*sin(2*PI*880*t)+0.1*sin(2*PI*1100*t))/2.08*if(lt(t\,0.008)\,t/0.008\,exp(-(t-0.008)/1.5))*if(gt(t\,3.85)\,(4-t)/0.15\,1)':d=4:s=48000" \
 -f lavfi -i "aevalsrc=exprs='(sin(2*PI*164.81*t)+0.5*sin(2*PI*329.62*t)+0.3*sin(2*PI*494.43*t)+0.18*sin(2*PI*659.24*t)+0.1*sin(2*PI*824.05*t))/2.08*if(lt(t\,0.008)\,t/0.008\,exp(-(t-0.008)/1.5))*if(gt(t\,3.85)\,(4-t)/0.15\,1)':d=4:s=48000" \
 -f lavfi -i "aevalsrc=exprs='(sin(2*PI*130.81*t)+0.5*sin(2*PI*261.62*t)+0.3*sin(2*PI*392.43*t)+0.18*sin(2*PI*523.24*t)+0.1*sin(2*PI*654.05*t))/2.08*if(lt(t\,0.008)\,t/0.008\,exp(-(t-0.008)/1.3))*if(gt(t\,3.35)\,(3.5-t)/0.15\,1)':d=3.5:s=48000" \
 -f lavfi -i "aevalsrc=exprs='(sin(2*PI*110*t)+0.5*sin(2*PI*220*t)+0.3*sin(2*PI*330*t)+0.18*sin(2*PI*440*t)+0.1*sin(2*PI*550*t))/2.08*if(lt(t\,0.008)\,t/0.008\,exp(-(t-0.008)/1.4))*if(gt(t\,2.85)\,(3-t)/0.15\,1)':d=3:s=48000" \
 -f lavfi -i "aevalsrc=exprs='(sin(2*PI*110*t)+0.6*sin(2*PI*164.81*t)+0.5*sin(2*PI*220*t)+0.3*sin(2*PI*261.63*t))/2.4':d=13:s=48000" \
 -f lavfi -i "aevalsrc=exprs='(sin(2*PI*110*t)+sin(2*PI*220*t)+0.5*sin(2*PI*330*t)+0.5*sin(2*PI*440*t)+0.3*sin(2*PI*550*t))/2.8*if(lt(t\,0.008)\,t/0.008\,exp(-(t-0.008)/1.8))*if(gt(t\,3.85)\,(4-t)/0.15\,1)':d=4:s=48000" \
 -i dialogue/v2/f01.mp3 -i dialogue/v2/d01.mp3 -i dialogue/v2/f02.mp3 -i dialogue/v2/d02.mp3 \
 -i dialogue/v2/f03.mp3 -i dialogue/v2/r01.mp3 -i dialogue/v2/d03.mp3 -i dialogue/v2/d04.mp3 \
 -i dialogue/v2/d05.mp3 -i dialogue/v2/f04.mp3 -i dialogue/v2/d06.mp3 \
 -filter_complex "\
[0:a]highpass=f=100,lowpass=f=3000,volume=-48dB,aresample=48000[a0]; \
[1:a]volume=-66dB,aresample=48000[a1]; \
[2:a]volume='if(lt(t,6),(1-cos(PI*t/6))/2,if(gt(t,16),(1-cos(PI*(22-t)/6))/2,1))':eval=frame,volume=-42dB,adelay=18000|18000[a2]; \
[3:a]volume=-15dB,adelay=11000|11000,aresample=48000[a3]; \
[4:a]volume=-15dB,adelay=27200|27200,aresample=48000[a4]; \
[5:a]volume=-16dB,adelay=34600|34600,aresample=48000[a5]; \
[6:a]volume=-16dB,adelay=40000|40000,aresample=48000[a6]; \
[7:a]lowpass=f=1200,volume='if(lt(t,3),t/3,if(gt(t,12.7),(13-t)/0.3,1))':eval=frame,volume=-24dB,adelay=42000|42000,aresample=48000[a7]; \
[8:a]volume=-13dB,adelay=56000|56000,aresample=48000[a8]; \
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
 you-can-see-anything-teaser-v7.mp4
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 you-can-see-anything-teaser-v7.mp4
