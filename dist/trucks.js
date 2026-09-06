(() => {
  'use strict';
  const form = document.getElementById('truck-calculator');
  if (!form) return;
  const get = id => document.getElementById(id);
  const number = new Intl.NumberFormat('en-ZA', {maximumFractionDigits: 0});
  const money = value => 'R ' + number.format(value);
  function update() {
    const names = ['trucks', 'distance', 'consumption', 'price', 'saving'];
    const inputs = names.map(name => form.elements.namedItem(name));
    get('calc-saving-label').textContent = inputs[4].value + '%';
    if (inputs.some(input => !input.value.trim() || !input.validity.valid || !Number.isFinite(Number(input.value)))) {
      ['calc-annual', 'calc-monthly', 'calc-litres'].forEach(id => { get(id).textContent = '—'; });
      get('calc-note').textContent = 'Complete the figures with valid numbers to calculate an estimate.';
      return;
    }
    const [trucks, distance, consumption, price, saving] = inputs.map(input => Number(input.value));
    const litres = trucks * distance * consumption / 100 * saving / 100;
    get('calc-annual').textContent = money(litres * price * 12);
    get('calc-monthly').textContent = money(litres * price);
    get('calc-litres').textContent = number.format(litres) + ' L';
    get('calc-note').textContent = 'Planning estimate before tuning costs.';
  }
  form.addEventListener('input', update);
  form.addEventListener('submit', event => event.preventDefault());
  update();
})();
