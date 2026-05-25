from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli_anahtar_123'
socketio = SocketIO(app)

# 50x50 boyutunda, başlangıçta beyaz olan bir ızgara (grid) oluşturuyoruz
GRID_SIZE = 50
grid = [["#ffffff" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('get_grid')
def handle_get_grid():
    # Oyuncu ilk bağlandığında mevcut tabloyu gönder
    emit('load_grid', grid)

@socketio.on('place_block')
def handle_place_block(data):
    x = data['x']
    y = data['y']
    color = data['color']
    
    # Koordinatlar geçerliyse grid'i güncelle ve tüm oyunculara yayınla
    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
        grid[y][x] = color
        emit('update_block', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)