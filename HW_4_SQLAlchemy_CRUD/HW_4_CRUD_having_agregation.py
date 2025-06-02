from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Boolean, create_engine, func
from colorama import init, Fore, Style

# --- Базовый класс для ORM моделей ---
Base = declarative_base()

# --- Создание движка и базы данных в памяти ---
engine = create_engine('sqlite:///:memory:')

# --- Создание сессии ---
Session = sessionmaker(bind=engine)
session = Session()

# --- Модель продукта ---
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean)
    category_id = Column(Integer, ForeignKey('category.id'))

# --- Модель категории ---
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)

    # --- Settings of relations 1 to many (ONE category to MANY products) ---
    products = relationship("Product", backref="category")

# --- Создание всех таблиц в БД ---
Base.metadata.create_all(bind=engine)

# --- Добавляем категории в таблицу Category ---
session.add_all([
    Category(name="Электроника", description="Гаджеты и устройства"),
    Category(name="Книги", description="Печатные книги и электронные книги"),
    Category(name="Одежда", description="Одежда для мужчин и женщин")
])
session.commit()

# --- Получаем созданные категории из базы ---
electronics = session.query(Category).filter_by(name="Электроника").first()
books = session.query(Category).filter_by(name="Книги").first()
clothing = session.query(Category).filter_by(name="Одежда").first()

# --- Добавляем продукты в таблицу Product ---
session.add_all([
    Product(name="Смартфон", price=299.99, in_stock=True, category=electronics),
    Product(name="Ноутбук", price=499.99, in_stock=True, category=electronics),
    Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=books),
    Product(name="Джинсы", price=40.50, in_stock=True, category=clothing),
    Product(name="Футболка", price=20.00, in_stock=True, category=clothing)
])
session.commit()

if __name__ == "__main__":
    for category in session.query(Category).all():
        print(Fore.YELLOW + f"Категория - {category.name} ({category.description}):" + Style.RESET_ALL )
        print(Fore.GREEN + "    Список продуктов данной категории и их детали:" + Style.RESET_ALL)
        for product in category.products: # Здесь product - это итерируемая переменная
            print(f"        ▶️{product.name} -> {product.price} ({'в наличии' if product.in_stock else 'нет в наличии'})")
print("---------------------------------------------------------------------------------------------------------------")

# --- Находим первый продукт с названием "Смартфон" и обновляем цену ---
smartphone = session.query(Product).filter_by(name="Смартфон").first()
if smartphone:
    smartphone.price = 349.99
    session.commit()
    print(Fore.CYAN + f"\n✅ Цена продукта '{smartphone.name}' успешно обновлена на {smartphone.price}" + Style.RESET_ALL)
else:
    print(Fore.RED + "\n❌ Продукт 'Смартфон' не найден." + Style.RESET_ALL)
print("\n---------------------------------------------------------------------------------------------------------------")

# --- Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории. ---

category_product_counts = (
    session.query(Category.name, func.count(Product.id))
    .join(Product)
    .group_by(Category.id)
    .all()
)

print(Fore.MAGENTA + "\n📊 Количество продуктов в каждой категории:" + Style.RESET_ALL)
for category_name, product_count in category_product_counts:
    print(f"  📁 {category_name}: {product_count} шт.")

print("\n---------------------------------------------------------------------------------------------------------------")

categories_with_multiple_products = (
    session.query(Category.name, func.count(Product.id).label("product_count"))
    .join(Product)
    .group_by(Category.id)
    .having(func.count(Product.id) > 1)
    .all()
)

print(Fore.BLUE + "\n📦 Категории, в которых более одного продукта:" + Style.RESET_ALL)
for category_name, product_count in categories_with_multiple_products:
    print(f"  🧮 {category_name}: {product_count} продукта(ов)")

print("\n---------------------------------------------------------------------------------------------------------------")