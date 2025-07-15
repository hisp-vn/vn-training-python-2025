from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int


p = Person(name="John Doe", age=30)

print(p.model_dump())
print(p.model_dump_json())

print(Person.model_json_schema())
