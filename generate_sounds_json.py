import os
import re
import json

SOUND_DIR = "sound_effects"
JSON_FILE = "sound_effects.json"

def clean_filename(name):
    return re.sub(r'^\d+\s*-\s*', '', name) # remove "01 - " prefix

def get_tags(name):
    # Split by spaces and non-alpha characters to create search tags
    words = re.findall(r'\b\w+\b', name.lower())
    # Filter out common short words and duplicate tags
    ignored = {'and', 'the', 'for', 'with', 'from', 'sound', 'effect', 'meme'}
    tags = [w for w in words if len(w) > 2 and w not in ignored]
    return list(set(tags)) if tags else ["sfx"]

def main():
    if not os.path.exists(SOUND_DIR):
        print(f"Directory {SOUND_DIR} does not exist.")
        return

    files = sorted([f for f in os.listdir(SOUND_DIR) if f.endswith('.mp4') or f.endswith('.mp3')])
    
    sound_database = []
    
    # We can reconstruct durations using the split_local.py timestamps list
    timestamps = [
        (0, "Chinese Gong"),
        (6, "Taco Bell"),
        (8, "Awkward Moment"),
        (10, "Awkward Pause (1-2)"),
        (15, "Camera Flash"),
        (16, "Collect Gold"),
        (18, "Bone Crack"),
        (19, "Topac Engle"),
        (25, "Skibidi Boom"),
        (29, "Blinking"),
        (30, "Magic Spells"),
        (32, "RUDE - Eternal Youth"),
        (38, "Vine Boom (Slowed)"),
        (42, "Lie Detector"),
        (43, "Man falling down the Stairs"),
        (45, "Please Stand By"),
        (50, "Ultra Instinct"),
        (55, "The Good Ending"),
        (62, "Cash Register (1-5)"),
        (74, "Cinematic Boom"),
        (78, "Breast Twitch"),
        (80, "Thank You!"),
        (81, "Discord Call (Join)"),
        (82, "Discord Call (Leave)"),
        (83, "Discord Notification"),
        (84, "Discord Ringtone"),
        (90, "Undertakers Bell"),
        (93, "iPhone (Send - Recieve)"),
        (95, "Build Up"),
        (98, "999 Credit Score Siren"),
        (102, "Daft Punk - Robot Rock"),
        (106, "Hell's Kitchen Suspense"),
        (109, "DA - Bells (1-3)"),
        (113, "TiK-TiK"),
        (114, "Bua Wa Wa Wa Wa"),
        (117, "Munch Bite"),
        (118, "French Meme"),
        (122, "God Damn!"),
        (123, "Travis Scott Meme"),
        (127, "Goku Power"),
        (131, "Anime Punch"),
        (133, "Lego Breaking"),
        (135, "Sakhteman Pezeshkan"),
        (139, "Gay Echo Voice"),
        (144, "Metal Pipe Falling"),
        (147, "TikTok Mentality"),
        (148, "Twitch Alert"),
        (150, "TF2 Om Nom Nom"),
        (153, "Goofy Ahh Car Honk"),
        (156, "Police Radio Beep"),
        (157, "Glass breaking"),
        (158, "Flashbang (Loud)"),
        (165, "End") # Estimated end for final duration
    ]

    for i, filename in enumerate(files):
        # Extract index and clean name
        match = re.match(r'^(\d+)\s*-\s*(.*)\.(mp4|mp3)$', filename)
        if not match:
            continue
            
        idx_str, raw_name, ext = match.groups()
        idx = int(idx_str) - 1
        
        name = raw_name
        
        # Calculate duration
        duration_sec = 5 # Default fallback
        if idx < len(timestamps) - 1:
            duration_sec = timestamps[idx+1][0] - timestamps[idx][0]
            
        min_part = duration_sec // 60
        sec_part = duration_sec % 60
        duration_str = f"{min_part}:{sec_part:02d}"
        
        sound_id = f"sfx-{idx_str}"
        path = f"{SOUND_DIR}/{filename}"
        
        sound_database.append({
            "id": sound_id,
            "name": name,
            "path": path,
            "category": "Sound Effect",
            "duration": duration_str,
            "description": f"Premium sound effect overlay of '{name}' for video editors.",
            "resolution": "Audio/Video Clip",
            "tags": get_tags(name)
        })
        
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(sound_database, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully generated {JSON_FILE} with {len(sound_database)} records.")

if __name__ == "__main__":
    main()
