from app import app, db
from models import Category, MenuItem

def seed_database():
    with app.app_context():
        existing_categories = Category.query.first()
        if existing_categories:
            print("Database already seeded!")
            return

        categories = [
            Category(name="Pizza", icon="fa-pizza-slice"),
            Category(name="Burgers", icon="fa-burger"),
            Category(name="Chicken", icon="fa-drumstick-bite"),
            Category(name="Salads", icon="fa-leaf"),
            Category(name="Seafood", icon="fa-fish"),
            Category(name="Desserts", icon="fa-ice-cream"),
            Category(name="Drinks", icon="fa-coffee"),
            Category(name="Asian", icon="fa-bowl-rice"),
        ]
        
        for cat in categories:
            db.session.add(cat)
        db.session.commit()
        
        pizza = Category.query.filter_by(name="Pizza").first()
        burgers = Category.query.filter_by(name="Burgers").first()
        chicken = Category.query.filter_by(name="Chicken").first()
        salads = Category.query.filter_by(name="Salads").first()
        seafood = Category.query.filter_by(name="Seafood").first()
        desserts = Category.query.filter_by(name="Desserts").first()
        drinks = Category.query.filter_by(name="Drinks").first()
        asian = Category.query.filter_by(name="Asian").first()
        
        menu_items = [
            MenuItem(
                name="Margherita Pizza",
                description="Classic Italian pizza with fresh mozzarella, tomatoes, and basil on a crispy thin crust",
                price=14.99,
                category_id=pizza.id,
                image_url="https://images.unsplash.com/photo-1604382355076-af4b0eb60143?w=600",
                is_popular=True
            ),
            MenuItem(
                name="Pepperoni Pizza",
                description="Loaded with spicy pepperoni, melted mozzarella cheese, and our signature tomato sauce",
                price=16.99,
                category_id=pizza.id,
                image_url="https://images.unsplash.com/photo-1628840042765-356cda07504e?w=600",
                is_popular=True
            ),
            MenuItem(
                name="BBQ Chicken Pizza",
                description="Grilled chicken, red onions, cilantro, and smoky BBQ sauce with mozzarella",
                price=17.99,
                category_id=pizza.id,
                image_url="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600"
            ),
            MenuItem(
                name="Classic Cheeseburger",
                description="Juicy beef patty with cheddar cheese, lettuce, tomato, and special sauce",
                price=12.99,
                category_id=burgers.id,
                image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600",
                is_popular=True
            ),
            MenuItem(
                name="Bacon Double Burger",
                description="Two beef patties, crispy bacon, American cheese, pickles, and mayo",
                price=15.99,
                category_id=burgers.id,
                image_url="https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=600"
            ),
            MenuItem(
                name="Veggie Burger",
                description="Plant-based patty with avocado, sprouts, tomato, and chipotle aioli",
                price=13.99,
                category_id=burgers.id,
                image_url="https://images.unsplash.com/photo-1525059696034-4967a8e1dca2?w=600"
            ),
            MenuItem(
                name="Crispy Fried Chicken",
                description="Golden fried chicken pieces served with honey mustard dipping sauce",
                price=11.99,
                category_id=chicken.id,
                image_url="https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=600",
                is_popular=True
            ),
            MenuItem(
                name="Grilled Chicken Breast",
                description="Herb-marinated chicken breast with roasted vegetables and lemon sauce",
                price=14.99,
                category_id=chicken.id,
                image_url="https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=600"
            ),
            MenuItem(
                name="Buffalo Wings",
                description="Spicy buffalo wings served with blue cheese dip and celery sticks",
                price=10.99,
                category_id=chicken.id,
                image_url="https://images.unsplash.com/photo-1608039755401-742074f0548d?w=600"
            ),
            MenuItem(
                name="Caesar Salad",
                description="Crisp romaine lettuce, parmesan, croutons, and creamy Caesar dressing",
                price=9.99,
                category_id=salads.id,
                image_url="https://images.unsplash.com/photo-1546793665-c74683f339c1?w=600"
            ),
            MenuItem(
                name="Greek Salad",
                description="Fresh cucumbers, tomatoes, olives, feta cheese with olive oil dressing",
                price=10.99,
                category_id=salads.id,
                image_url="https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600"
            ),
            MenuItem(
                name="Grilled Salmon",
                description="Fresh Atlantic salmon fillet with asparagus and lemon butter sauce",
                price=22.99,
                category_id=seafood.id,
                image_url="https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=600",
                is_popular=True
            ),
            MenuItem(
                name="Fish & Chips",
                description="Beer-battered cod with crispy fries and tartar sauce",
                price=15.99,
                category_id=seafood.id,
                image_url="https://images.unsplash.com/photo-1579208030886-b1a5ed1a7888?w=600"
            ),
            MenuItem(
                name="Shrimp Scampi",
                description="Garlic butter shrimp served over linguine pasta",
                price=18.99,
                category_id=seafood.id,
                image_url="https://images.unsplash.com/photo-1633504581786-316c8002b1b9?w=600"
            ),
            MenuItem(
                name="Chocolate Lava Cake",
                description="Warm chocolate cake with a molten center, served with vanilla ice cream",
                price=8.99,
                category_id=desserts.id,
                image_url="https://images.unsplash.com/photo-1624353365286-3f8d62daad51?w=600",
                is_popular=True
            ),
            MenuItem(
                name="New York Cheesecake",
                description="Creamy classic cheesecake with strawberry topping",
                price=7.99,
                category_id=desserts.id,
                image_url="https://images.unsplash.com/photo-1508737804141-4c3b688e2546?w=600"
            ),
            MenuItem(
                name="Tiramisu",
                description="Italian coffee-flavored dessert with mascarpone and cocoa",
                price=8.99,
                category_id=desserts.id,
                image_url="https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=600"
            ),
            MenuItem(
                name="Fresh Lemonade",
                description="Freshly squeezed lemons with a hint of mint",
                price=4.99,
                category_id=drinks.id,
                image_url="https://images.unsplash.com/photo-1621263764928-df1444c5e859?w=600"
            ),
            MenuItem(
                name="Iced Coffee",
                description="Cold brewed coffee served over ice with your choice of milk",
                price=5.99,
                category_id=drinks.id,
                image_url="https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?w=600"
            ),
            MenuItem(
                name="Mango Smoothie",
                description="Fresh mango blended with yogurt and honey",
                price=6.99,
                category_id=drinks.id,
                image_url="https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?w=600"
            ),
            MenuItem(
                name="Pad Thai",
                description="Stir-fried rice noodles with shrimp, peanuts, egg, and tamarind sauce",
                price=14.99,
                category_id=asian.id,
                image_url="https://images.unsplash.com/photo-1559314809-0d155014e29e?w=600",
                is_popular=True
            ),
            MenuItem(
                name="Chicken Teriyaki Bowl",
                description="Grilled chicken with teriyaki glaze over steamed rice and vegetables",
                price=13.99,
                category_id=asian.id,
                image_url="https://images.unsplash.com/photo-1609183480237-ccb439e7e27e?w=600"
            ),
            MenuItem(
                name="Vegetable Fried Rice",
                description="Wok-fried rice with mixed vegetables, egg, and soy sauce",
                price=11.99,
                category_id=asian.id,
                image_url="https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=600"
            ),
        ]
        
        for item in menu_items:
            db.session.add(item)
        db.session.commit()
        
        print("Database seeded successfully!")
        print(f"Added {len(categories)} categories and {len(menu_items)} menu items.")

if __name__ == "__main__":
    seed_database()
