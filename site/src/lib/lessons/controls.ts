export function slider(id: string, label: string, min: number, max: number, value: number, step = 1): string {
  return `<label class="lesson-control" for="${id}"><span>${label} <output id="${id}-value">${value}</output></span><input id="${id}" type="range" min="${min}" max="${max}" value="${value}" step="${step}"></label>`;
}

export function wireSlider(id: string, onChange: (value: number) => void): void {
  const input = document.getElementById(id) as HTMLInputElement | null;
  const output = document.getElementById(`${id}-value`);
  if (!input || !output) return;
  const update = () => { const value = Number(input.value); output.textContent = String(value); onChange(value); };
  input.addEventListener('input', update); update();
}

export function svgAxes(width: number, height: number, xLabel: string, yLabel: string): string {
  return `<line x1="56" y1="${height - 42}" x2="${width - 20}" y2="${height - 42}" class="axis"/><line x1="56" y1="${height - 42}" x2="56" y2="18" class="axis"/><text x="${width - 70}" y="${height - 12}" class="axis-label">${xLabel}</text><text x="12" y="28" class="axis-label">${yLabel}</text>`;
}
