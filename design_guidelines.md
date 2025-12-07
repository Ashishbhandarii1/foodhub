# Food Delivery Website - Design Guidelines

## Design Approach
**Reference-Based:** Drawing inspiration from Uber Eats, DoorDash, and Grubhub with focus on appetite appeal and frictionless ordering experience.

**Core Principle:** Food-first visual hierarchy where imagery drives engagement and simple, clear interactions enable quick ordering.

## Typography
- **Headlines:** Bold, modern sans-serif (Poppins 600-700) for restaurant names, section headers
- **Body/Menu Items:** Clean sans-serif (Inter 400-500) for descriptions, prices
- **Prices:** Prominent weight (600) to stand out, larger size than descriptions
- **Hierarchy:** Restaurant names (text-2xl), food item names (text-lg), descriptions (text-sm), prices (text-xl font-semibold)

## Layout System
**Spacing Units:** Tailwind units of 2, 4, 6, 8, 12, 16 for consistent rhythm
- Section padding: py-12 (mobile), py-20 (desktop)
- Card spacing: p-6
- Grid gaps: gap-6 to gap-8
- Component margins: mb-8 to mb-12

## Page-Specific Layouts

### Homepage/Menu Browser
**Hero Section (70vh):**
- Full-width food photography (vibrant prepared meal or restaurant interior)
- Centered search bar with delivery address input
- Semi-transparent overlay with blurred background buttons
- Tagline emphasizing speed/quality ("Fresh Meals Delivered in 30 Minutes")

**Restaurant/Category Grid:**
- 3-column grid (desktop), 2-column (tablet), 1-column (mobile)
- Card design: Large food image (aspect-ratio-4/3), restaurant name, cuisine type, delivery time badge, rating stars
- Hover state: Subtle lift effect (transform: translateY(-4px))

**Menu Items Section:**
- 2-column layout (desktop): Left sidebar with category filters, right content area with food items
- Food item cards: Horizontal layout with image (square, 120x120px), title, description (2 lines max), price, add-to-cart button
- Category headers with sticky positioning

### Shopping Cart
**Side Panel Design (slides from right):**
- Fixed width (400px desktop, full-width mobile)
- Cart items: Compact horizontal cards with thumbnail, name, quantity controls, price
- Sticky checkout summary at bottom with subtotal, delivery fee, total
- Prominent "Checkout" button

### Order Placement Form
**Single-column layout (max-w-2xl centered):**
- Multi-step progression indicator at top
- Step 1: Delivery details (address, phone, delivery instructions)
- Step 2: Payment method selection (cards with radio buttons)
- Step 3: Order review with estimated delivery time
- Each step in clean card with generous padding (p-8)

### Order Tracking/History
**Timeline-based design:**
- Order card with restaurant name, items summary, total, timestamp
- Visual status tracker: Horizontal progress bar with icons (confirmed → preparing → out for delivery → delivered)
- Expandable accordion to view full order details

### Admin Panel
**Dashboard layout:**
- 3-column stats cards at top (pending orders, today's revenue, active deliveries)
- Data table for orders with filters (status dropdown, date range)
- Menu management: Grid of food items with quick edit/delete actions
- Modal for adding/editing menu items with image upload placeholder

## Component Library

### Navigation
- **Top bar:** Logo left, category links center, cart icon with badge and login/signup right
- **Mobile:** Hamburger menu with slide-out drawer
- Sticky on scroll with subtle shadow

### Cards
- **Food Item Card:** Rounded corners (rounded-lg), shadow on hover, image with overlay for "Popular" or "New" badges
- **Restaurant Card:** Larger images, rating and delivery time overlaid on image bottom

### Forms
- Input fields: Full-width, comfortable padding (px-4 py-3), rounded-lg borders
- Labels: Small, uppercase, letter-spaced above inputs
- Buttons: Full-width on mobile, auto-width on desktop
- Validation states: Border color changes, inline error messages below fields

### Buttons
- **Primary CTA:** Large, rounded-full, bold text, prominent positioning
- **Secondary:** Outlined style with transparent background
- **Icon buttons:** Circular for cart actions (add/remove quantity)
- All buttons implement hover/active states

### Data Display
- **Price tags:** Highlighted with larger font, positioned prominently
- **Badges:** Small, rounded-full pills for status, cuisine type, delivery time
- **Rating stars:** Filled/outlined star icons with numerical rating beside

### Modals
- Centered overlay with semi-transparent backdrop
- Max-width constraint (max-w-lg), rounded corners, shadow-2xl
- Close button (X) in top-right corner

## Images

### Required Images:
1. **Hero Background:** High-quality food photography showing vibrant, fresh prepared meals or diverse cuisine spread (1920x1080px minimum)
2. **Menu Item Photos:** Square format (600x600px) for each food item showing plated dish from appetizing angle
3. **Restaurant Logos/Images:** For restaurant cards if multi-restaurant platform
4. **Category Icons:** Simple icon illustrations for cuisine types (pizza, burger, salad, etc.)

### Image Treatment:
- Consistent aspect ratios across similar elements
- Lazy loading for performance
- Alt text for accessibility
- Subtle rounded corners (rounded-lg) on all food images

### Placeholder Strategy:
- Use `https://placehold.co/[dimensions]` with relevant text like "Delicious Pizza" for food items
- Icon placeholders: Use Font Awesome food-related icons (fa-utensils, fa-pizza-slice, fa-burger)

## Icons
**Library:** Font Awesome (CDN)
- Shopping cart: fa-shopping-cart
- Location: fa-map-marker-alt
- Clock/delivery time: fa-clock
- Star ratings: fa-star
- Search: fa-search
- User account: fa-user
- Plus/minus for quantity: fa-plus, fa-minus

## Responsive Behavior
- **Mobile-first:** Single column stacking, full-width cards
- **Tablet (768px+):** 2-column grids, side-by-side layouts emerge
- **Desktop (1024px+):** 3-column grids, maximum content width 1280px
- **Touch-friendly:** Minimum tap targets 44x44px, increased spacing on mobile

## Accessibility
- Semantic HTML throughout (nav, main, article, section)
- ARIA labels for icon-only buttons
- Keyboard navigation support for cart and forms
- Focus indicators on all interactive elements
- Color contrast ratios meeting WCAG AA standards