(function () {
  function ready(handler) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', handler);
    } else {
      handler();
    }
  }

  function initNavigation() {
    const toggle = document.querySelector('.nav-toggle');
    const menu = document.getElementById('navbarNav');
    if (!toggle || !menu) {
      return;
    }
    toggle.addEventListener('click', () => {
      const isOpen = menu.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }

  function initAccordion() {
    const toggles = document.querySelectorAll('[data-accordion-toggle]');
    toggles.forEach((toggle) => {
      toggle.addEventListener('click', () => {
        const targetId = toggle.dataset.accordionToggle;
        const item = toggle.closest('.accordion-item');
        const panel = targetId ? document.getElementById(targetId) : null;
        if (!item || !panel) {
          return;
        }
        const isOpen = item.classList.contains('is-open');
        document.querySelectorAll('.accordion-item').forEach((other) => {
          if (other === item) {
            return;
          }
          other.classList.remove('is-open');
          const otherToggle = other.querySelector('[data-accordion-toggle]');
          if (otherToggle) {
            otherToggle.classList.add('collapsed');
          }
          const otherPanelId = otherToggle ? otherToggle.dataset.accordionToggle : null;
          if (otherPanelId) {
            const otherPanel = document.getElementById(otherPanelId);
            if (otherPanel) {
              otherPanel.classList.remove('is-open');
            }
          }
        });

        if (isOpen) {
          item.classList.remove('is-open');
          panel.classList.remove('is-open');
          toggle.classList.add('collapsed');
        } else {
          item.classList.add('is-open');
          panel.classList.add('is-open');
          toggle.classList.remove('collapsed');
        }
      });
    });
  }

  function createModalController(modalElement, formElement) {
    const closeButtons = modalElement.querySelectorAll('[data-modal-close]');
    const state = { isOpen: false };

    function open() {
      modalElement.classList.add('is-visible');
      modalElement.setAttribute('aria-hidden', 'false');
      document.body.classList.add('modal-open');
      state.isOpen = true;
    }

    function close() {
      modalElement.classList.remove('is-visible');
      modalElement.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('modal-open');
      formElement.reset();
      formElement.dataset.method = '';
      formElement.dataset.rowId = '';
      state.isOpen = false;
    }

    closeButtons.forEach((button) => {
      button.addEventListener('click', close);
    });

    modalElement.addEventListener('click', (event) => {
      if (event.target === modalElement) {
        close();
      }
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && state.isOpen) {
        close();
      }
    });

    return { open, close };
  }

  function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(';') : [];
    for (let i = 0; i < cookies.length; i += 1) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(`${name}=`)) {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
    return null;
  }

  function guessInput(field) {
    const lower = field.name.toLowerCase();
    if (field.type && field.type.toLowerCase().includes('date')) {
      return 'date';
    }
    if (
      ['remarks', 'description', 'content', 'objective', 'measure', 'plan', 'analysis'].some((token) =>
        lower.includes(token),
      )
    ) {
      return 'textarea';
    }
    if (lower.includes('email')) {
      return 'email';
    }
    return 'text';
  }

  function renderForm(formElement, fields, data) {
    formElement.innerHTML = '';
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
      const value = data && Object.prototype.hasOwnProperty.call(data, field.name) ? data[field.name] : '';
      if (value !== null && value !== undefined) {
        input.value = value;
      }
      wrapper.appendChild(input);
      formElement.appendChild(wrapper);
    });
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

  function initPlanSections() {
    const config = window.PlanConfig || null;
    if (!config) {
      return;
    }
    const sectionContent = document.getElementById('section-content');
    const modalElement = document.getElementById('sectionModal');
    const modalForm = document.getElementById('section-form');
    const triggers = Array.from(document.querySelectorAll('.section-trigger'));
    if (!sectionContent || !modalElement || !modalForm || !triggers.length) {
      return;
    }

    const modal = createModalController(modalElement, modalForm);
    const csrfToken = getCookie('csrftoken');
    let currentConfig = null;

    function showModal(title, fields, rowData, method, rowId) {
      document.getElementById('sectionModalLabel').textContent = title;
      renderForm(modalForm, fields, rowData);
      modalForm.dataset.method = method;
      modalForm.dataset.rowId = rowId || '';
      modal.open();
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
      header.className = 'card-header d-flex justify-content-between align-items-center';
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
        th.dataset.sortable = 'true';
        headRow.appendChild(th);
      });
      if (config.canEdit) {
        const th = document.createElement('th');
        th.textContent = 'Actions';
        th.dataset.sortable = 'false';
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

      const emptyState = document.createElement('div');
      emptyState.className = 'empty-state d-none';
      emptyState.textContent = 'No records available.';
      body.appendChild(emptyState);

      card.appendChild(body);
      sectionContent.appendChild(card);

      if (window.SimpleTable) {
        const options = {
          emptyStateElement: emptyState,
          pageSize: 10,
        };
        currentConfig.tableInstance = new window.SimpleTable(table, options);
      }
    }

    async function fetchTable(tableKey, title) {
      sectionContent.innerHTML = '<div class="section-placeholder">Loading…</div>';
      try {
        const response = await fetch(`/projects/${config.projectId}/sections/${tableKey}/`, {
          headers: { 'X-Requested-With': 'XMLHttpRequest' },
        });
        if (!response.ok) {
          throw new Error('Request failed');
        }
        const payload = await response.json();
        renderTable(tableKey, title, payload);
      } catch (error) {
        sectionContent.innerHTML = '<div class="alert alert-danger">Unable to load data.</div>';
      }
    }

    function collectFormData() {
      const formData = {};
      Array.from(modalForm.elements).forEach((element) => {
        if (!element.name) {
          return;
        }
        formData[element.name] = element.value;
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
      const url = rowId ? `${baseUrl}/${rowId}/` : baseUrl;
      try {
        const response = await fetch(url, {
          method: method.toUpperCase(),
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken || '',
          },
          body: JSON.stringify(data),
        });
        if (!response.ok) {
          const payload = await response.json();
          const errorMessage = payload.errors ? JSON.stringify(payload.errors) : 'Failed to save changes.';
          window.alert(errorMessage);
          return;
        }
        modal.close();
        const trigger = document.querySelector(`.section-trigger[data-table-key="${currentConfig.tableKey}"]`);
        const title = trigger ? trigger.dataset.title : currentConfig.title;
        fetchTable(currentConfig.tableKey, title);
      } catch (error) {
        window.alert('Failed to save changes.');
      }
    }

    async function deleteRow(rowId) {
      if (!currentConfig) {
        return;
      }
      if (!window.confirm('Are you sure you want to delete this entry?')) {
        return;
      }
      const url = `/projects/${config.projectId}/sections/${currentConfig.tableKey}/rows/${rowId}/`;
      try {
        const response = await fetch(url, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': csrfToken || '',
          },
        });
        if (!response.ok) {
          window.alert('Failed to delete row.');
          return;
        }
        const trigger = document.querySelector(`.section-trigger[data-table-key="${currentConfig.tableKey}"]`);
        const title = trigger ? trigger.dataset.title : currentConfig.title;
        fetchTable(currentConfig.tableKey, title);
      } catch (error) {
        window.alert('Failed to delete row.');
      }
    }

    sectionContent.addEventListener('click', (event) => {
      const target = event.target;
      if (!(target instanceof HTMLElement)) {
        return;
      }
      if (target.dataset.action === 'refresh' && currentConfig) {
        const trigger = document.querySelector(`.section-trigger[data-table-key="${currentConfig.tableKey}"]`);
        const title = trigger ? trigger.dataset.title : currentConfig.title;
        fetchTable(currentConfig.tableKey, title);
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
        if (!rowId) {
          const index = row ? parseInt(row.dataset.index || '0', 10) : 0;
          data = currentConfig.rows[index] || {};
        }
        showModal(`Edit ${currentConfig.title}`, currentConfig.fields, data, 'put', rowId || '');
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
        triggers.forEach((item) => item.classList.remove('is-active'));
        trigger.classList.add('is-active');
        const tableKey = trigger.dataset.tableKey;
        const title = trigger.dataset.title;
        if (tableKey && title) {
          fetchTable(tableKey, title);
        }
      });
    });
  }

  ready(() => {
    initNavigation();
    initAccordion();
    initPlanSections();
  });
})();
