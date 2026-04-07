/* ============================================================
 * BarberPro — App JS
 * ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  // ── Auto-dismiss flash messages ──
  const flashEl = document.querySelectorAll('[data-auto-dismiss]');
  flashEl.forEach(function (el) {
    setTimeout(function () {
      el.style.transition = 'opacity 200ms ease, transform 200ms ease';
      el.style.opacity = '0';
      el.style.transform = 'translateY(-4px)';
      setTimeout(function () { el.remove(); }, 200);
    }, 4000);
  });

  // ── Close modal on Escape key ──
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-backdrop').forEach(function (m) {
        m.classList.add('hidden');
        m.classList.remove('flex');
      });
    }
  });

});

// ── Modal helpers (global for onclick) ──
function openModal(id) {
  var el = document.getElementById(id);
  el.classList.remove('hidden');
  el.classList.add('flex');
}

function closeModal(id) {
  var el = document.getElementById(id);
  el.classList.add('hidden');
  el.classList.remove('flex');
}

// ── Sidebar toggle ──
function toggleSidebar() {
  var sidebar = document.getElementById('sidebar');
  var overlay = document.getElementById('sidebarOverlay');
  if (!sidebar) return;
  sidebar.classList.toggle('-translate-x-full');
  sidebar.classList.toggle('sidebar--open');
  if (overlay) overlay.classList.toggle('hidden');
}
