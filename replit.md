# FoodHub - E-Food Delivery Website

## Overview
FoodHub is a full-stack food delivery web application built with Python Flask backend and HTML/CSS/JavaScript frontend. The application allows customers to browse menu items, add items to cart, place orders, and track their order status. It also includes an admin panel for managing menu items and orders.

## Current State
- **Status**: MVP Complete
- **Last Updated**: December 5, 2024

## Tech Stack
- **Backend**: Python Flask with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: PostgreSQL
- **Server**: Gunicorn

## Project Structure
```
├── app.py              # Flask app configuration and database setup
├── main.py             # Application entry point
├── models.py           # Database models (Category, MenuItem, Order, OrderItem)
├── routes.py           # All route handlers
├── seed_data.py        # Database seeding script
├── templates/          # Jinja2 HTML templates
│   ├── base.html       # Base template with navigation and footer
│   ├── index.html      # Homepage with hero, categories, popular items
│   ├── menu.html       # Menu browsing page with category filter
│   ├── cart.html       # Shopping cart page
│   ├── checkout.html   # Checkout form
│   ├── order_confirmation.html  # Order confirmation page
│   ├── track_order.html         # Order tracking page
│   ├── order_history.html       # Order history list
│   └── admin.html      # Admin panel for orders and menu management
├── static/
│   ├── css/style.css   # All styles
│   └── js/main.js      # JavaScript functionality
└── design_guidelines.md # UI/UX design guidelines
```

## Features
1. **Menu Browsing**: Browse food items by category with images, descriptions, and prices
2. **Shopping Cart**: Add/remove items, adjust quantities, view totals
3. **Checkout**: Place orders with delivery details
4. **Order Tracking**: Track order status with visual progress indicator
5. **Admin Panel**: 
   - View and manage orders
   - Add/edit/delete menu items
   - Manage food categories
   - View statistics (pending orders, revenue)

## Database Models
- **Category**: Food categories (Pizza, Burgers, etc.)
- **MenuItem**: Individual food items with name, description, price, image
- **Order**: Customer orders with delivery details and status
- **OrderItem**: Items within an order

## Running the Application
The application runs on port 5000 using Gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

## Seeding the Database
To populate the database with sample data:
```bash
python seed_data.py
```

## Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SESSION_SECRET`: Flask session secret key

## Future Enhancements
- User authentication and registration
- Payment gateway integration (Stripe/PayPal)
- Real-time order tracking with live updates
- Restaurant search and filtering
- User reviews and ratings
- Delivery driver assignment system
