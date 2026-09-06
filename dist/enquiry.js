(() => {
  'use strict';
  const form = document.getElementById('bloem-enquiry');
  if (!form) return;
  const status = document.getElementById('enquiry-status');
  const destination = {
    whatsapp: ['27', '73', '972', '7708'].join(''),
    email: ['boostech', 'bfn', '@', 'gmail', '.', 'com'].join('')
  };
  const fields = ['name', 'year', 'make', 'model', 'engine', 'transmission', 'location'];
  fields.forEach(name => form.elements.namedItem(name).addEventListener('input', event => event.target.setCustomValidity('')));
  const article = new URLSearchParams(location.search).get('article');
  if (article) form.elements.namedItem('notes').value = 'I read your article: ' + article.slice(0, 250);

  form.addEventListener('submit', event => {
    event.preventDefault();
    for (const name of fields) {
      const input = form.elements.namedItem(name);
      input.setCustomValidity(input.value.trim() ? '' : 'Please complete this field.');
    }
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const value = name => String(data.get(name) || '').trim();
    const lines = [
      'Hi Pieter, I would like advice and a quote from Boostech Bloemfontein.',
      '', 'Name: ' + value('name'), 'Service: ' + value('service'),
      'Year: ' + value('year'), 'Make: ' + value('make'), 'Model: ' + value('model'),
      'Engine: ' + value('engine'), 'Transmission: ' + value('transmission'),
      'Location: ' + value('location')
    ];
    if (value('notes')) lines.push('', 'Additional details: ' + value('notes'));
    const message = lines.join('\n');
    const channel = event.submitter?.value || 'whatsapp';
    if (channel === 'email') {
      const subject = 'Boostech Bloemfontein enquiry: ' + value('make') + ' ' + value('model');
      status.textContent = 'Your email app will open a draft. Review it and send it there.';
      window.location.assign('mailto:' + destination.email + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(message));
    } else {
      status.textContent = 'WhatsApp will open your enquiry. Review it and send it there.';
      window.location.assign('https://wa.me/' + destination.whatsapp + '?text=' + encodeURIComponent(message));
    }
  });
})();
