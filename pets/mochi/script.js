let bridge = null;
let dragging = false;
let pointerDown = false;
let moved = false;
let lastX = 0;
let lastY = 0;
let startX = 0;
let startY = 0;
let clickTimer = null;
let reactionTimer = null;

const DRAG_THRESHOLD = 6;
const CLICK_DELAY = 220;

const root = document.getElementById('pet-root');
const bubble = document.getElementById('bubble');
const hitbox = document.getElementById('cat-hitbox');

function setState(state, message) {
  // Update only the state class.
  // Do NOT remove petting, dragging, interacting, etc.
  Array.from(root.classList)
    .filter(cls => cls.startsWith('state-'))
    .forEach(cls => root.classList.remove(cls));

  root.classList.add(`state-${state}`);

  root.dataset.state = state;
  root.dataset.stateMessage = message || '';

  // While hovering, keep the petting message.
  if (
    !root.classList.contains('petting') &&
    !root.classList.contains('dragging') &&
    !root.classList.contains('interacting') &&
    !root.classList.contains('special')
  ) {
    bubble.textContent = message || '';
    bubble.style.display = message ? 'block' : 'none';
  }
}

window.doompetsSetMessages = function(messages) {
  window._doompetsMessages = messages || {};
};

window.doompetsSetState = setState;

function restoreStateMessage() {
  const state = root.dataset.state || 'normal';
  const message = root.dataset.stateMessage || '';
  bubble.textContent = message;
  bubble.style.display = message ? 'block' : 'none';
}

function clearReactionClasses() {
  root.classList.remove('interacting', 'special');
  if (!dragging && !root.classList.contains('petting')) {
    restoreStateMessage();
  }
}

function showReaction(kind, message, duration = 1100) {
  clearTimeout(reactionTimer);
  root.classList.remove('interacting', 'special');
  root.classList.add(kind);

  if (message) {
    bubble.textContent = message;
    bubble.style.display = 'block';
  }

  reactionTimer = setTimeout(() => {
    root.classList.remove(kind);
    restoreStateMessage();
  }, duration);
}

function updateLook(event) {
  if (dragging) return;

  const rect = hitbox.getBoundingClientRect();
  const x = event.clientX - (rect.left + rect.width / 2);
  const y = event.clientY - (rect.top + rect.height / 2);

  root.classList.remove('look-left', 'look-right', 'look-up', 'look-center');

  if (y < -rect.height * 0.20) {
    root.classList.add('look-up');
  } else if (x < -rect.width * 0.16) {
    root.classList.add('look-left');
  } else if (x > rect.width * 0.16) {
    root.classList.add('look-right');
  } else {
    root.classList.add('look-center');
  }
}

function startPointer(event) {
  pointerDown = true;
  moved = false;
  lastX = startX = event.screenX;
  lastY = startY = event.screenY;
  hitbox.setPointerCapture?.(event.pointerId);
  event.preventDefault();
}

function movePointer(event) {
  updateLook(event);

  if (!pointerDown) return;

  const dxFromStart = event.screenX - startX;
  const dyFromStart = event.screenY - startY;
  const distance = Math.hypot(dxFromStart, dyFromStart);

  if (!dragging && distance >= DRAG_THRESHOLD) {
    dragging = true;
    moved = true;
    root.classList.add('dragging');
    root.classList.remove('petting', 'interacting', 'special');
    bubble.style.display = 'none';
    if (bridge) bridge.begin_drag();
  }

  if (!dragging) return;

  const dx = event.screenX - lastX;
  const dy = event.screenY - lastY;
  lastX = event.screenX;
  lastY = event.screenY;

  if (bridge) {
    bridge.move_pet(dx, dy);
  }

  event.preventDefault();
}

function endPointer(event) {
  if (!pointerDown) return;

  pointerDown = false;
  hitbox.releasePointerCapture?.(event.pointerId);

  if (dragging) {
    dragging = false;
    root.classList.remove('dragging');
    if (bridge) bridge.end_drag();
    restoreStateMessage();
  } else if (!moved) {
    scheduleSingleClickReaction();
  }

  event.preventDefault();
}

function scheduleSingleClickReaction() {
  clearTimeout(clickTimer);
  clickTimer = setTimeout(() => {
    showReaction('interacting', 'mrrp! 🐾', 800);
  }, CLICK_DELAY);
}

function handleDoubleClick(event) {
  clearTimeout(clickTimer);
  showReaction('special', 'hehe... zoomies! ✨', 1300);
  event.preventDefault();
}

hitbox.addEventListener('pointerenter', () => {
  if (!dragging) {
    root.classList.add('petting');
    bubble.textContent = 'purrr... ♥';
    bubble.style.display = 'block';
  }
});

hitbox.addEventListener('pointerleave', () => {
  root.classList.remove('petting');
  if (!dragging && !root.classList.contains('interacting') && !root.classList.contains('special')) {
    restoreStateMessage();
  }
  root.classList.remove('look-left', 'look-right', 'look-up', 'look-center');
});

hitbox.addEventListener('pointerdown', startPointer);
hitbox.addEventListener('pointermove', movePointer);
hitbox.addEventListener('pointerup', endPointer);
hitbox.addEventListener('pointercancel', endPointer);
hitbox.addEventListener('dblclick', handleDoubleClick);

try {
  new QWebChannel(qt.webChannelTransport, (channel) => {
    bridge = channel.objects.doompets;
  });
} catch (_) {
  // Browser preview mode: dragging only moves the pet inside the page.
  hitbox.addEventListener('pointermove', (event) => {
    if (!bridge || !dragging) return;
    hitbox.style.left = `calc(50% + ${event.screenX - startX}px)`;
    hitbox.style.bottom = `calc(-4px - ${event.screenY - startY}px)`;
  });
}
