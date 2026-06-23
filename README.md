# ChromaVault - Green Screen Meme Library

A premium, interactive personal library for green screen overlays and meme assets. Designed for video editors, content creators, and developers to quickly preview green screen video templates, copy their paths, download assets, and obtain instant chroma-key processing commands.

## 🚀 Key Features

*   **Premium Glassmorphic Dark UI:** Sleek, modern dashboard aesthetic with glowing green accents and micro-animations.
*   **Tactile Hover Autoplay:** Hovering over any meme card triggers autoplay. When the cursor leaves, the video immediately pauses and resets to the beginning (`currentTime = 0`).
*   **Local Repository mode:** Designed to read directly from your local `memes/` folder to serve as a fast local asset assistant.
*   **Interactive Details Modal:** Clicking on any card opens an inspection window displaying metadata, resolution, duration, download links, and a pre-configured **FFmpeg colorkey overlay command**.
*   **Dynamic Search & Filtering:** Filter items by name, category, or hashtag search instantly. Sorting options (A-Z, duration) are built-in.
*   **Adjustable Grid Density:** Toggle grid layouts (3 columns vs 4 columns on desktop) with a simple header button.
*   **Clipboard Copy Helpers:** Copy file paths or command lines with single-click functionality and visual toast feedback.

---

## 🛠️ Tech Stack

*   **HTML5**
*   **Tailwind CSS** (via custom-configured CDN)
*   **Vanilla JavaScript** (ES6+)
*   **Lucide Icons** (Vector SVG via CDN)
*   **Google Fonts** (Outfit & Plus Jakarta Sans)

---

## 📂 Project Structure

To organize your local repository, set up your folder structure as follows:

```bash
green-screen-collection/
├── index.html
├── README.md
└── memes/               # Place your local MP4 files here
    ├── Anime Girl...mp4
    ├── BANGBOO...mp4
    ├── Chika Fujiwara...mp4
    └── ...
```

---

## 💻 Local Setup & Development

Because browser security policies (CORS) restrict loading local files directly via `file://` protocols, you should run a simple local HTTP server to preview your local videos.

### 1. Run a Simple Local Server

Open your terminal in the project directory and run one of the following commands:

**Using Python (Pre-installed on most systems):**
```bash
# Python 3
python -m http.server 8000
```

**Using Node.js (If installed):**
```bash
# Install live-server globally and run
npx live-server
```

Now, navigate to `http://localhost:8000` (or the port specified) in your browser.

Open `index.html` and look for the `memeFiles` array in the `<script>` tag. Simply add your exact video filenames there:

```javascript
const memeFiles = [
    "Your_Meme_Filename_720p.mp4",
    "Another_Meme_720p.mp4",
    // Add more filenames here...
];
```

The application's dynamic mapper will automatically clean up the file name to display a human-readable title, guess its category (e.g. Reaction, Gaming, Anime, Dance, Effects, Utility), tag it, and fetch the video duration once it loads in the browser.

---

## 🌐 Deploy to GitHub Pages

Since the project is completely static, it can be deployed on GitHub Pages in less than a minute:

1.  Create a new repository on GitHub (e.g., `green-screen-collection`).
2.  Commit your files and push them to the repository:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/green-screen-collection.git
    git push -u origin main
    ```
3.  Go to the repository **Settings** -> **Pages**.
4.  Under **Build and deployment**, select **Deploy from a branch** and set the branch to `main` (and folder `/ (root)`).
5.  Click **Save**. Your site will be live at `https://YOUR_USERNAME.github.io/green-screen-collection/` within a minute!

---

## 🎬 Video Editing: FFmpeg Chromakey Command Example

For quick green screen removal, click a card, open the detail modal, and copy the customized FFmpeg command. Below is the standard syntax:

```bash
# Key out pure green color (0x00FF00) and overlay it onto another input video
ffmpeg -i background.mp4 -i memes/your_meme.mp4 -filter_complex "[1:v]colorkey=0x00FF00:0.1:0.1[ck];[0:v][ck]overlay=x=0:y=0" -c:v libx264 output.mp4
```

*   `colorkey=0x00FF00`: Targets the primary green color.
*   `0.1:0.1`: Adjusts color similarity and blend/feather thresholds.
