# MtaaBiz Kenya

**"Find trusted businesses near you."**

A full-stack Django local business directory, launched first in Kisumu,
Kenya, architected to expand to all 47 counties. This is a real, working
application — not a mockup. Every flow described below has been tested
through Django's test client (23 automated tests, all passing) and
verified by hand.

## What's built

**Public site**
- Homepage with hero search, popular categories, featured/popular
  businesses, browse-by-location, "how it works", owner CTA
- Search & browse (`/business/explore/`) with filters (category, location,
  premium) and sorting (relevant, highest rated, newest, featured), paginated
- Category pages (`/category/<slug>/`) and location pages (`/location/<slug>/`)
- Business profile pages with logo/cover, services & prices, photo gallery,
  opening hours, socials, Call/WhatsApp/Directions/Website buttons with
  click tracking, reviews, and similar businesses
- SEO: sitemap.xml, robots.txt, per-page meta descriptions, clean slugs

**Accounts**
- Register, log in, log out, edit profile
- A user automatically becomes a "business_owner" the moment they register
  their first business

**Business owners**
- Register a business (goes to "pending" until an admin approves it)
- Dashboard (`/dashboard/`): overview with real click/view analytics,
  edit business, manage services, manage photos, view & respond to
  reviews, subscription plan status, advertising requests

**Reviews & favorites**
- 1–5 star reviews, one per user per business (editing replaces the old
  one), business owners can respond publicly
- Save/unsave businesses, "My Favorites" page

**Premium & advertising**
- Free / Premium (KSh 500/mo) / Featured (KSh 1,500/mo) plans, seeded via
  migration
- Upgrade requests are **manual** — an admin verifies payment (e.g. an
  M-Pesa transaction code the owner enters) and activates the plan from
  the admin. No fake/simulated payment gateway is wired in, per the brief.
- Advertisement requests (title, banner image, destination URL, placement,
  date range) go to "pending" until an admin approves them

**Admin**
- Every model manageable from `/admin/`, with list filters, search,
  inline editing, and bulk actions (approve/reject businesses, activate
  subscriptions, approve ads, moderate reviews)

## What's intentionally NOT built yet

- Automatic/online payment processing (M-Pesa STK push, card payments) —
  the brief explicitly asked for a manual/mock system for now
- A cascading category→county→town→area picker in the registration form
  (currently plain dropdowns); JS-driven filtering is a natural next step
- Multi-business-per-owner dashboard switching (the dashboard currently
  manages the owner's first registered business)
- Live deployment to Render (the configuration is present and passes
  Django's `--deploy` security checklist, but hasn't been deployed to a
  live instance)

## Setup (Windows / Command Prompt)

```text
cd path\to\mtaabiz
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Setup (macOS / Linux)

```bash
cd path/to/mtaabiz
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

`migrate` automatically seeds: Kisumu County → Kisumu Town → 6 areas, all
35 business categories from the brief, and the 3 subscription plans.

## Try the whole flow

1. Open **http://127.0.0.1:8000/** — homepage.
2. Click **Register** and create an account.
3. Click **List Your Business**, fill in the form, submit — you'll land on
   your (empty, pending) dashboard.
4. Log into **http://127.0.0.1:8000/admin/** as your superuser, open
   **Businesses**, select your new business, and either set **Approval
   status** to "Approved" or use the bulk action, plus tick **Is featured**.
5. Back on the site, your business now appears on the homepage, in
   **Explore**, its category page, and its location page.
6. Log in as a *different* user (or register a second account) and leave
   a review and save it to favorites — the rating updates immediately.
7. As the business owner, visit **Dashboard → Reviews** and reply to it.
8. Visit **Dashboard → Subscription** and request an upgrade — this
   creates a "pending" subscription you can activate from the admin's
   Subscriptions page (bulk action "Activate selected subscriptions").

## Running the tests

```text
python manage.py test
```

23 tests covering: registration, login, business creation & approval
workflow, slug generation & uniqueness, search & filtering, review
creation/uniqueness/rating calculation, favorites, and dashboard
access/permissions.

## Database

SQLite by default. Set `DATABASE_URL` in the environment to switch to
PostgreSQL — no code changes needed:

```text
DATABASE_URL=postgres://USER:PASSWORD@HOST:5432/DBNAME
```

## Deploying (Render or similar)

1. Set environment variables: `SECRET_KEY` (generate a real one — see
   `.env.example`), `DEBUG=False`, `ALLOWED_HOSTS`, `DATABASE_URL`,
   `CSRF_TRUSTED_ORIGINS`.
2. Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
3. Start command (already in `Procfile`): `gunicorn config.wsgi:application`
4. Verified: `python manage.py check --deploy` returns **zero issues**
   when `DEBUG=False` with a real `SECRET_KEY` set.

## Project structure

```text
mtaabiz/
├── config/            settings, root urls, wsgi/asgi, sitemaps wiring
├── core/               home, about, robots.txt, sitemaps.py
├── accounts/           custom User model, auth views/forms
├── categories/          Category model + browse views
├── locations/           County/Town/Area models + browse views
├── businesses/          Business/Service/Photo/Analytics + registration, search, detail
├── dashboard/            business owner dashboard (aggregates other apps)
├── reviews/              Review model + add/respond views
├── favorites/            Favorite model + toggle/list views
├── subscriptions/        Plan/Subscription models + pricing/upgrade views
├── advertisements/       Advertisement model + request view
├── templates/             base.html, home.html, and per-app templates
├── static/css/style.css  design system
├── requirements.txt, Procfile, .env.example, .gitignore
```
"# mtaa" 
