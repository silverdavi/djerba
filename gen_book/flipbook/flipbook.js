/**
 * Silver Cooks Flipbook - PageFlip.js Integration
 * LAZY LOADING VERSION - Only loads pages as needed
 */

// PageFlip instance
let pageFlip = null;

// Page cache
const pageCache = new Map();
const loadingPages = new Set();

// Configuration
const CONFIG = {
  pageWidth: 600,
  pageHeight: 600,
  maxShadowOpacity: 0.3,
  showCover: false,
  mobileScrollSupport: true,
  swipeDistance: 30,
  clickEventForward: true,
  useMouseEvents: true,
  flippingTime: 800,
  usePortrait: true,
  autoSize: true,
  drawShadow: true,
  startPage: 0,
  preloadAhead: 2  // Preload 2 pages ahead
};

// Initialize when DOM ready
document.addEventListener('DOMContentLoaded', initFlipbook);

/**
 * Initialize the flipbook with lazy loading
 */
async function initFlipbook() {
  const container = document.getElementById('flipbook');
  container.innerHTML = '<div class="loading">Loading cookbook...</div>';
  
  // Wait for recipe list
  await waitForRecipes();
  
  const totalRecipes = window.AppState.recipes.length;
  const totalPages = 5 + (totalRecipes * 4); // 5 front matter + 4 per recipe
  
  // Create placeholder pages
  const pages = createPlaceholderPages(totalPages);
  
  // Create PageFlip
  pageFlip = new St.PageFlip(container, {
    width: CONFIG.pageWidth,
    height: CONFIG.pageHeight,
    maxShadowOpacity: CONFIG.maxShadowOpacity,
    showCover: CONFIG.showCover,
    mobileScrollSupport: CONFIG.mobileScrollSupport,
    swipeDistance: CONFIG.swipeDistance,
    clickEventForward: CONFIG.clickEventForward,
    useMouseEvents: CONFIG.useMouseEvents,
    flippingTime: CONFIG.flippingTime,
    usePortrait: CONFIG.usePortrait,
    autoSize: CONFIG.autoSize,
    drawShadow: CONFIG.drawShadow,
    startPage: CONFIG.startPage
  });
  
  pageFlip.loadFromHTML(pages);
  
  // Set up page change listener for lazy loading
  pageFlip.on('flip', (e) => {
    const pageNum = e.data;
    if (window.onPageChange) window.onPageChange(pageNum);
    
    // Lazy load visible and nearby pages
    loadPageRange(pageNum - CONFIG.preloadAhead, pageNum + CONFIG.preloadAhead + 2);
  });
  
  // Export for navigation
  window.pageFlip = {
    turnToPage: (pageNum) => {
      loadPageRange(pageNum - 1, pageNum + 3);
      setTimeout(() => pageFlip.turnToPage(pageNum), 50);
    },
    flipNext: () => pageFlip.flipNext(),
    flipPrev: () => pageFlip.flipPrev(),
    getCurrentPageIndex: () => pageFlip.getCurrentPageIndex()
  };
  
  // Load initial pages (first recipe)
  loadPageRange(0, 8);
  
  console.log(`Flipbook ready with ${totalPages} pages (lazy loading)`);
}

/**
 * Wait for recipes to load
 */
function waitForRecipes() {
  return new Promise((resolve) => {
    const check = () => {
      if (window.AppState?.recipes?.length > 0) resolve();
      else setTimeout(check, 100);
    };
    check();
  });
}

/**
 * Create placeholder pages
 */
function createPlaceholderPages(count) {
  const pages = [];
  for (let i = 0; i < count; i++) {
    const div = document.createElement('div');
    div.className = 'flipbook-page placeholder-page';
    div.dataset.pageIndex = i;
    div.innerHTML = `
      <div class="page-loading">
        <div class="loading-spinner"></div>
      </div>
    `;
    pages.push(div);
  }
  return pages;
}

/**
 * Load a range of pages
 */
function loadPageRange(start, end) {
  const totalPages = 5 + (window.AppState.recipes.length * 4);
  start = Math.max(0, start);
  end = Math.min(totalPages - 1, end);
  
  for (let i = start; i <= end; i++) {
    loadPage(i);
  }
}

/**
 * Load a single page
 */
async function loadPage(pageIndex) {
  // Skip if already loaded or loading
  if (pageCache.has(pageIndex) || loadingPages.has(pageIndex)) return;
  
  loadingPages.add(pageIndex);
  
  try {
    const content = await fetchPageContent(pageIndex);
    if (content) {
      updatePageContent(pageIndex, content);
      pageCache.set(pageIndex, true);
    }
  } catch (err) {
    console.error(`Failed to load page ${pageIndex}:`, err);
  } finally {
    loadingPages.delete(pageIndex);
  }
}

/**
 * Fetch page content based on index
 */
async function fetchPageContent(pageIndex) {
  // Front matter pages (0-4)
  if (pageIndex < 5) {
    return getFrontMatterContent(pageIndex);
  }
  
  // Recipe pages
  const recipePageIndex = pageIndex - 5;
  const recipeIndex = Math.floor(recipePageIndex / 4);
  const pageInRecipe = recipePageIndex % 4;
  
  if (recipeIndex >= window.AppState.recipes.length) return null;
  
  const recipe = window.AppState.recipes[recipeIndex];
  return await fetchRecipePageContent(recipe.id, pageInRecipe, recipeIndex + 1);
}

/**
 * Get front matter content
 */
function getFrontMatterContent(pageIndex) {
  const pages = [
    '<div class="front-matter title-page"><h1>Silver Cooks</h1><p>Four-Language Cookbook</p></div>',
    '<div class="front-matter copyright-page"><p>© 2025 David & Enny Silver</p></div>',
    '<div class="front-matter intro-page"><h2>Introduction</h2><p>Recipes from Djerba & Tangier</p></div>',
    '<div class="front-matter intro-page"><h2>Introducción</h2><p>Plant-based cooking traditions</p></div>',
    '<div class="front-matter blank-page"></div>'
  ];
  return pages[pageIndex] || '';
}

/**
 * Fetch recipe page content from HTML file
 */
async function fetchRecipePageContent(recipeId, pageInRecipe, chapterNum) {
  try {
    const response = await fetch(`recipes/${recipeId}.html`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    
    const html = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    
    // Get the specific page section
    const pages = doc.querySelectorAll('.page');
    if (pages[pageInRecipe]) {
      return pages[pageInRecipe].innerHTML;
    }
    
    return `<div class="page-error">Page not found</div>`;
  } catch (err) {
    return `<div class="page-error">
      <p>Recipe: ${recipeId}</p>
      <p>Page ${pageInRecipe + 1}</p>
    </div>`;
  }
}

/**
 * Update page content in the flipbook
 */
function updatePageContent(pageIndex, content) {
  // Find the page element
  const pages = document.querySelectorAll('.flipbook-page');
  if (pages[pageIndex]) {
    pages[pageIndex].innerHTML = content;
    pages[pageIndex].classList.remove('placeholder-page');
    pages[pageIndex].classList.add('loaded-page');
  }
}

/**
 * Apply page styles
 */
function applyPageStyles() {
  const style = document.createElement('style');
  style.textContent = `
    .flipbook-page {
      background: #faf6f1;
      width: 100%;
      height: 100%;
      overflow: hidden;
    }
    
    .flipbook-page.placeholder-page {
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .page-loading {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: #999;
    }
    
    .loading-spinner {
      width: 32px;
      height: 32px;
      border: 3px solid #f3d7b4;
      border-top-color: #d9925b;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    
    .page-error {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      color: #999;
      font-size: 0.9rem;
    }
    
    .front-matter {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      padding: 2rem;
      text-align: center;
    }
    
    .front-matter h1 {
      font-family: "Bona Nova", serif;
      font-size: 2.5rem;
      color: #d9925b;
      margin-bottom: 1rem;
    }
    
    .front-matter h2 {
      font-family: "Bona Nova", serif;
      font-size: 1.8rem;
      color: #d9925b;
      margin-bottom: 0.5rem;
    }
    
    .front-matter p {
      color: #666;
      font-size: 1rem;
    }
    
    /* Scale down recipe content */
    .loaded-page .page-inner {
      transform: scale(0.95);
      transform-origin: top left;
    }
  `;
  document.head.appendChild(style);
}

applyPageStyles();

/**
 * Touch gesture handling
 */
let touchStartX = 0;

document.addEventListener('touchstart', (e) => {
  touchStartX = e.changedTouches[0].screenX;
}, { passive: true });

document.addEventListener('touchend', (e) => {
  const diff = touchStartX - e.changedTouches[0].screenX;
  if (Math.abs(diff) > 50) {
    if (diff > 0 && window.pageFlip) window.pageFlip.flipNext();
    else if (window.pageFlip) window.pageFlip.flipPrev();
  }
}, { passive: true });

/**
 * Debounced resize handler
 */
let resizeTimeout;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    console.log('Window resized');
  }, 250);
});
