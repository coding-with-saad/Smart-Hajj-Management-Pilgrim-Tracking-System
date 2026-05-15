# Research: Frontend & UI Design Patterns

## Decision: Sidebar-Driven Admin Dashboard
**Rationale**: Sidebar navigation is the industry standard for management systems. It allows for high scalability as more modules (Pilgrims, Packages, Payments) are added without cluttering the horizontal space.
**Alternatives Considered**: Top-bar only (rejected as it becomes crowded quickly), Hamburger-only (rejected for desktop as it adds extra clicks).

## Decision: Bootstrap 5 for Responsiveness
**Rationale**: Bootstrap 5 provides a robust grid system and pre-built components (cards, tables, modals) that significantly speed up development while ensuring mobile compatibility.
**Alternatives Considered**: Tailwind CSS (rejected to keep the project beginner-friendly for the user).

## Decision: Chart.js for Analytics
**Rationale**: Lightweight and easy to integrate with Flask. Data can be passed as JSON and rendered in canvas elements.
**Alternatives Considered**: D3.js (too complex), Google Charts (requires external library loading/internet).

## Decision: Client-Side Search Filtering
**Rationale**: For the expected scale of an undergraduate project (hundreds of pilgrims), client-side filtering using simple JavaScript is faster and provides a better UX than full page reloads.
**Alternatives Considered**: Server-side search (overkill for small datasets but a good fallback for scale).

## Best Practices Found
1. **Sticky Sidebar**: Use `position: sticky` or a fixed wrapper to keep navigation accessible.
2. **Chart Responsiveness**: Set `responsive: true` and `maintainAspectRatio: false` in Chart.js options.
3. **Form Validation**: Utilize Bootstrap's `:invalid` and `:valid` pseudo-classes for immediate feedback.
4. **Print CSS**: Use `@media print` to hide navigation and buttons when printing QR cards.
