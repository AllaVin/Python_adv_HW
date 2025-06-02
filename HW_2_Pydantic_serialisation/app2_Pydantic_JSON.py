from pydantic import BaseModel, Field, EmailStr, ValidationError, model_validator
import json
from colorama import Fore, Style, init


# --- Модели данных ---
class Address(BaseModel):
    city: str
    street: str
    house_number: int = Field(..., gt=0)


class User(BaseModel):
    name: str
    age: int = Field(..., gt=0, lt=100)
    email: EmailStr
    is_employed: bool
    address: Address

    # --- Декоратор ---
    @model_validator(mode="after")
    def check_employment_and_age(self) -> 'User':
        if self.is_employed and (self.age < 18 or self.age > 65):
            raise ValueError("Работающий пользователь должен быть от 18 до 65 лет")
        return self

# --- Передаем JOSN строку ---
json_string = """{
    "name" : "Emma",
    "age": 43,
    "email" : "emma@test.com",
    "is_employed" : true,
    "address" : {
        "city" : "Stuttgart",
        "street" : "Blumen Str",
        "house_number" : 123
        }
    }
"""

# --- Десериализация в модель Pydentic ---
data = json.loads(json_string)

try:
    # --- Валидируем словарь через модель ---
    person = User(**data)

    # --- Если валидация прошла, выводим обратно в JSON ---
    print(Fore.GREEN + "Валидация прошла успешно.\n",Fore.BLUE+"JSON формат данных:\n" + Style.RESET_ALL,
          person.model_dump_json(indent=4))  # вернёт строку JSON

except ValidationError as e:
    # --- Если валидация не прошла — выводим ошибку ---
    print(Fore.YELLOW + "Ошибка валидации:" + Style.RESET_ALL, e )

