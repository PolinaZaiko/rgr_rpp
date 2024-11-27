import yaml
import os

from app import app


def generate_openapi_yaml():
    docs_dir = "docs"
    os.makedirs(docs_dir, exist_ok=True)

    with app.test_client() as client:
        response = client.get('/apispec_1.json')
        
        if response.status_code == 200 and response.is_json:
            openapi_spec = response.json
            
            openapi_file_path = os.path.join(docs_dir, "openapi.yaml")

            with open(openapi_file_path, "w") as file:
                yaml.dump(openapi_spec, file, default_flow_style=False)
            
            print("Спецификация OpenAPI сохранена в docs/openapi.yaml")
        else:
            print("Ошибка: не удалось получить спецификацию OpenAPI.")
            print(response.status_code, response.data)


if __name__ == "__main__":
    generate_openapi_yaml()
