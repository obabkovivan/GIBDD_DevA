from flask import Flask, request, jsonify
from model import db, Vehicle
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

swagger = Swagger(app)

with app.app_context():
    db.create_all()  # Создание таблиц

# Эндпоинт для создания транспортного средства (POST /api/vehicles)
@app.route('/api/vehicles', methods=['POST'])
def create_vehicle():
    """Создание транспортного средства
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            model:
              type: string
            owner:
              type: string
            registration_number:
              type: string
            is_active:
              type: boolean
    responses:
      201:
        description: Транспортное средство создано
      400:
        description: Ошибка в данных
    """
    data = request.json
    new_vehicle = Vehicle(model=data['model'], owner=data['owner'], registration_number=data['registration_number'], is_active=data['is_active'])
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify({'id': new_vehicle.id}), 201

# Эндпоинт для чтения конкретного транспортного средства (GET /api/vehicles/<id>)
@app.route('/api/vehicles/<int:id>', methods=['GET'])
def get_vehicle(id):
    """Чтение конкретного транспортного средства
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Информация о транспортном средстве
      404:
        description: Транспортное средство не найдено
    """
    vehicle = Vehicle.query.get(id)
    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404
    return jsonify({'id': vehicle.id, 'model': vehicle.model, 'owner': vehicle.owner, 'registration_number': vehicle.registration_number, 'is_active': vehicle.is_active})

# Эндпоинт для чтения всех транспортных средств (GET /api/vehicles)
@app.route('/api/vehicles', methods=['GET'])
def get_all_vehicles():
    """Чтение всех транспортных средств
    ---
    responses:
      200:
        description: Список всех транспортных средств
    """
    vehicles = Vehicle.query.all()
    return jsonify([{'id': vehicle.id, 'model': vehicle.model, 'owner': vehicle.owner, 'registration_number': vehicle.registration_number, 'is_active': vehicle.is_active} for vehicle in vehicles])

# Эндпоинт для обновления транспортного средства (PUT /api/vehicles/<id>)
@app.route('/api/vehicles/<int:id>', methods=['PUT'])
def update_vehicle(id):
    """Обновление транспортного средства
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            model:
              type: string
            owner:
              type: string
            registration_number:
              type: string
            is_active:
              type: boolean
    responses:
      200:
        description: Транспортное средство обновлено
      404:
        description: Транспортное средство не найдено
    """
    vehicle = Vehicle.query.get(id)
    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404

    data = request.json
    vehicle.model = data['model']
    vehicle.owner = data['owner']
    vehicle.registration_number = data['registration_number']
    vehicle.is_active = data['is_active']
    db.session.commit()
    return jsonify({'message': 'Vehicle updated'})

# Эндпоинт для удаления транспортного средства (DELETE /api/vehicles/<id>)

@app.route('/api/vehicles/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    """Удаление транспортного средства
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Транспортное средство удалено
      404:
        description: Транспортное средство не найдено
    """
    vehicle = Vehicle.query.get(id)
    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404

    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({'message': 'Vehicle deleted'})

if __name__ == '__main__':
    app.run(debug=True)
