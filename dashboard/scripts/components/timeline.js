import { escapeHtml } from '../core/dom.js';

export function renderTimeline(container, steps = [], activeIndex = steps.length - 1) {
  container.innerHTML = steps.map((step, index) => `
    <div class="timeline-step ${index <= activeIndex ? 'is-active' : ''}">
      <div class="timeline-dot">${index + 1}</div>
      <div class="timeline-card">
        <strong>${escapeHtml(step.title || step.phase || `Step ${index + 1}`)}</strong>
        <p>${escapeHtml(step.description || step.detail || '')}</p>
      </div>
    </div>
  `).join('');
}

export function replayTimeline(container, steps = []) {
  let index = 0;
  renderTimeline(container, steps, -1);
  const timer = setInterval(() => {
    renderTimeline(container, steps, index);
    index += 1;
    if (index >= steps.length) clearInterval(timer);
  }, 650);
}
