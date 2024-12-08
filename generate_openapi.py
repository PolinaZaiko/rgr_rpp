import yaml  # Импортируем библиотеку для работы с YAML-файлами
import os  # Импортируем библиотеку для работы с операционной системой

from app import app  # Импортируем экземпляр приложения Flask из модуля app

def generate_openapi_yaml():
    """
    Генерирует спецификацию OpenAPI в формате YAML и сохраняет ее в директорию docs.
    """
    # Проверяем, существует ли директория "docs"; если нет, создаем ее
    if not os.path.exists("docs"):
        os.makedirs("docs")

    # Используем тестовый клиент Flask для выполнения запроса к API
    with app.test_client() as client:
        # Выполняем GET-запрос к маршруту '/apispec_1.json' для получения спецификации OpenAPI
        response = client.get('/apispec_1.json')
        
        # Проверяем, успешен ли запрос (код 200) и является ли ответ JSON
        if response.status_code == 200 and response.is_json:
            openapi_spec = response.json  # Получаем спецификацию OpenAPI из ответа

            # Открываем (или создаем) файл openapi.yaml в директории docs для записи
            with open("docs/openapi.yaml", "w") as file:
                yaml.dump(openapi_spec, file, default_flow_style=False)  # Сохраняем спецификацию в формате YAML
            
            # Выводим сообщение об успешном сохранении спецификации
            print("Спецификация OpenAPI сохранена в docs/openapi.yaml")
            # Выводим содержимое директории docs
            print("Содержимое директории docs:", os.listdir("docs"))
        else:
            # Если запрос не удался, выводим сообщение об ошибке и информацию о статусе
            print("Ошибка: не удалось получить спецификацию OpenAPI.")
            print(response.status_code, response.data)

# Проверяем, выполняется ли этот файл как основной модуль
if __name__ == "__main__":
    generate_openapi_yaml()  # Вызываем функцию для генерации спецификации OpenAPI
