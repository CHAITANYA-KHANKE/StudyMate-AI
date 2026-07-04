// Global fetch interceptor to support multi-user sessions
(function() {
  const originalFetch = window.fetch;
  window.fetch = function(url, options = {}) {
    let userId = localStorage.getItem('studymate_user_id');
    if (!userId) {
      userId = 'user_' + Math.random().toString(36).substring(2, 15);
      localStorage.setItem('studymate_user_id', userId);
    }
    
    options.headers = options.headers || {};
    if (options.headers instanceof Headers) {
      options.headers.set('X-User-ID', userId);
    } else {
      options.headers['X-User-ID'] = userId;
    }
    return originalFetch(url, options);
  };
})();

document.addEventListener('DOMContentLoaded', () => {
  initLayout();
  initTheme();
  initDynamicComponents();
});

// 1. Shared Layout Initialization
function initLayout() {
  const sidebarContainer = document.getElementById('sidebar-placeholder');
  const navbarContainer = document.getElementById('navbar-placeholder');

  const currentPath = window.location.pathname;

  if (sidebarContainer) {
    sidebarContainer.innerHTML = `
      <div class="sidebar">
        <div class="logo-container">
          <div class="logo-icon">📚</div>
          <div class="logo-text">StudyMate AI</div>
        </div>
        <ul class="nav-links">
          <li class="nav-item ${currentPath.includes('/home/') ? 'active' : ''}">
            <a href="/home">🏠 Home</a>
          </li>
          <li class="nav-item ${currentPath.includes('/setup/') ? 'active' : ''}">
            <a href="/setup">⚙️ Student Setup</a>
          </li>
          <li class="nav-item ${currentPath.includes('/dashboard/') ? 'active' : ''}">
            <a href="/dashboard">📊 Dashboard</a>
          </li>
          <li class="nav-item ${currentPath.includes('/study-plan/') ? 'active' : ''}">
            <a href="/study-plan">📅 Study Plan</a>
          </li>
          <li class="nav-item ${currentPath.includes('/progress/') ? 'active' : ''}">
            <a href="/progress">📈 Progress</a>
          </li>
          <li class="nav-item ${currentPath.includes('/chat/') ? 'active' : ''}">
            <a href="/chat">💬 AI Assistant</a>
          </li>
          <li class="nav-item ${currentPath.includes('/settings/') ? 'active' : ''}">
            <a href="/settings">⚙️ Settings</a>
          </li>
        </ul>
        <div style="margin-top: auto; padding-top: 1rem; border-top: 2px dashed var(--border-color); font-size: 0.8rem; font-weight: 700;">
          v1.0 Capstone Agent
        </div>
      </div>
    `;
  }

  if (navbarContainer) {
    const pageTitles = {
      '/home/': 'Home Welcome',
      '/setup/': 'Study Setup Profile',
      '/dashboard/': 'Student Dashboard',
      '/study-plan/': 'AI Study Timetable',
      '/progress/': 'Progress Tracker',
      '/chat/': 'AI Study Coach Chat',
      '/settings/': 'App Settings'
    };

    let titleText = 'StudyMate AI';
    for (const [route, title] of Object.entries(pageTitles)) {
      if (currentPath.includes(route)) {
        titleText = title;
        break;
      }
    }

    navbarContainer.innerHTML = `
      <div class="top-navbar">
        <h1 class="page-title">${titleText}</h1>
        <div class="user-profile-badge" id="navbar-user-badge">
          👋 Student Profile
        </div>
      </div>
    `;

    // Fetch user profile name dynamically
    fetch('/api/settings')
      .then(res => res.json())
      .then(data => {
        const badge = document.getElementById('navbar-user-badge');
        if (badge && data && data.profile) {
          badge.innerHTML = `🎓 ${data.profile.name}`;
          badge.style.backgroundColor = 'var(--accent-green)';
        } else if (badge) {
          badge.innerHTML = `⚠️ Set up required`;
          badge.style.backgroundColor = 'var(--accent-orange)';
        }
      })
      .catch(() => {});
  }
}

// 2. Theme Initialization
function initTheme() {
  fetch('/api/settings')
    .then(res => res.json())
    .then(data => {
      const theme = data.settings?.theme || 'light';
      document.documentElement.setAttribute('data-theme', theme);
      
      const themeToggle = document.getElementById('theme-select');
      if (themeToggle) {
        themeToggle.value = theme;
      }
    })
    .catch(() => {});
}

// 3. Dynamic Page Components (Pomodoro, Dashboard alerts, print etc.)
function initDynamicComponents() {
  initPomodoroTimer();
}

// Pomodoro Timer Logic
let pomodoroInterval;
let pomodoroTimeLeft = 25 * 60; // 25 minutes
let pomodoroIsRunning = false;
let pomodoroIsBreak = false;

function initPomodoroTimer() {
  const timerDisplay = document.getElementById('timer-display');
  const startBtn = document.getElementById('timer-start');
  const pauseBtn = document.getElementById('timer-pause');
  const resetBtn = document.getElementById('timer-reset');

  if (!timerDisplay) return;

  function updateDisplay() {
    const minutes = Math.floor(pomodoroTimeLeft / 60);
    const seconds = pomodoroTimeLeft % 60;
    timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  }

  if (startBtn) {
    startBtn.addEventListener('click', () => {
      if (pomodoroIsRunning) return;
      pomodoroIsRunning = true;
      pomodoroInterval = setInterval(() => {
        if (pomodoroTimeLeft > 0) {
          pomodoroTimeLeft--;
          updateDisplay();
        } else {
          // Play buzzer sound
          try {
            const context = new (window.AudioContext || window.webkitAudioContext)();
            const osc = context.createOscillator();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(440, context.currentTime);
            osc.connect(context.destination);
            osc.start();
            osc.stop(context.currentTime + 0.5);
          } catch(e) {}

          pomodoroIsBreak = !pomodoroIsBreak;
          pomodoroTimeLeft = (pomodoroIsBreak ? 5 : 25) * 60;
          alert(pomodoroIsBreak ? "Work session done! Take a 5-minute break." : "Break over! Get back to studying!");
          updateDisplay();
        }
      }, 1000);
    });
  }

  if (pauseBtn) {
    pauseBtn.addEventListener('click', () => {
      clearInterval(pomodoroInterval);
      pomodoroIsRunning = false;
    });
  }

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      clearInterval(pomodoroInterval);
      pomodoroIsRunning = false;
      pomodoroIsBreak = false;
      pomodoroTimeLeft = 25 * 60;
      updateDisplay();
    });
  }

  updateDisplay();
}

// Alert Notification system wrapper
function showNotification(message, type = 'info') {
  const container = document.getElementById('notification-container');
  if (!container) return;

  const alertDiv = document.createElement('div');
  alertDiv.className = `notification-banner ${type}`;
  alertDiv.innerHTML = `<span>${message}</span>`;
  container.prepend(alertDiv);

  setTimeout(() => {
    alertDiv.remove();
  }, 5000);
}
