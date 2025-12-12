/**
 * Silver Cooks - Simple Recipe Viewer
 * Includes front matter pages + recipes
 */

let pages = [];  // Combined: front matter + recipes
let currentIndex = 0;

// Front matter pages
const FRONT_MATTER = [
  { id: '_title', names: { en: 'Silver Cooks', he: 'מטבח כסף', ar: 'مطبخ سيلفر', es: 'Silver Cooks' }, type: 'front' },
  { id: '_copyright', names: { en: 'Copyright & Credits', he: 'זכויות יוצרים', ar: 'حقوق النشر', es: 'Derechos de autor' }, type: 'front' },
  { id: '_intro1', names: { en: 'Introduction (EN/HE)', he: 'הקדמה', ar: 'مقدمة', es: 'Introducción' }, type: 'front' },
  { id: '_intro2', names: { en: 'Introduction (ES/AR)', he: 'הקדמה', ar: 'مقدمة', es: 'Introducción' }, type: 'front' }
];

// Initialize
document.addEventListener('DOMContentLoaded', init);

async function init() {
  // Load recipe list
  try {
    const res = await fetch('search-index.json');
    const data = await res.json();
    // Combine front matter + recipes
    pages = [...FRONT_MATTER, ...data.recipes.map(r => ({ ...r, type: 'recipe' }))];
  } catch (e) {
    console.error('Failed to load recipes:', e);
    return;
  }
  
  renderRecipeList();
  setupEvents();
  
  // Load title page first
  if (pages.length > 0) {
    loadRecipe(0);
  }
}

function renderRecipeList() {
  const list = document.getElementById('recipe-list');
  
  list.innerHTML = pages.map((p, i) => {
    const isFront = p.type === 'front';
    const numDisplay = isFront ? '—' : (i - FRONT_MATTER.length + 1).toString().padStart(2, '0');
    const itemClass = isFront ? 'recipe-item front-matter-item' : 'recipe-item';
    
    return `
      <div class="${itemClass}${i === 0 ? ' active' : ''}" data-index="${i}">
        <span class="recipe-item-num">${numDisplay}</span>
        <span class="recipe-item-name">${p.names.en}</span>
        ${!isFront ? `<div class="recipe-item-sub">${p.names.he} • ${p.names.ar}</div>` : ''}
      </div>
    `;
  }).join('');
  
  // Click handlers
  list.querySelectorAll('.recipe-item').forEach(item => {
    item.addEventListener('click', () => {
      loadRecipe(parseInt(item.dataset.index));
    });
  });
}

function loadRecipe(index) {
  if (index < 0 || index >= pages.length) return;
  
  currentIndex = index;
  const page = pages[index];
  
  // Load in iframe - front matter uses different path
  const iframe = document.getElementById('recipe-iframe');
  iframe.src = `recipes/${page.id}.html`;
  
  // Update UI
  updateUI();
}

function updateUI() {
  // Update indicator
  const page = pages[currentIndex];
  const isFront = page.type === 'front';
  const recipeNum = isFront ? page.names.en : (currentIndex - FRONT_MATTER.length + 1);
  const totalRecipes = pages.length - FRONT_MATTER.length;
  
  document.getElementById('recipe-indicator').textContent = isFront 
    ? page.names.en 
    : `${recipeNum} / ${totalRecipes}`;
  
  // Update nav buttons
  document.getElementById('prev-btn').disabled = currentIndex === 0;
  document.getElementById('next-btn').disabled = currentIndex === pages.length - 1;
  
  // Update active item in list
  document.querySelectorAll('.recipe-item').forEach((item, i) => {
    item.classList.toggle('active', i === currentIndex);
  });
  
  // Scroll active into view
  const activeItem = document.querySelector('.recipe-item.active');
  if (activeItem) {
    activeItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

function setupEvents() {
  // Navigation
  document.getElementById('prev-btn').addEventListener('click', () => {
    loadRecipe(currentIndex - 1);
  });
  
  document.getElementById('next-btn').addEventListener('click', () => {
    loadRecipe(currentIndex + 1);
  });
  
  // Sidebar toggle
  document.getElementById('toc-toggle').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('hidden');
  });
  
  document.getElementById('sidebar-close').addEventListener('click', () => {
    document.getElementById('sidebar').classList.add('hidden');
  });
  
  // Search
  const searchInput = document.getElementById('search-input');
  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    filterRecipes(query);
  });
  
  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT') return;
    
    switch (e.key) {
      case 'ArrowLeft':
        e.preventDefault();
        loadRecipe(currentIndex - 1);
        break;
      case 'ArrowRight':
        e.preventDefault();
        loadRecipe(currentIndex + 1);
        break;
      case 'Home':
        e.preventDefault();
        loadRecipe(0);
        break;
      case 'End':
        e.preventDefault();
        loadRecipe(pages.length - 1);
        break;
    }
  });
}

function filterRecipes(query) {
  const items = document.querySelectorAll('.recipe-item');
  
  if (!query) {
    items.forEach(item => item.style.display = '');
    return;
  }
  
  items.forEach((item, i) => {
    const page = pages[i];
    const text = Object.values(page.names).join(' ').toLowerCase();
    const match = text.includes(query);
    item.style.display = match ? '' : 'none';
  });
}

