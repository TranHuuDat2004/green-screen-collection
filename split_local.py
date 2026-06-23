import os
import re
import subprocess

OUTPUT_DIR = "sound_effects"

BATCHES = [
    {
        "file": "input.mp4",
        "start_index": 1,
        "timestamps": """
0:00 - Chinese Gong
0:06 - Taco Bell
0:08 - Awkward Moment
0:10 - Awkward Pause (1-2)
0:15 - Camera Flash
0:16 - Collect Gold
0:18 - Bone Crack
0:19 - Topac Engle
0:25 - Skibidi Boom
0:29 - Blinking
0:30 - Magic Spells
0:32 - RUDE - Eternal Youth
0:38 - Vine Boom (Slowed)
0:42 - Lie Detector
0:43 - Man falling down the Stairs
0:45 - Please Stand By
0:50 - Ultra Instinct
0:55 - The Good Ending
1:02 - Cash Register (1-5)
1:14 - Cinematic Boom
1:18 - Breast Twitch
1:20 - Thank You!
1:21 - Discord Call (Join)
1:22 - Discord Call (Leave)
1:23 - Discord Notification
1:24 - Discord Ringtone
1:30 - Undertakers Bell
1:33 - iPhone (Send - Recieve)
1:35 - Build Up
1:38 - 999 Credit Score Siren
1:42 - Daft Punk - Robot Rock
1:46 - Hell's Kitchen Suspense
1:49 - DA - Bells (1-3)
1:53 - TiK-TiK
1:54 - Bua Wa Wa Wa Wa
1:57 - Munch Bite
1:58 - French Meme
2:02 - God Damn!
2:03 - Travis Scott Meme
2:07 - Goku Power
2:11 - Anime Punch
2:13 - Lego Breaking
2:15 - Sakhteman Pezeshkan
2:19 - Gay Echo Voice
2:24 - Metal Pipe Falling
2:27 - TikTok Mentality
2:28 - Twitch Alert
2:30 - TF2 Om Nom Nom
2:33 - Goofy Ahh Car Honk
2:36 - Police Radio Beep
2:37 - Glass breaking
2:38 - Flashbang (Loud)
"""
    },
    {
        "file": "input2.mp4",
        "start_index": 53,
        "timestamps": """
00:00 - Collect Item
00:03 - Record Scratch
00:04 - Bass Drop + Vine Boom
00:09 - English Or Spanish
00:16 - Dragon Ball Z Teleportation
00:18 - I Have No Enemies
00:24 - Tape Rewind
00:25 - Devious Song
00:32 - Bad To The Bone
00:38 - Long Brain Fart
00:43 - PS2 Start Up Screen
00:51 - Don Pollo Goofy Ahh
00:58 - Sisyphus Meme
01:05 - Magical Healing
01:07 - Slow Motion
01:14 - Skeleton Rahhh
01:16 - Chill Guy Meme
01:24 - Negus
01:26 - I'm Bouta Cuh Harmony
01:34 - You Stupid Men
01:36 - What Bottom Text Meme
01:41 - Sad Hamester Violin
01:49 - Primavera - Antonio Vivaldi
01:54 - Cat Laughing At You
02:02 - Tarantella Medley (Italian)
02:06 - Gulp-Gulp-Gulp
02:10 - Body Thud
02:12 - I Be Poppin Bottles (Boosted)
02:18 - Flashback
02:23 - Thousand Yard Stare
02:31 - Plankton Meme
02:36 - Kanye Wolves Meme
02:43 - Sonic Ring
02:45 - Boy Sing With Helium
02:53 - Laugh Toy Wolrd Animation
02:58 - The Purge Siren
03:01 - Building Explotion
03:03 - Mistfulplays Meme
03:09 - South Park Guitar
03:13 - Cinematic Boom
03:16 - Super Idol
03:22 - Google Ngram Viewer
03:30 - Oh My God Bro WTF Man
03:38 - Birdsall - Guiding Path
03:45 - Berserk Skeleton
03:53 - Napoleon Meme
03:58 - Bamboo Hit
04:00 - Gangnam Style
04:03 - Cartoon Transition
04:05 - Salamaleco Maleco Sala
04:10 - Confused (Reverb)
04:14 - Spider Man Black Suit
04:20 - Fnaf 2 Hallway
04:25 - Windows Start Up
04:29 - Go Crazy!
04:32 - The Lego Batman Meme
04:39 - Anime Discovery
04:42 - Party Horn
04:44 - Spider Man Pizza Theme
04:51 - Slime Sword Clash
"""
    },
    {
        "file": "input3.mp4",
        "start_index": 113,
        "timestamps": """
00:00 - God Damn!
00:02 - Spawn
00:05 - Metal Pipe Falling (Loud)
00:08 - Undertakers Bell
00:13 - Travis Scott Meme
00:17 - Mentality
00:19 - PS2 Startup Screen
00:26 - French Meme
00:30 - Bass Drop
00:35 - Windows 95 Startup
00:41 - Windows XP Start
00:46 - Windows XP Shutdown
00:49 - English OR Spanish
00:56 - Flashbang
01:00 - 999 Credit Score Siren
01:05 - Exaggerated Among Us
01:11 - Long Brain Fart
01:17 - Gay Echo Voice
01:21 - Bye Bye Mewing
01:22 - Crowd Laugh
01:26 - Get Out!
01:28 - Glass Breaking
01:31 - RDR2 : Low Honor
01:35 - Grandma House
01:40 - Collect Gold
01:43 - Slow Motion
01:49 - Spongebob Walking
01:53 - I Be Poppin Bottles (Boosted)
02:00 - Depressed Penguin
02:05 - Super Idol
02:11 - Fortnite Shield Potion
02:19 - Don Pollo Ahh Sound
02:26 - Dark Piano Dexter
02:32 - Optimus Prime
02:40 - Hells Kitchen Suspense
02:44 - Bone Crack
02:46 - Magic Spells
02:49 - Laugh Toy World Animation
02:53 - You Are My Sunshine
03:00 - Taco Bell
03:03 - Fahh
"""
    }
]

def time_to_seconds(t_str):
    parts = list(map(int, t_str.split(':')))
    if len(parts) == 2: # MM:SS
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3: # HH:MM:SS
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return 0

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def main():
    # Clear output directory first
    if os.path.exists(OUTPUT_DIR):
        print("Clearing output directory...")
        for f in os.listdir(OUTPUT_DIR):
            try:
                os.remove(os.path.join(OUTPUT_DIR, f))
            except Exception as e:
                print(f"Error removing {f}: {e}")
    else:
        os.makedirs(OUTPUT_DIR)

    for batch in BATCHES:
        input_file = batch["file"]
        start_idx = batch["start_index"]
        
        if not os.path.exists(input_file):
            print(f"Lỗi: Không tìm thấy file nguồn '{input_file}'!")
            continue

        print(f"\nBắt đầu phân tách file: {input_file} (Bắt đầu từ index: {start_idx})")

        # Parse timestamps
        chapters = []
        lines = [line.strip() for line in batch["timestamps"].strip().split('\n') if line.strip()]
        
        for line in lines:
            match = re.match(r'^(\d+:\d+(?::\d+)?)\s*-\s*(.*)$', line)
            if match:
                time_str, name = match.groups()
                chapters.append({
                    'seconds': time_to_seconds(time_str),
                    'name': clean_filename(name)
                })

        file_ext = os.path.splitext(input_file)[1]

        # Splitting using ffmpeg
        for i, chapter in enumerate(chapters):
            curr_idx = start_idx + i
            start_time = chapter['seconds']
            name = chapter['name']
            
            output_file = os.path.join(OUTPUT_DIR, f"{curr_idx:03d} - {name}{file_ext}")
            
            if i + 1 < len(chapters):
                duration = chapters[i+1]['seconds'] - start_time
                duration_cmd = ["-t", str(duration)]
            else:
                duration_cmd = [] # Cut to end of video
                
            print(f"  [{curr_idx:03d}] Đang cắt: {name} ({start_time}s)")
            
            cmd = [
                "ffmpeg", "-y",
                "-ss", str(start_time),
                "-i", input_file
            ] + duration_cmd + [
                "-acodec", "copy",
                "-vcodec", "copy",
                output_file
            ]
            
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"\n Hoàn tất! Tất cả các file đã được lưu trong thư mục '{OUTPUT_DIR}/'.")

if __name__ == "__main__":
    main()
