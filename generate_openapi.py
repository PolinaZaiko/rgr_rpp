import yaml
import os

from app import app


def generate_openapi_yaml():
    if not os.path.exists("docs"):
        os.makedirs("docs")

    with app.test_client() as client:
        response = client.get('/apispec_1.json')
        
        if response.status_code == 200 and response.is_json:
            openapi_spec = response.json

            with open("docs/openapi.yaml", "w") as file:
                yaml.dump(openapi_spec, file, default_flow_style=False)
            
            print("Спецификация OpenAPI сохранена в docs/openapi.yaml")
            print("Содержимое директории docs:", os.listdir("docs"))
        else:
            print("Ошибка: не удалось получить спецификацию OpenAPI.")
            print(response.status_code, response.data)


if __name__ == "__main__":
    generate_openapi_yaml()
    print("Содержимое директории docs после генерации:", os.listdir("docs"))
