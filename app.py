from flask import Flask, request, jsonify, render_template, redirect, url_for
from flasgger import Swagger

# Создаем экземпляр приложения Flask
app = Flask(__name__)
# Инициализируем Swagger для документирования API
swagger = Swagger(app)

# Словарь для хранения контактов
contacts = {}
# Счетчик для уникальных идентификаторов контактов
contact_id_counter = 1

@app.route('/')
def index():
    """
    Главная страница приложения, отображающая список всех контактов.

    Эта страница предоставляет пользователю возможность просматривать все созданные контакты. 
    Каждый контакт представлен с именем и номером телефона, а также включает ссылки для просмотра 
    подробной информации о контакте и кнопку для его удаления.
    ---
    responses:
      200:
        description: Успешный ответ с отображением главной страницы, содержащей список контактов, если они есть.
    """

    return render_template('index.html', contacts=contacts.values())

@app.route('/contacts/new', methods=['GET', 'POST'])
def create_contact():
    """
    Создание нового контакта.

    Этот маршрут обрабатывает создание нового контакта в системе. Он поддерживает два метода: 
    GET для отображения формы создания контакта и POST для обработки отправленных данных.

    ---
    parameters:
      - name: name
        type: string
        required: true
        description: Имя контакта.
        in: formData
      - name: phone
        type: string
        required: true
        description: Номер телефона.
        in: formData
    responses:
      200:
        description: Форма для создания нового контакта.
      302:
        description: Контакт успешно создан, перенаправление на главную страницу.
    """
    global contact_id_counter # Делаем переменную глобальной для доступа в функции
    if request.method == 'POST':  # Если запрос метода POST (отправка формы)
        data = request.form # Получаем данные из формы
        contact_id = contact_id_counter  # Получаем текущий идентификатор контакта
        # Сохраняем контакт в словаре с уникальным идентификатором
        contacts[contact_id] = {
            "id": contact_id,
            "name": data['name'],
            "phone": data['phone'],
        }
        contact_id_counter += 1 # Увеличиваем счетчик для следующего контакта
        return redirect(url_for('index'))

    return render_template('create_contact.html')

@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    """
    Получение информации о контакте по его идентификатору.

    Этот маршрут позволяет пользователю получить информацию о конкретном контакте, 
    используя его уникальный идентификатор. 
    Если контакт найден, возвращается страница с информацией о нем.
    ---
    parameters:
      - name: id
        type: integer
        required: true
        description: Идентификатор контакта.
        in: path
    responses:
      200:
        description: Информация о контакте.
      404:
        description: Контакт не найден.
    """
    contact = contacts.get(id) # Получаем контакт по идентификатору
    if not contact: # Если контакт не найден
        return jsonify({"message": "Контакт не найден"}), 404 # Возвращаем ошибку 404

    return render_template('contact.html', contact=contact)

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    """
    Удаление контакта по его идентификатору.

    Этот маршрут позволяет удалить контакт из системы по его уникальному идентификатору. 
    Если контакт с указанным идентификатором существует, он будет удален. 
    Если контакт не найден, будет возвращена ошибка 404.

    ---
    parameters:
      - name: id
        type: integer
        required: true
        description: Идентификатор контакта.
        in: path
    responses:
      204:
        description: Успешное удаление контакта.
      404:
        description: Контакт не найден.
    """
    if id in contacts:  # Проверяем, существует ли контакт с данным идентификатором
      del contacts[id] # Удаляем контакт из словаря
      return '', 204 # Возвращаем статус 204 No Content
    else:
      return jsonify({"message": "Контакт не найден"}), 404 # Возвращаем ошибку 404, если контакт не найден

if __name__ == '__main__':
    app.run()
