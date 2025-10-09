(function () {
  const config = window.PlanConfig || null;
  if (!config) {
    return;
  }
  const triggers = document.querySelectorAll('.section-trigger');
  const sectionContent = document.getElementById('section-content');
  const modalElement = document.getElementById('sectionModal');
  const modalForm = document.getElementById('section-form');
  let modalInstance = null;
  let currentConfig = null;

  if (!sectionContent || !triggers.length) {
    return;
  }

  const csrfToken = getCookie('csrftoken');

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i += 1) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function guessInput(field) {
    const lower = field.name.toLowerCase();
    if (field.type.includes('Date')) {
      return 'date';
    }
    if (['remarks', 'description', 'content', 'objective', 'measure', 'plan', 'analysis'].some((token) => lower.includes(token))) {
      return 'textarea';
    }
    if (lower.includes('email')) {
      return 'email';
    }
    return 'text';
  }

  function renderForm(fields, data) {
    modalForm.innerHTML = '';
    fields.forEach((field) => {
      const wrapper = document.createElement('div');
      wrapper.className = 'mb-3';
      const label = document.createElement('label');
      label.className = 'form-label';
      label.setAttribute('for', `id_${field.name}`);
      label.textContent = field.label;
      wrapper.appendChild(label);
      const inputType = guessInput(field);
      let input;
      if (inputType === 'textarea') {
        input = document.createElement('textarea');
        input.className = 'form-control';
        input.rows = 3;
      } else {
        input = document.createElement('input');
        input.type = inputType;
        input.className = 'form-control';
      }
      input.name = field.name;
      input.id = `id_${field.name}`;
      const value = data && data[field.name] !== null && data[field.name] !== undefined ? data[field.name] : '';
      if (inputType === 'date' && value) {
        input.value = value;
      } else if (inputType === 'textarea') {
        input.value = value;
      } else {
        input.value = value;
      }
      wrapper.appendChild(input);
      modalForm.appendChild(wrapper);
    });
  }

  function closeModal() {
    if (modalInstance) {
      modalInstance.hide();
    }
  }

  function showModal(title, fields, rowData, method, rowId) {
    if (!modalInstance) {
      modalInstance = new bootstrap.Modal(modalElement);
    }
    document.getElementById('sectionModalLabel').textContent = title;
    renderForm(fields, rowData);
    modalForm.dataset.method = method;
    modalForm.dataset.rowId = rowId || '';
    modalInstance.show();
  }

  function buildActionButtons(canEdit, singleton) {
    const container = document.createElement('div');
    container.className = 'table-actions';
    const refreshButton = document.createElement('button');
    refreshButton.type = 'button';
    refreshButton.className = 'btn btn-sm btn-outline-secondary';
    refreshButton.dataset.action = 'refresh';
    refreshButton.textContent = 'Refresh';
    container.appendChild(refreshButton);
    if (canEdit) {
      const addButton = document.createElement('button');
      addButton.type = 'button';
      addButton.className = 'btn btn-sm btn-primary';
      addButton.dataset.action = 'add';
      addButton.textContent = singleton ? 'Edit' : 'Add Row';
      container.appendChild(addButton);
    }
    return container;
  }

  function renderTable(tableKey, title, payload) {
    currentConfig = {
      tableKey,
      fields: payload.fields,
      singleton: payload.singleton,
      rows: payload.rows,
      title,
    };
    sectionContent.innerHTML = '';
    const card = document.createElement('div');
    card.className = 'card section-card';
    const header = document.createElement('div');
    header.className = 'card-header';
    const heading = document.createElement('h2');
    heading.className = 'h5 mb-0';
    heading.textContent = title;
    header.appendChild(heading);
    header.appendChild(buildActionButtons(config.canEdit, payload.singleton));
    card.appendChild(header);
    const body = document.createElement('div');
    body.className = 'card-body';

    const table = document.createElement('table');
    table.className = 'table table-striped w-100';
    table.id = `table-${tableKey}`;

    const thead = document.createElement('thead');
    const headRow = document.createElement('tr');
    payload.fields.forEach((field) => {
      const th = document.createElement('th');
      th.textContent = field.label;
      headRow.appendChild(th);
    });
    if (config.canEdit) {
      const th = document.createElement('th');
      th.textContent = 'Actions';
      headRow.appendChild(th);
    }
    thead.appendChild(headRow);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    payload.rows.forEach((row, index) => {
      const tr = document.createElement('tr');
      tr.dataset.rowId = row.id ? String(row.id) : '';
      tr.dataset.index = String(index);
      payload.fields.forEach((field) => {
        const td = document.createElement('td');
        const value = row[field.name];
        td.textContent = value !== null && value !== undefined && value !== '' ? value : '—';
        tr.appendChild(td);
      });
      if (config.canEdit) {
        const td = document.createElement('td');
        td.className = 'text-end';
        if (row.id) {
          const editBtn = document.createElement('button');
          editBtn.type = 'button';
          editBtn.className = 'btn btn-sm btn-outline-primary me-2';
          editBtn.dataset.action = 'edit-row';
          editBtn.textContent = 'Edit';
          td.appendChild(editBtn);
          const deleteBtn = document.createElement('button');
          deleteBtn.type = 'button';
          deleteBtn.className = 'btn btn-sm btn-outline-danger';
          deleteBtn.dataset.action = 'delete-row';
          deleteBtn.textContent = 'Delete';
          td.appendChild(deleteBtn);
        } else if (payload.singleton) {
          const addBtn = document.createElement('button');
          addBtn.type = 'button';
          addBtn.className = 'btn btn-sm btn-outline-primary';
          addBtn.dataset.action = 'add';
          addBtn.textContent = 'Create';
          td.appendChild(addBtn);
        }
        tr.appendChild(td);
      }
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    body.appendChild(table);
    card.appendChild(body);
    sectionContent.appendChild(card);

    $(table).DataTable({
      destroy: true,
      paging: payload.rows.length > 10,
      searching: true,
      lengthChange: false,
    });
  }

  async function fetchTable(tableKey, title) {
    sectionContent.innerHTML = '<div class="section-placeholder">Loading…</div>';
    const response = await fetch(`/projects/${config.projectId}/sections/${tableKey}/`, {
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
    });
    if (!response.ok) {
      sectionContent.innerHTML = '<div class="alert alert-danger">Unable to load data.</div>';
      return;
    }
    const payload = await response.json();
    renderTable(tableKey, title, payload);
  }

  function collectFormData() {
    const formData = {};
    Array.from(modalForm.elements).forEach((el) => {
      if (!el.name) {
        return;
      }
      formData[el.name] = el.value;
    });
    return formData;
  }

  async function submitForm(event) {
    event.preventDefault();
    if (!currentConfig) {
      return;
    }
    const data = collectFormData();
    const method = modalForm.dataset.method || 'post';
    const rowId = modalForm.dataset.rowId;
    const baseUrl = `/projects/${config.projectId}/sections/${currentConfig.tableKey}/rows`;
    const url = rowId ? `${baseUrl}/${rowId}/` : `${baseUrl}`;
    const response = await fetch(url, {
      method: method.toUpperCase(),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      const payload = await response.json();
      alert(payload.errors ? JSON.stringify(payload.errors) : 'Failed to save changes.');
      return;
    }
    closeModal();
    fetchTable(currentConfig.tableKey, document.querySelector(`.section-trigger[data-table-key="${currentConfig.tableKey}"]`).dataset.title);
  }

  async function deleteRow(rowId) {
    if (!currentConfig) {
      return;
    }
    if (!confirm('Are you sure you want to delete this entry?')) {
      return;
    }
    const url = `/projects/${config.projectId}/sections/${currentConfig.tableKey}/rows/${rowId}/`;
    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': csrfToken,
      },
    });
    if (!response.ok) {
      alert('Failed to delete row.');
      return;
    }
    fetchTable(currentConfig.tableKey, document.querySelector(`.section-trigger[data-table-key="${currentConfig.tableKey}"]`).dataset.title);
  }

  sectionContent.addEventListener('click', (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) {
      return;
    }
    if (target.dataset.action === 'refresh' && currentConfig) {
      const trigger = document.querySelector(`.section-trigger[data-table-key="${currentConfig.tableKey}"]`);
      fetchTable(currentConfig.tableKey, trigger.dataset.title);
    }
    if (target.dataset.action === 'add' && currentConfig) {
      let method = 'post';
      let rowId = '';
      let rowData = {};
      if (currentConfig.singleton && currentConfig.rows) {
        const existing = currentConfig.rows.find((row) => row.id);
        if (existing) {
          method = 'put';
          rowId = String(existing.id);
          rowData = existing;
        } else if (currentConfig.rows.length) {
          rowData = currentConfig.rows[0];
        }
      }
      const modalTitle = `${currentConfig.singleton ? 'Edit' : 'Add'} ${currentConfig.title}`;
      showModal(modalTitle, currentConfig.fields, rowData, method, rowId);
    }
    if (target.dataset.action === 'edit-row' && currentConfig) {
      const row = target.closest('tr');
      const rowId = row ? row.dataset.rowId : null;
      let data = {};
      if (rowId) {
        const existing = currentConfig.rows.find((item) => item.id && String(item.id) === rowId);
        if (existing) {
          data = existing;
        }
      }
      showModal('Edit Row', currentConfig.fields, data, 'put', rowId || '');
    }
    if (target.dataset.action === 'delete-row' && currentConfig) {
      const row = target.closest('tr');
      const rowId = row ? row.dataset.rowId : null;
      if (rowId) {
        deleteRow(rowId);
      }
    }
  });

  modalForm.addEventListener('submit', submitForm);

  triggers.forEach((trigger) => {
    trigger.addEventListener('click', () => {
      const tableKey = trigger.dataset.tableKey;
      const title = trigger.dataset.title;
      fetchTable(tableKey, title);
    });
  });

  // Auto-load the first section
  if (triggers.length) {
    triggers[0].click();
  }
})();
