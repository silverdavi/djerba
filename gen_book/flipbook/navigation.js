/**
 * Silver Cooks Flipbook - Navigation Module
 * Handles TOC, search, and recipe navigation
 */

// Global state
const AppState = {
  recipes: [],
  currentRecipeIndex: 0,
  currentPage: 0,
  totalPages: 0,
  pagesPerRecipe: 4,
  tocOpen: true,
  zoomLevel: 100,
  searchIndex: null
};

// Initialize navigation
document.addEventListener('DOMContentLoaded', () => {
  loadSearchIndex();
  setupEventListeners();
});

/**
 * Load search index from JSON
 */
async function loadSearchIndex() {
  try {
    const response = await fetch('search-index.json');
    if (!response.ok) throw new Error('Failed to load search index');
    
    const data = await response.json();
    AppState.recipes = data.recipes;
    AppState.totalPages = data.recipes.length * AppState.pagesPerRecipe + 5; // +5 for front matter
    AppState.searchIndex = data;
    
    renderTOC();
    updatePageIndicator();
    updateRecipeCount();
  } catch (err) {
    console.error('Error loading search index:', err);
    // Try loading from embedded data
    const embedded = document.getElementById('search-data');
    if (embedded) {
      try {
        const data = JSON.parse(embedded.textContent);
        AppState.recipes = data.recipes;
        AppState.totalPages = data.recipes.length * AppState.pagesPerRecipe + 5;
        AppState.searchIndex = data;
        renderTOC();
        updatePageIndicator();
        updateRecipeCount();
      } catch (e) {
        console.error('Failed to parse embedded data:', e);
      }
    }
  }
}

/**
 * Set up all event listeners
 */
function setupEventListeners() {
  // TOC toggle
  document.getElementById('toc-toggle').addEventListener('click', toggleTOC);
  
  // Search
  const searchInput = document.getElementById('search-input');
  searchInput.addEventListener('input', handleSearch);
  searchInput.addEventListener('focus', () => {
    if (searchInput.value.trim()) handleSearch({ target: searchInput });
  });
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-box')) {
      document.getElementById('search-results').classList.add('hidden');
    }
  });
  
  // Zoom controls
  document.getElementById('zoom-in').addEventListener('click', () => adjustZoom(10));
  document.getElementById('zoom-out').addEventListener('click', () => adjustZoom(-10));
  
  // Fullscreen
  document.getElementById('fullscreen').addEventListener('click', toggleFullscreen);
  
  // Navigation
  document.getElementById('prev-recipe').addEventListener('click', prevRecipe);
  document.getElementById('next-recipe').addEventListener('click', nextRecipe);
  document.getElementById('prev-page').addEventListener('click', prevPage);
  document.getElementById('next-page').addEventListener('click', nextPage);
  
  // Keyboard navigation
  document.addEventListener('keydown', handleKeyboard);
}

/**
 * Render Table of Contents
 */
function renderTOC() {
  const tocList = document.getElementById('toc-list');
  tocList.innerHTML = '';
  
  AppState.recipes.forEach((recipe, index) => {
    const item = document.createElement('div');
    item.className = 'toc-item' + (index === AppState.currentRecipeIndex ? ' active' : '');
    item.dataset.index = index;
    
    const num = document.createElement('span');
    num.className = 'toc-item-num';
    num.textContent = (index + 1).toString().padStart(2, '0');
    
    const name = document.createElement('span');
    name.className = 'toc-item-name';
    name.textContent = recipe.names.en;
    
    const subName = document.createElement('span');
    subName.className = 'toc-item-name-sub';
    subName.textContent = `${recipe.names.he} • ${recipe.names.ar}`;
    
    item.appendChild(num);
    item.appendChild(name);
    item.appendChild(subName);
    
    item.addEventListener('click', () => goToRecipe(index));
    tocList.appendChild(item);
  });
}

/**
 * Update TOC active state
 */
function updateTOCActive() {
  const items = document.querySelectorAll('.toc-item');
  items.forEach((item, index) => {
    item.classList.toggle('active', index === AppState.currentRecipeIndex);
  });
  
  // Scroll active item into view
  const activeItem = document.querySelector('.toc-item.active');
  if (activeItem) {
    activeItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

/**
 * Toggle TOC sidebar
 */
function toggleTOC() {
  const sidebar = document.getElementById('toc-sidebar');
  sidebar.classList.toggle('collapsed');
  AppState.tocOpen = !sidebar.classList.contains('collapsed');
}

/**
 * Handle search input
 */
function handleSearch(e) {
  const query = e.target.value.trim().toLowerCase();
  const resultsContainer = document.getElementById('search-results');
  
  if (!query) {
    resultsContainer.classList.add('hidden');
    return;
  }
  
  const results = AppState.recipes.filter(recipe => {
    // Search in all language names
    const names = Object.values(recipe.names).join(' ').toLowerCase();
    if (names.includes(query)) return true;
    
    // Search in ingredients
    if (recipe.ingredients) {
      const ingredients = recipe.ingredients.join(' ').toLowerCase();
      if (ingredients.includes(query)) return true;
    }
    
    return false;
  });
  
  if (results.length === 0) {
    resultsContainer.innerHTML = '<div class="search-result"><span class="search-result-name">No results found</span></div>';
  } else {
    resultsContainer.innerHTML = results.slice(0, 10).map(recipe => {
      const index = AppState.recipes.indexOf(recipe);
      return `
        <div class="search-result" data-index="${index}">
          <div class="search-result-name">${recipe.names.en}</div>
          <div class="search-result-langs">${recipe.names.he} • ${recipe.names.es} • ${recipe.names.ar}</div>
        </div>
      `;
    }).join('');
    
    // Add click handlers
    resultsContainer.querySelectorAll('.search-result').forEach(item => {
      item.addEventListener('click', () => {
        const index = parseInt(item.dataset.index);
        if (!isNaN(index)) {
          goToRecipe(index);
          resultsContainer.classList.add('hidden');
          document.getElementById('search-input').value = '';
        }
      });
    });
  }
  
  resultsContainer.classList.remove('hidden');
}

/**
 * Navigate to specific recipe
 */
function goToRecipe(index) {
  if (index < 0 || index >= AppState.recipes.length) return;
  
  AppState.currentRecipeIndex = index;
  // Front matter is 5 pages, then 4 pages per recipe
  AppState.currentPage = 5 + (index * AppState.pagesPerRecipe);
  
  updateTOCActive();
  updatePageIndicator();
  updateNavButtons();
  
  // Notify flipbook to turn to page
  if (window.pageFlip) {
    window.pageFlip.turnToPage(AppState.currentPage);
  }
}

/**
 * Previous recipe
 */
function prevRecipe() {
  if (AppState.currentRecipeIndex > 0) {
    goToRecipe(AppState.currentRecipeIndex - 1);
  }
}

/**
 * Next recipe
 */
function nextRecipe() {
  if (AppState.currentRecipeIndex < AppState.recipes.length - 1) {
    goToRecipe(AppState.currentRecipeIndex + 1);
  }
}

/**
 * Previous page
 */
function prevPage() {
  if (AppState.currentPage > 0) {
    AppState.currentPage--;
    updateCurrentRecipeFromPage();
    updatePageIndicator();
    updateNavButtons();
    
    if (window.pageFlip) {
      window.pageFlip.flipPrev();
    }
  }
}

/**
 * Next page
 */
function nextPage() {
  if (AppState.currentPage < AppState.totalPages - 1) {
    AppState.currentPage++;
    updateCurrentRecipeFromPage();
    updatePageIndicator();
    updateNavButtons();
    
    if (window.pageFlip) {
      window.pageFlip.flipNext();
    }
  }
}

/**
 * Update current recipe index based on page number
 */
function updateCurrentRecipeFromPage() {
  if (AppState.currentPage < 5) {
    // Front matter
    AppState.currentRecipeIndex = 0;
  } else {
    AppState.currentRecipeIndex = Math.floor((AppState.currentPage - 5) / AppState.pagesPerRecipe);
  }
  updateTOCActive();
}

/**
 * Update page indicator display
 */
function updatePageIndicator() {
  document.getElementById('current-page').textContent = AppState.currentPage + 1;
  document.getElementById('total-pages').textContent = AppState.totalPages;
}

/**
 * Update recipe count display
 */
function updateRecipeCount() {
  document.getElementById('recipe-count').textContent = `${AppState.recipes.length} recipes`;
}

/**
 * Update navigation button states
 */
function updateNavButtons() {
  document.getElementById('prev-recipe').disabled = AppState.currentRecipeIndex <= 0;
  document.getElementById('next-recipe').disabled = AppState.currentRecipeIndex >= AppState.recipes.length - 1;
}

/**
 * Adjust zoom level
 */
function adjustZoom(delta) {
  AppState.zoomLevel = Math.max(50, Math.min(200, AppState.zoomLevel + delta));
  document.getElementById('zoom-level').textContent = `${AppState.zoomLevel}%`;
  
  const container = document.getElementById('flipbook-container');
  container.style.transform = `scale(${AppState.zoomLevel / 100})`;
  container.style.transformOrigin = 'center center';
}

/**
 * Toggle fullscreen mode
 */
function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(err => {
      console.log('Fullscreen error:', err);
    });
  } else {
    document.exitFullscreen();
  }
}

/**
 * Handle keyboard navigation
 */
function handleKeyboard(e) {
  // Don't handle if typing in search
  if (e.target.tagName === 'INPUT') return;
  
  switch (e.key) {
    case 'ArrowLeft':
      e.preventDefault();
      if (e.shiftKey) prevRecipe();
      else prevPage();
      break;
    case 'ArrowRight':
      e.preventDefault();
      if (e.shiftKey) nextRecipe();
      else nextPage();
      break;
    case 'ArrowUp':
      e.preventDefault();
      prevRecipe();
      break;
    case 'ArrowDown':
      e.preventDefault();
      nextRecipe();
      break;
    case 'Home':
      e.preventDefault();
      goToRecipe(0);
      break;
    case 'End':
      e.preventDefault();
      goToRecipe(AppState.recipes.length - 1);
      break;
    case 'Escape':
      document.getElementById('search-results').classList.add('hidden');
      break;
    case 'f':
      if (e.ctrlKey || e.metaKey) {
        e.preventDefault();
        document.getElementById('search-input').focus();
      }
      break;
    case '+':
    case '=':
      if (e.ctrlKey || e.metaKey) {
        e.preventDefault();
        adjustZoom(10);
      }
      break;
    case '-':
      if (e.ctrlKey || e.metaKey) {
        e.preventDefault();
        adjustZoom(-10);
      }
      break;
  }
}

/**
 * Called by flipbook when page changes
 */
function onPageChange(pageNum) {
  AppState.currentPage = pageNum;
  updateCurrentRecipeFromPage();
  updatePageIndicator();
  updateNavButtons();
}

// Export for flipbook.js
window.AppState = AppState;
window.onPageChange = onPageChange;
window.goToRecipe = goToRecipe;

