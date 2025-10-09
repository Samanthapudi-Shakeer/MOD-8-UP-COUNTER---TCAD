(function () {
  class SimpleTable {
    constructor(table, options = {}) {
      this.table = table;
      this.tbody = table.querySelector('tbody');
      this.options = Object.assign(
        {
          pageSize: 10,
          paging: true,
          search: true,
          sort: true,
          searchPlaceholder: 'Search…',
          emptyStateElement: null,
        },
        options,
      );
      this.rows = Array.from(this.tbody.querySelectorAll('tr'));
      this.filteredRows = [...this.rows];
      this.page = 1;
      this.sortState = { column: null, direction: 'asc' };
      this.toolbar = null;
      this.searchInput = null;
      this.paginationContainer = null;

      this.init();
    }

    init() {
      this.createToolbar();
      if (this.options.sort) {
        this.setupSortHandlers();
      } else {
        this.disableSortableHeaders();
      }
      this.render();
    }

    createToolbar() {
      const toolbar = document.createElement('div');
      toolbar.className = 'simple-table-toolbar';

      if (this.options.search) {
        const searchWrapper = document.createElement('div');
        searchWrapper.className = 'simple-table-search';
        const searchInput = document.createElement('input');
        searchInput.type = 'search';
        searchInput.placeholder = this.options.searchPlaceholder;
        searchInput.setAttribute('aria-label', 'Search table');
        searchWrapper.appendChild(searchInput);
        toolbar.appendChild(searchWrapper);
        this.searchInput = searchInput;

        searchInput.addEventListener('input', () => {
          const query = searchInput.value.trim().toLowerCase();
          if (!query) {
            this.filteredRows = [...this.rows];
          } else {
            this.filteredRows = this.rows.filter((row) =>
              row.textContent.toLowerCase().includes(query),
            );
          }
          this.page = 1;
          this.render();
        });
      }

      const pagination = document.createElement('div');
      pagination.className = 'simple-table-pagination';
      toolbar.appendChild(pagination);
      this.paginationContainer = pagination;

      this.table.parentElement.insertBefore(toolbar, this.table);
    }

    setupSortHandlers() {
      const headers = Array.from(this.table.querySelectorAll('thead th'));
      headers.forEach((th, index) => {
        const sortable = th.dataset.sortable !== 'false';
        if (!sortable) {
          th.dataset.sortDirection = '';
          return;
        }
        th.addEventListener('click', () => {
          this.sortByColumn(index, th);
        });
      });
    }

    disableSortableHeaders() {
      const headers = Array.from(this.table.querySelectorAll('thead th'));
      headers.forEach((th) => {
        th.dataset.sortable = 'false';
      });
    }

    sortByColumn(index, header) {
      const currentDirection = header.dataset.sortDirection || 'none';
      const nextDirection = currentDirection === 'asc' ? 'desc' : 'asc';

      this.table.querySelectorAll('thead th').forEach((th) => {
        if (th !== header) {
          th.dataset.sortDirection = '';
        }
      });
      header.dataset.sortDirection = nextDirection;

      const comparator = this.buildComparator(index, nextDirection === 'asc');
      this.filteredRows.sort(comparator);
      this.page = 1;
      this.render();
    }

    buildComparator(index, ascending) {
      return (rowA, rowB) => {
        const a = this.getCellValue(rowA, index);
        const b = this.getCellValue(rowB, index);
        const numberA = parseFloat(a);
        const numberB = parseFloat(b);
        let comparison = 0;
        if (!Number.isNaN(numberA) && !Number.isNaN(numberB)) {
          comparison = numberA - numberB;
        } else {
          comparison = a.localeCompare(b, undefined, { sensitivity: 'base' });
        }
        return ascending ? comparison : -comparison;
      };
    }

    getCellValue(row, index) {
      const cell = row.cells[index];
      if (!cell) {
        return '';
      }
      return (cell.textContent || '').trim();
    }

    render() {
      const totalRows = this.filteredRows.length;
      const pagingEnabled = this.options.paging && totalRows > this.options.pageSize;
      const totalPages = pagingEnabled ? Math.max(1, Math.ceil(totalRows / this.options.pageSize)) : 1;
      if (this.page > totalPages) {
        this.page = totalPages;
      }
      const start = pagingEnabled ? (this.page - 1) * this.options.pageSize : 0;
      const end = pagingEnabled ? start + this.options.pageSize : totalRows;
      const fragment = document.createDocumentFragment();
      this.filteredRows.slice(start, end).forEach((row) => {
        fragment.appendChild(row);
      });
      this.tbody.innerHTML = '';
      this.tbody.appendChild(fragment);

      this.updateEmptyState(totalRows === 0);
      this.renderPagination(pagingEnabled ? totalPages : 1, pagingEnabled);
    }

    updateEmptyState(isEmpty) {
      if (!this.options.emptyStateElement) {
        return;
      }
      if (isEmpty) {
        this.table.classList.add('d-none');
        this.options.emptyStateElement.classList.remove('d-none');
      } else {
        this.table.classList.remove('d-none');
        this.options.emptyStateElement.classList.add('d-none');
      }
    }

    renderPagination(totalPages, pagingEnabled) {
      if (!this.paginationContainer) {
        return;
      }
      this.paginationContainer.innerHTML = '';
      if (!pagingEnabled || totalPages <= 1) {
        return;
      }

      const createButton = (label, page, disabled = false) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = label;
        if (disabled) {
          button.disabled = true;
        } else {
          button.addEventListener('click', () => {
            this.page = page;
            this.render();
          });
        }
        return button;
      };

      this.paginationContainer.appendChild(
        createButton('Prev', Math.max(1, this.page - 1), this.page === 1),
      );

      for (let page = 1; page <= totalPages; page += 1) {
        const button = createButton(String(page), page, false);
        if (page === this.page) {
          button.classList.add('is-active');
        }
        this.paginationContainer.appendChild(button);
      }

      this.paginationContainer.appendChild(
        createButton('Next', Math.min(totalPages, this.page + 1), this.page === totalPages),
      );
    }
  }

  function initializeStaticTables() {
    document.querySelectorAll('[data-simple-table]').forEach((table) => {
      if (table.dataset.simpleTableInitialized === 'true') {
        return;
      }
      const options = {};
      if (table.dataset.pageSize) {
        const size = parseInt(table.dataset.pageSize, 10);
        if (!Number.isNaN(size)) {
          options.pageSize = size;
        }
      }
      if (table.dataset.search === 'false') {
        options.search = false;
      }
      if (table.dataset.sort === 'false') {
        options.sort = false;
      }
      if (table.dataset.paging === 'false') {
        options.paging = false;
      }
      if (table.dataset.emptyTarget) {
        const element = document.querySelector(table.dataset.emptyTarget);
        if (element) {
          options.emptyStateElement = element;
        }
      }
      const instance = new SimpleTable(table, options);
      table.dataset.simpleTableInitialized = 'true';
      table.simpleTable = instance;
    });
  }

  window.SimpleTable = SimpleTable;
  document.addEventListener('DOMContentLoaded', initializeStaticTables);
})();
