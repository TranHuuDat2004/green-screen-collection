import os
import re
import subprocess

# 1. DÁN TIMESTAMPS TỪ YOUTUBE VÀO ĐÂY
timestamps_text = """
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

# 2. ĐẶT TÊN FILE NHẠC ĐÃ TẢI VỀ Ở ĐÂY
INPUT_FILE = "input.mp4"  # Thay đổi thành .mp4, .m4a nếu file của bạn định dạng khác
OUTPUT_DIR = "sound_effects"

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
    if not os.path.exists(INPUT_FILE):
        print(f"Lỗi: Không tìm thấy file nguồn '{INPUT_FILE}' trong thư mục hiện tại!")
        print("Vui lòng tải file về và đặt tên trùng với cấu hình.")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Parse timestamps
    chapters = []
    lines = [line.strip() for line in timestamps_text.strip().split('\n') if line.strip()]
    
    for line in lines:
        match = re.match(r'^(\d+:\d+(?::\d+)?)\s*-\s*(.*)$', line)
        if match:
            time_str, name = match.groups()
            chapters.append({
                'seconds': time_to_seconds(time_str),
                'name': clean_filename(name)
            })
            
    if not chapters:
        print("Không tìm thấy timestamps hợp lệ!")
        return

    # Lấy định dạng đuôi file nguồn để cắt ra đúng định dạng
    file_ext = os.path.splitext(INPUT_FILE)[1]

    print("Bắt đầu phân tách âm thanh...")

    # Gọi FFmpeg cắt nhạc
    for i, chapter in enumerate(chapters):
        start_time = chapter['seconds']
        name = chapter['name']
        output_file = os.path.join(OUTPUT_DIR, f"{i+1:02d} - {name}{file_ext}")
        
        if i + 1 < len(chapters):
            duration = chapters[i+1]['seconds'] - start_time
            duration_cmd = ["-t", str(duration)]
        else:
            duration_cmd = [] # Cắt tới hết video
            
        print(f"Đang cắt: {name} ({start_time}s)")
        
        # Lệnh chạy FFmpeg thuần
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_time),
            "-i", INPUT_FILE
        ] + duration_cmd + [
            "-acodec", "copy",
            "-vcodec", "copy", # Đảm bảo hoạt động nếu file nguồn là video .mp4
            output_file
        ]
        
        # Chạy ẩn tiến trình ffmpeg
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"\n Hoàn tất! Tất cả các file đã được lưu trong thư mục '{OUTPUT_DIR}/'.")

if __name__ == "__main__":
    main()
