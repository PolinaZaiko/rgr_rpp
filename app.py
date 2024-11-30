from flask import Flask, request, jsonify, render_template, redirect, url_for
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

contacts = {}
contact_id_counter = 1

@app.route('/')
def index():
    """Главная страница с списком контактов."""
    return render_template('index.html', contacts=contacts.values())

@app.route('/contacts/new', methods=['GET', 'POST'])
def create_contact():
    """
    Создание нового контакта!
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
      302:
        description: Контакт успешно создан и перенаправление на главную страницу.
    """
    global contact_id_counter
    if request.method == 'POST':
        data = request.form
        contact_id = contact_id_counter
        contacts[contact_id] = {
            "id": contact_id,
            "name": data['name'],
            "phone": data['phone'],
        }
        contact_id_counter += 1
        return redirect(url_for('index'))

    return render_template('create_contact.html')

@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    """
    Получение информации о контакте по его идентификатору.
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
    contact = contacts.get(id)
    if not contact:
        return jsonify({"message": "Contact not found"}), 404

    return render_template('contact.html', contact=contact)

@app.route('/contacts/<int:id>', methods=['POST'])
def delete_contact(id):
    """
    Удаление контакта по его идентификатору.
    ---
    parameters:
      - name: id
        type: integer
        required: true
        description: Идентификатор контакта.
        in: path
    responses:
      302:
        description: Успешное удаление контакта и перенаправление на главную страницу.
      404:
        description: Контакт не найден.
    """
    if id not in contacts:
        return jsonify({"message": "Contact not found"}), 404

    del contacts[id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)
