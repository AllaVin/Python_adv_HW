
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Boolean, create_engine



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
    price = Column(Numeric (10, 2), nullable=False)
    in_stock = Column(Boolean)
    category_id = Column(Integer, ForeignKey('category.id'))

# --- Модель категории ---
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    products = relationship("Product", backref="category") # --- Settings of relations between tables ---

# --- Создание всех таблиц в БД ---
Base.metadata.create_all(engine)

# --- Создадим категорию и продукт ---
if __name__ == "__main__":
    cat = Category(name="Электроника", description="Все электронные товары")
    prod = Product(name="Фен", price=29.99, in_stock=True, category=cat)

    session.add(cat) # --- В сессию добавляем категорию
    session.add(prod) # --- В сессию добавляем продукт
    session.commit() # --- Коммитим изменения (наши добавления)

    # --- Выведем результат ---
    for product in session.query(Product).all():
        print(f"- {product.name}: {product.price} EUR -> Категория: {product.category.name}")

