let replayTimer = null;

export function stopReplay() {
  if (replayTimer) clearInterval(replayTimer);
  replayTimer = null;
}

export function startReplay({ steps, speed = 1, onFrame, onDone }) {
  stopReplay();
  const safeSteps = Array.isArray(steps) && steps.length ? steps : [{ title: 'Flow captured', description: 'Replay event' }];
  let index = -1;
  const frameMs = Math.max(260, 760 / Number(speed || 1));

  onFrame?.(index, safeSteps);
  replayTimer = setInterval(() => {
    index += 1;
    onFrame?.(index, safeSteps);
    if (index >= safeSteps.length - 1) {
      stopReplay();
      onDone?.(index, safeSteps);
    }
  }, frameMs);
}

export function scrubReplay({ steps, index, onFrame }) {
  stopReplay();
  const safeSteps = Array.isArray(steps) ? steps : [];
  const bounded = Math.max(-1, Math.min(Number(index), safeSteps.length - 1));
  onFrame?.(bounded, safeSteps);
}
