const page = document.querySelector('.page');
const tabButtons = Array.from(document.querySelectorAll('.tabs__button'));
const tabPanels = Array.from(document.querySelectorAll('.tabs__panel'));
const scrollButtons = document.querySelectorAll('[data-scroll-to]');

function activateTab(id) {
  tabButtons.forEach((btn) => {
    const isTarget = btn.dataset.tab === id;
    btn.classList.toggle('is-active', isTarget);
    btn.setAttribute('aria-selected', isTarget);
  });

  tabPanels.forEach((panel) => {
    const isTarget = panel.id === id;
    panel.classList.toggle('is-active', isTarget);
    if (isTarget) {
      panel.focus();
    }
  });

  localStorage.setItem('puppy-enhanced-active-tab', id);
}

if (tabButtons.length) {
  tabButtons.forEach((btn) => {
    btn.addEventListener('click', () => activateTab(btn.dataset.tab));
  });

  const storedTab = localStorage.getItem('puppy-enhanced-active-tab');
  if (storedTab && tabPanels.some((panel) => panel.id === storedTab)) {
    activateTab(storedTab);
  }
}

scrollButtons.forEach((button) => {
  const targetId = button.dataset.scrollTo;
  button.addEventListener('click', () => {
    const target = document.getElementById(targetId);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// Diary handling
const diaryForm = document.getElementById('diary-form');
const diaryList = document.getElementById('diary-list');
const clearDiaryButton = document.getElementById('clear-diary');
const diaryDateInput = document.getElementById('diary-date');

const diaryStorageKey = 'puppy-enhanced-diary-entries';

function loadDiaryEntries() {
  const raw = localStorage.getItem(diaryStorageKey);
  try {
    return raw ? JSON.parse(raw) : [];
  } catch (error) {
    console.warn('Unable to parse diary entries, resetting storage.', error);
    localStorage.removeItem(diaryStorageKey);
    return [];
  }
}

function saveDiaryEntries(entries) {
  localStorage.setItem(diaryStorageKey, JSON.stringify(entries));
}

function renderDiary(entries) {
  diaryList.innerHTML = '';
  if (!entries.length) {
    diaryList.innerHTML = '<li class="diary__empty">No entries yet. Start recording today\'s milestones!</li>';
    return;
  }

  entries
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .forEach((entry) => {
      const li = document.createElement('li');
      li.className = 'diary__entry';
      li.innerHTML = `
        <div class="diary__entry-header">
          <span>${new Date(entry.date).toLocaleDateString(undefined, {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
          })}</span>
          <span class="entry-focus">${entry.focus}</span>
        </div>
        <p>${entry.text.replace(/\n/g, '<br />')}</p>
        <button class="ghost ghost--small" data-remove-entry="${entry.id}">Remove</button>
      `;
      diaryList.appendChild(li);
    });
}

const diaryEntries = loadDiaryEntries();
renderDiary(diaryEntries);

if (diaryForm) {
  if (diaryDateInput) {
    diaryDateInput.value = new Date().toISOString().split('T')[0];
  }

  diaryForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(diaryForm);
    const date = formData.get('date');
    const focus = formData.get('focus');
    const text = formData.get('entry').trim();

    if (!date || !text) {
      diaryForm.reportValidity();
      return;
    }

    diaryEntries.push({
      id: crypto.randomUUID(),
      date,
      focus,
      text
    });
    saveDiaryEntries(diaryEntries);
    renderDiary(diaryEntries);
    diaryForm.reset();
    if (diaryDateInput) {
      diaryDateInput.value = date;
    }
  });
}

if (clearDiaryButton) {
  clearDiaryButton.addEventListener('click', () => {
    if (confirm('Clear all saved diary entries? This cannot be undone.')) {
      diaryEntries.splice(0, diaryEntries.length);
      saveDiaryEntries(diaryEntries);
      renderDiary(diaryEntries);
    }
  });
}

diaryList.addEventListener('click', (event) => {
  const button = event.target.closest('[data-remove-entry]');
  if (!button) return;

  const id = button.dataset.removeEntry;
  const index = diaryEntries.findIndex((entry) => entry.id === id);
  if (index !== -1) {
    diaryEntries.splice(index, 1);
    saveDiaryEntries(diaryEntries);
    renderDiary(diaryEntries);
  }
});

// Persist socialization checklist state
const checklistForm = document.getElementById('socialization-form');
const checklistStorageKey = 'puppy-enhanced-socialization';

if (checklistForm) {
  const stored = localStorage.getItem(checklistStorageKey);
  if (stored) {
    try {
      const values = JSON.parse(stored);
      checklistForm.querySelectorAll('input[type="checkbox"]').forEach((checkbox) => {
        checkbox.checked = values.includes(checkbox.value);
      });
    } catch (error) {
      console.warn('Unable to parse checklist state, resetting.', error);
      localStorage.removeItem(checklistStorageKey);
    }
  }

  checklistForm.addEventListener('change', () => {
    const selected = Array.from(checklistForm.querySelectorAll('input[type="checkbox"]'))
      .filter((checkbox) => checkbox.checked)
      .map((checkbox) => checkbox.value);
    localStorage.setItem(checklistStorageKey, JSON.stringify(selected));
  });
}

// Decorative background interaction
if (page) {
  document.addEventListener('mousemove', (event) => {
    const x = (event.clientX / window.innerWidth - 0.5) * 6;
    const y = (event.clientY / window.innerHeight - 0.5) * 6;
    page.style.transform = `perspective(1200px) rotateX(${y}deg) rotateY(${x}deg)`;
  });

  document.addEventListener('mouseleave', () => {
    page.style.transform = 'perspective(1200px) rotateX(0deg) rotateY(0deg)';
  });
}

// Ensure page reset on unload to avoid extreme transforms
window.addEventListener('beforeunload', () => {
  if (page) {
    page.style.transform = '';
  }
});
