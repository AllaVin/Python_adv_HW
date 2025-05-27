# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Этот код выводит и данные в формате JSON, и данные в формате Pydentic
# Тут есть валидация и данных формата JSON в соответствии с условиями, описанными в декораторе,
# и данных в формате Pydentic
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from pydantic import BaseModel, Field, EmailStr, ValidationError, model_validator
import json

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
    
    @model_validator(mode="after")
    def check_employment_and_age(self) -> 'User':
        if self.is_employed and (self.age < 18 or self.age > 65):
            raise ValueError("Работающий пользователь должен быть от 18 до 65 лет")
        return self

# --- Словарь (Python-объект) ---
data_dict = {
    "name": "Emma",
    "age": 12,
    "email": "emma@test.com",
    "is_employed": False,
    "address": {
        "city": "Stuttgart",
        "street": "Blumen Str",
        "house_number": 123
    }
}
# --- Валидация словаря ---
try:
    user = User.model_validate(data_dict, strict=True)
    print("\n✅ Валидация Pydentic формата успешна:", user)
except ValidationError as e:
    print("❌ Валидация Pydentic формата успешна Validation error:", e)

json_string = """{
    "name" : "Emma",
    "age": 45,
    "email" : "emma@test.com",
    "is_employed" : true,
    "address" : {
        "city" : "Stuttgart",
        "street" : "Blumen Str",
        "house_number" : 123
        }
    }
"""

# --- Валидация JSON-строки ---
try:
    user = User.model_validate_json(json_string, strict=True)
    print("✅ Валидация строки JSON формата:", user)
except ValidationError as e:
    print("❌ Валидация строки JSON формата не прошла. Validation error:", e)


# --- Сериализация обратно ---
user_dict = user.model_dump()
print("\n🔁 Словарь:", user_dict)

user_json = user.model_dump_json(indent=4)
print("\n🔁 JSON:\n", user_json)