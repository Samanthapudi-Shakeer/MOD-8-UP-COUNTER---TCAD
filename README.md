# Project Plan Templates Platform

This repository now contains a Django-based web application for managing complex project plan templates across multiple sections (M1–M13). The platform supports role-based access (viewer/editor), dynamic table interactions, and AJAX-driven updates for rapid data entry.

## Features

- **Authentication & Roles** – Uses Django authentication with viewer/editor permissions enforced per project membership.
- **Project Scoping** – Users only see projects they are assigned to through `ProjectMembership` records.
- **Comprehensive Data Model** – Implements all section models (revision history, resources, quality, risk, supplier management, etc.) linked to projects.
- **Dynamic UI** – Bootstrap 5 + DataTables powered interface with accordion navigation, inline modal editing, search, sort, and pagination.
- **AJAX CRUD** – All table operations load lazily via JSON endpoints and support create/update/delete without page reloads.
- **Caching** – Frequently accessed table payloads are cached using Django’s cache framework.

## Getting Started

> **Note:** The execution environment used to author this code does not have external network access, so dependency installation commands could not be executed. Run the following steps locally after cloning the repository.

1. **Create a virtual environment and install requirements**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

3. **Create a superuser and sample data**
   ```bash
   python manage.py createsuperuser
   ```
   Then use the Django admin to create projects and assign memberships. Editor permissions can be toggled via `ProjectMembership.can_edit` or by setting the user profile role to `editor`.

4. **Run the development server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` and log in with your credentials.

## Project Structure

- `config/` – Django project configuration and settings.
- `accounts/` – User profile model and authentication URL wiring.
- `plans/` – Core app containing models for each project plan section, service layer helpers, registry metadata, and views.
- `templates/` – Bootstrap-based templates for authentication and plan management.
- `static/` – Compiled JavaScript and CSS for the interactive dashboard experience.

## Development Notes

- The section registry (`plans/section_registry.py`) centralises metadata for tables, enabling generic CRUD endpoints and pre-populated deliverable lists.
- AJAX views live in `plans/views.py` and expose JSON payloads consumed by `static/js/app.js` for inline editing and DataTable rendering.
- File and image uploads are represented via `FileField` definitions. Configure media storage if uploads are required in production.
- Because package installation could not be verified in the authoring environment, ensure Django 4.2+ is installed locally before running management commands.

## Next Steps

- Add automated tests once migrations are generated.
- Configure deployment settings (ALLOWED_HOSTS, database, static/media storage) for production use.
- Extend `static/js/app.js` with richer inline editing (e.g., field type detection from server metadata).

Enjoy building and tracking your project plans!
