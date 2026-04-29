import { escapeHtml } from '../core/dom.js';

export function renderEventStream(container, steps = [], activeIndex = -1, scenario = {}) {
  const events = (steps || []).map((step, index) => ({
    time: `00:${String(index * 2).padStart(2, '0')}`,
    title: step.title || step.phase || `Step ${index + 1}`,
    detail: step.description || step.detail || '',
  }));
  container.innerHTML = `
    <div class="event-stream-head">
      <span>Live SOC event stream</span>
      <strong>${escapeHtml(scenario.expected_outcome || 'demo')}</strong>
    </div>
    <ol class="event-stream-list">
      ${events.map((event, index) => `
        <li class="event-row ${index <= activeIndex ? 'is-active' : ''} ${index === activeIndex ? 'is-current' : ''}">
          <time>${escapeHtml(event.time)}</time>
          <div><strong>${escapeHtml(event.title)}</strong><p>${escapeHtml(event.detail)}</p></div>
        </li>
      `).join('')}
    </ol>
  `;
}
