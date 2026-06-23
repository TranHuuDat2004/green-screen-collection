// APP STATE
let memeDatabase = [];
let searchQuery = '';
let selectedCategory = 'All';
let sortOption = 'name-asc';
let gridCols = 4; // default column count

// DOM ELEMENTS
const memesGrid = document.getElementById('memes-grid');
const emptyState = document.getElementById('empty-state');
const categoryContainer = document.getElementById('category-container');
const resultsCountLabel = document.getElementById('results-count');
const searchInput = document.getElementById('search-input');
const clearSearchBtn = document.getElementById('clear-search');

// MODAL DOM
const detailModal = document.getElementById('detail-modal');
const modalVideo = document.getElementById('modal-video');
const modalSpinner = document.getElementById('modal-spinner');
const modalTitle = document.getElementById('modal-title');
const modalDesc = document.getElementById('modal-desc');
const modalRes = document.getElementById('modal-res');
const modalDownloadBtn = document.getElementById('modal-download-btn');

// INITIALIZE APP
document.addEventListener('DOMContentLoaded', () => {
    fetch('sound_effects.json')
        .then(res => res.json())
        .then(data => {
            memeDatabase = data;
            renderCategories();
            renderGrid();
            lucide.createIcons();
        })
        .catch(err => {
            console.error("Error loading sound_effects.json:", err);
            showToast("Failed to load sound effects database. Please ensure you are running on a local web server (e.g. python -m http.server 8000).", "error");
        });
    
    // ESC key to close modal
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });
});

// EXTRACT CATEGORIES
function getCategories() {
    const categories = new Set();
    memeDatabase.forEach(item => categories.add(item.category));
    return ['All', ...Array.from(categories)];
}

// RENDER CATEGORY PILLS
function renderCategories() {
    const categories = getCategories();
    categoryContainer.innerHTML = '';
    
    categories.forEach(category => {
        const isActive = category === selectedCategory;
        const btn = document.createElement('button');
        btn.className = `px-4 py-2 rounded-xl text-xs font-semibold tracking-wide transition-all duration-200 ${
            isActive 
                ? 'bg-brand-500 text-darkbg shadow-lg shadow-brand-500/10' 
                : 'bg-slate-900 border border-darkborder hover:border-brand-500/30 text-slate-400 hover:text-slate-200'
        }`;
        btn.textContent = category;
        btn.onclick = () => filterCategory(category);
        categoryContainer.appendChild(btn);
    });
}

// GRID COLUMNS STATE
function setGridColumns(cols) {
    gridCols = cols;
    const grid3 = document.getElementById('grid-3-btn');
    const grid4 = document.getElementById('grid-4-btn');
    
    memesGrid.className = `grid grid-cols-1 sm:grid-cols-2 transition-all duration-300 gap-6`;
    if (cols === 3) {
        memesGrid.classList.add('lg:grid-cols-3');
        grid3.className = "p-1.5 rounded-lg bg-slate-800 text-brand-400 transition-colors";
        grid4.className = "p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors";
    } else {
        memesGrid.classList.add('lg:grid-cols-4');
        grid4.className = "p-1.5 rounded-lg bg-slate-800 text-brand-400 transition-colors";
        grid3.className = "p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors";
    }
}

// FILTER LOGIC
function filterCategory(category) {
    selectedCategory = category;
    renderCategories();
    renderGrid();
}

// SEARCH LOGIC
function handleSearch(val) {
    searchQuery = val.trim().toLowerCase();
    if (searchQuery) {
        clearSearchBtn.classList.remove('hidden');
    } else {
        clearSearchBtn.classList.add('hidden');
    }
    renderGrid();
}

// CLEAR SEARCH LOGIC
function clearSearch() {
    searchInput.value = '';
    searchQuery = '';
    clearSearchBtn.classList.add('hidden');
    renderGrid();
}

// SORT LOGIC
function handleSort(option) {
    sortOption = option;
    renderGrid();
}

// RESET FILTERS LOGIC
function resetFilters() {
    searchInput.value = '';
    searchQuery = '';
    selectedCategory = 'All';
    sortOption = 'name-asc';
    clearSearchBtn.classList.add('hidden');
    renderCategories();
    renderGrid();
}

// RENDER MEME GRID
function renderGrid() {
    let filtered = memeDatabase.filter(item => {
        const matchesCategory = selectedCategory === 'All' || item.category === selectedCategory;
        const matchesSearch = item.name.toLowerCase().includes(searchQuery) ||
                              item.category.toLowerCase().includes(searchQuery) ||
                              item.tags.some(tag => tag.toLowerCase().includes(searchQuery));
        return matchesCategory && matchesSearch;
    });

    if (sortOption === 'name-asc') {
        filtered.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortOption === 'name-desc') {
        filtered.sort((a, b) => b.name.localeCompare(a.name));
    } else if (sortOption === 'duration-desc') {
        filtered.sort((a, b) => b.duration.localeCompare(a.duration));
    } else if (sortOption === 'duration-asc') {
        filtered.sort((a, b) => a.duration.localeCompare(b.duration));
    }

    resultsCountLabel.textContent = `${filtered.length} sound${filtered.length !== 1 ? 's' : ''}`;

    if (filtered.length === 0) {
        memesGrid.classList.add('hidden');
        emptyState.classList.remove('hidden');
        emptyState.classList.add('flex');
        return;
    } else {
        memesGrid.classList.remove('hidden');
        emptyState.classList.remove('flex');
        emptyState.classList.add('hidden');
    }

    memesGrid.innerHTML = '';

    filtered.forEach(item => {
        const card = document.createElement('div');
        card.className = "meme-card group bg-darkcard/40 border border-darkborder/75 rounded-2xl overflow-hidden hover:-translate-y-1 transition-all duration-300 flex flex-col justify-between";
        
        card.innerHTML = `
            <!-- Video Container -->
            <div class="relative w-full aspect-video bg-black overflow-hidden select-none cursor-pointer" onclick="openModal('${item.id}')">
                <!-- Glowing SFX Overlay -->
                <div class="absolute inset-0 bg-brand-500/10 pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10 border-b border-brand-500/25"></div>
                
                <!-- Audio Play Waveform / Icon Indicator -->
                <div class="play-indicator absolute inset-0 flex items-center justify-center bg-slate-950/50 z-20 transition-all duration-300 group-hover:opacity-0 group-hover:scale-90">
                    <div class="h-12 w-12 rounded-full bg-slate-900/90 border border-slate-800/80 text-brand-400 flex items-center justify-center shadow-lg group-hover:bg-brand-500 group-hover:text-darkbg group-hover:border-transparent transition-all">
                        <i data-lucide="volume-2" class="h-5 w-5"></i>
                    </div>
                </div>

                <!-- Active Preview Dot -->
                <div class="absolute top-3 left-3 z-20 bg-brand-500 text-darkbg font-display font-black text-[9px] px-2 py-0.5 rounded-full flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                    <span class="h-1.5 w-1.5 rounded-full bg-darkbg animate-pulse"></span>
                    PREVIEW
                </div>

                <!-- Card Audio Toggle (SFX plays with audio by default) -->
                <button onclick="toggleCardMute(event, '${item.id}')" id="mute-btn-${item.id}" class="absolute top-3 right-3 z-30 p-1.5 bg-brand-500/20 border border-brand-500/30 rounded-lg text-brand-400 transition-colors" title="Toggle audio">
                    <i data-lucide="volume-2" class="h-3.5 w-3.5"></i>
                </button>

                <!-- Spinner for loading state -->
                <div id="spinner-${item.id}" class="absolute inset-0 flex items-center justify-center bg-slate-950/50 hidden z-15">
                    <div class="animate-spin rounded-full h-8 w-8 border-2 border-brand-500 border-t-transparent"></div>
                </div>

                <!-- Video Element -->
                <video 
                    id="video-${item.id}" 
                    src="${item.path}"
                    class="w-full h-full object-cover relative z-0" 
                    playsinline
                    loop
                    preload="metadata"
                ></video>
            </div>

            <!-- Details Content -->
            <div class="p-4 flex flex-col flex-1 justify-between">
                <div>
                    <div class="flex items-center justify-between gap-2 mb-1.5">
                        <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">${item.category}</span>
                        <span class="duration-label text-[10px] text-slate-500 font-mono flex items-center gap-1" id="duration-label-${item.id}">
                            <i data-lucide="clock" class="h-2.5 w-2.5"></i> ${item.duration}
                        </span>
                    </div>
                    <h4 class="font-display font-bold text-slate-100 text-sm hover:text-brand-400 transition-colors cursor-pointer line-clamp-1" onclick="openModal('${item.id}')" title="${item.name}">
                        ${item.name}
                    </h4>
                    
                    <!-- Tags -->
                    <div class="flex flex-wrap gap-1 mt-3">
                        ${item.tags.slice(0, 3).map(tag => `
                            <span class="text-[9px] font-semibold bg-slate-900/60 border border-darkborder/50 text-slate-400 px-2 py-0.5 rounded-md hover:text-slate-200 cursor-pointer" onclick="clickTag('${tag}')">#${tag}</span>
                        `).join('')}
                    </div>
                </div>

                <!-- Card Action Footer -->
                <div class="flex gap-2 mt-4 pt-3 border-t border-darkborder/30">
                    <a href="${item.path}" download="${item.name}.mp4" class="flex-1 flex items-center justify-center gap-1.5 py-2 bg-brand-500 hover:bg-brand-600 text-darkbg rounded-lg text-xs font-bold transition-all shadow-md" title="Download audio file">
                        <i data-lucide="download" class="h-3.5 w-3.5"></i>
                        Download
                    </a>
                    <button onclick="openModal('${item.id}')" class="p-2 bg-brand-500/10 hover:bg-brand-500 text-brand-400 hover:text-darkbg rounded-lg transition-all" title="Inspect details">
                        <i data-lucide="expand" class="h-3.5 w-3.5"></i>
                    </button>
                </div>
            </div>
        `;

        memesGrid.appendChild(card);

        const video = card.querySelector(`video`);
        const spinner = card.querySelector(`#spinner-${item.id}`);

        video.addEventListener('waiting', () => {
            spinner.classList.remove('hidden');
        });
        
        video.addEventListener('playing', () => {
            spinner.classList.add('hidden');
        });

        video.addEventListener('canplay', () => {
            spinner.classList.add('hidden');
        });

        // Load duration dynamically once metadata is loaded
        video.addEventListener('loadedmetadata', () => {
            const min = Math.floor(video.duration / 60);
            const sec = Math.floor(video.duration % 60).toString().padStart(2, '0');
            const durStr = `${min}:${sec}`;
            item.duration = durStr;
            
            const label = document.getElementById(`duration-label-${item.id}`);
            if (label) {
                label.innerHTML = `<i data-lucide="clock" class="h-2.5 w-2.5"></i> ${durStr}`;
                lucide.createIcons();
            }
        });

        card.addEventListener('mouseenter', () => {
            const playPromise = video.play();
            if (playPromise !== undefined) {
                playPromise.catch(error => {
                    console.log("Autoplay prevented by browser safety", error);
                });
            }
        });

        card.addEventListener('mouseleave', () => {
            video.pause();
            video.currentTime = 0;
            spinner.classList.add('hidden');
        });
    });

    lucide.createIcons();
}

// TACTILE CARD AUDIO TOGGLE
function toggleCardMute(event, itemId) {
    event.stopPropagation();
    const video = document.getElementById(`video-${itemId}`);
    const btn = document.getElementById(`mute-btn-${itemId}`);
    
    if (video.muted) {
        video.muted = false;
        btn.innerHTML = `<i data-lucide="volume-2" class="h-3.5 w-3.5"></i>`;
        btn.classList.add('bg-brand-500/20', 'border-brand-500/30', 'text-brand-400');
    } else {
        video.muted = true;
        btn.innerHTML = `<i data-lucide="volume-x" class="h-3.5 w-3.5"></i>`;
        btn.classList.remove('bg-brand-500/20', 'border-brand-500/30', 'text-brand-400');
        showToast("Audio Muted", "Hover preview will play silently.", "info");
    }
    lucide.createIcons();
}

// TAG CLICK SEARCH
function clickTag(tag) {
    searchInput.value = tag;
    handleSearch(tag);
}

// TOAST NOTIFICATIONS SYSTEM
function showToast(title, message, type = "success") {
    const toastContainer = document.getElementById('toast-container');
    const toastId = 'toast-' + Math.random().toString(36).substr(2, 9);
    
    let icon = "check-circle";
    let colorClass = "border-emerald-500/20 text-emerald-400 bg-slate-900/90";
    if (type === "warning") {
        icon = "alert-triangle";
        colorClass = "border-yellow-500/20 text-yellow-400 bg-slate-900/90";
    } else if (type === "info") {
        icon = "info";
        colorClass = "border-sky-500/20 text-sky-400 bg-slate-900/90";
    }

    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = `flex gap-3 items-start p-4 rounded-xl border backdrop-blur-md shadow-xl transition-all duration-300 translate-y-2 opacity-0 max-w-sm ${colorClass}`;
    toast.innerHTML = `
        <i data-lucide="${icon}" class="h-5 w-5 flex-shrink-0 mt-0.5"></i>
        <div>
            <h5 class="text-xs font-bold text-white">${title}</h5>
            <p class="text-[11px] text-slate-400 mt-0.5 leading-normal">${message}</p>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    lucide.createIcons();

    setTimeout(() => {
        toast.classList.remove('translate-y-2', 'opacity-0');
    }, 50);

    setTimeout(() => {
        toast.classList.add('translate-y-2', 'opacity-0');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3500);
}

// MODAL DETAILED VIEW
let activeModalMeme = null;

function openModal(itemId) {
    const item = memeDatabase.find(i => i.id === itemId);
    if (!item) return;

    activeModalMeme = item;
    
    modalTitle.textContent = item.name;
    modalDesc.textContent = item.description;
    modalRes.textContent = item.resolution;
    modalDownloadBtn.href = item.path;

    modalSpinner.classList.remove('hidden');
    modalVideo.src = item.path;
    modalVideo.load();
    
    modalVideo.addEventListener('canplay', () => {
        modalSpinner.classList.add('hidden');
        modalVideo.play().catch(() => {});
    }, { once: true });

    detailModal.classList.remove('opacity-0', 'pointer-events-none');
    lucide.createIcons();
}

function closeModal() {
    detailModal.classList.add('opacity-0', 'pointer-events-none');
    modalVideo.pause();
    modalVideo.src = '';
    activeModalMeme = null;
}
