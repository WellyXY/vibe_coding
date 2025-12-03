const DATA_FILE = 'users_database.json';
const STACK_SIZE = 3;
const stackEl = document.getElementById('cardStack');
const cardTemplate = document.getElementById('card-template');

let recommendations = [];
let frontIndex = 0;
let nextDataIndex = 0;
let activeCard = null;
let isAnimating = false;
let isDragging = false;
let startX = 0;
let currentX = 0;

init();

async function init() {
  try {
    const res = await fetch(DATA_FILE);
    recommendations = await res.json();
    if (!recommendations.length) return;
    buildInitialStack();
  } catch (error) {
    console.error('Unable to load recommendations_example1.json', error);
  }
}

function buildInitialStack() {
  stackEl.innerHTML = '';
  const deckCount = Math.min(STACK_SIZE, recommendations.length);
  for (let offset = deckCount - 1; offset >= 0; offset--) {
    const dataIndex = (frontIndex + deckCount - 1 - offset) % recommendations.length;
    const card = createCard(dataIndex);
    stackEl.appendChild(card);
  }
  nextDataIndex = (frontIndex + deckCount) % recommendations.length;
  updatePositions();
  attachKeyboardControls();
}

function createCard(dataIndex) {
  const person = recommendations[dataIndex];
  const fragment = cardTemplate.content.cloneNode(true);
  const card = fragment.querySelector('.swipe-card');
  card.dataset.index = String(dataIndex);
  populateCard(card, person);
  return card;
}

function populateCard(card, person) {
  const img = card.querySelector('[data-card-image]');
  img.src = person.image;
  img.alt = person.name;
  card.querySelector('[data-card-name]').textContent = person.name;
  card.querySelector('[data-card-pill]').textContent = person.occupation || 'Profile';
  const locationEl = card.querySelector('[data-card-location]');
  if (locationEl) {
    locationEl.textContent = person.location || 'Somewhere';
  }

  const stats = calculateStats(person);
  card.querySelector('[data-card-likes]').textContent = stats.likes;
  card.querySelector('[data-card-posts]').textContent = stats.posts;
  card.querySelector('[data-card-followers]').textContent = stats.followers;
}

function calculateStats(person) {
  const hobbyBonus = (person.hobby?.length || 0) * 160;
  const likes = person.age * 400 + hobbyBonus + 1800;
  const posts = 150 + (person.id % 90) + hobbyBonus / 8;
  const followers = likes * 3.4;
  return {
    likes: formatCompact(likes),
    posts: Math.max(1, Math.round(posts)),
    followers: formatCompact(followers),
  };
}

function formatCompact(value) {
  return Intl.NumberFormat('en-US', {
    notation: 'compact',
    maximumFractionDigits: 1,
  }).format(Math.round(value));
}

function setCardStyle(card, position) {
  const translateY = position * 18;
  const scale = 1 - position * 0.05;
  card.style.zIndex = String(100 - position);
  card.style.opacity = String(1 - position * 0.18);
  card.style.transform = `translate3d(0, ${translateY}px, 0) scale(${scale})`;
  card.dataset.position = String(position);
}

function updatePositions() {
  const cards = Array.from(stackEl.children);
  for (let i = 0; i < cards.length; i++) {
    const card = cards[i];
    const position = cards.length - 1 - i;
    setCardStyle(card, position);
    if (position === 0) {
      card.style.pointerEvents = 'auto';
      enableInteractions(card);
    } else {
      disableInteractions(card);
    }
  }
  activeCard = cards[cards.length - 1] || null;
}

function enableInteractions(card) {
  if (card.dataset.interactive) return;
  card.dataset.interactive = '1';
  card.style.pointerEvents = 'auto';
  card.addEventListener('pointerdown', onPointerDown);
  card.addEventListener('pointermove', onPointerMove);
  card.addEventListener('pointerup', onPointerUp);
  card.addEventListener('pointercancel', onPointerUp);
  card.addEventListener('pointerleave', onPointerUp);
}

function disableInteractions(card) {
  card.style.pointerEvents = 'none';
}

function onPointerDown(event) {
  if (isAnimating) return;
  isDragging = true;
  startX = event.clientX;
  currentX = 0;
  activeCard = event.currentTarget;
  activeCard.setPointerCapture(event.pointerId);
  activeCard.classList.add('swipe-card--dragging');
  activeCard.style.transition = 'transform 0.05s linear';
  updateBadges(0);
}

function onPointerMove(event) {
  if (!isDragging || !activeCard) return;
  currentX = event.clientX - startX;
  const rotation = currentX / 14;
  activeCard.style.transform = `translate3d(${currentX}px, ${currentX / 25}px, 0) rotate(${rotation}deg)`;
  updateBadges(currentX);
}

function onPointerUp(event) {
  if (!isDragging || !activeCard) return;
  activeCard.releasePointerCapture(event.pointerId);
  activeCard.classList.remove('swipe-card--dragging');
  activeCard.style.transition = '';

  if (Math.abs(currentX) > 80) {
    performSwipe(currentX > 0 ? 1 : -1);
  } else {
    resetActiveCard();
  }
  updateBadges(0);
  isDragging = false;
  currentX = 0;
}

function resetActiveCard() {
  if (!activeCard) return;
  activeCard.style.transition = 'transform 0.35s ease';
  setCardStyle(activeCard, 0);
}

function attachKeyboardControls() {
  window.onkeydown = (event) => {
    if (isAnimating) return;
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      performSwipe(event.key === 'ArrowRight' ? 1 : -1);
    }
  };
}

function performSwipe(direction) {
  if (!activeCard || isAnimating) return;
  isAnimating = true;
  const target = activeCard;
  const distance = window.innerWidth * 0.85;
  target.style.transition = 'transform 0.35s ease, opacity 0.2s ease';
  target.style.transform = `translate3d(${direction * distance}px, -40px, 0) rotate(${direction * 28}deg)`;
  target.style.opacity = '0';
  target.addEventListener('transitionend', () => {
    updateBadges(0);
    target.remove();
    advanceDeck();
    isAnimating = false;
  }, { once: true });
}

function advanceDeck() {
  frontIndex = (frontIndex + 1) % recommendations.length;
  if (recommendations.length > stackEl.children.length) {
    const card = createCard(nextDataIndex);
    nextDataIndex = (nextDataIndex + 1) % recommendations.length;
    stackEl.insertBefore(card, stackEl.firstChild);
  }
  updatePositions();
}

window.findAndRender = function (location) {
  const index = recommendations.findIndex((p) => p.location?.toLowerCase().includes(location.toLowerCase()));
  if (index === -1) return false;
  frontIndex = index;
  nextDataIndex = (frontIndex + STACK_SIZE) % recommendations.length;
  buildInitialStack();
  return true;
};

function updateBadges(delta) {
  if (!activeCard) return;
  const likeBadge = activeCard.querySelector('.swipe-card__badge--like');
  const nopeBadge = activeCard.querySelector('.swipe-card__badge--nope');
  if (!likeBadge || !nopeBadge) return;
  const intensity = Math.min(Math.abs(delta) / 120, 1);
  if (delta > 0) {
    likeBadge.style.opacity = intensity;
    likeBadge.style.transform = `scale(${0.9 + intensity * 0.2})`;
    nopeBadge.style.opacity = 0;
    nopeBadge.style.transform = 'scale(0.9)';
  } else if (delta < 0) {
    nopeBadge.style.opacity = intensity;
    nopeBadge.style.transform = `scale(${0.9 + intensity * 0.2})`;
    likeBadge.style.opacity = 0;
    likeBadge.style.transform = 'scale(0.9)';
  } else {
    likeBadge.style.opacity = 0;
    nopeBadge.style.opacity = 0;
    likeBadge.style.transform = 'scale(0.9)';
    nopeBadge.style.transform = 'scale(0.9)';
  }
}

// Update stack with Gemini API recommendations
window.updateStackWithRecommendations = function (apiRecommendations) {
  if (!apiRecommendations || apiRecommendations.length === 0) {
    console.error('No recommendations provided');
    return false;
  }

  // Replace the recommendations array with API results
  recommendations = apiRecommendations;
  frontIndex = 0;
  nextDataIndex = Math.min(STACK_SIZE, recommendations.length);

  // Rebuild the stack
  buildInitialStack();

  console.log(`✅ Updated stack with ${recommendations.length} Gemini-ranked recommendations`);
  return true;
};
