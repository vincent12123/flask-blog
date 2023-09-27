## Struktur Program 
```
flasklogin1
├── app
│   ├── models.py
│   ├── routes.py
│   ├── static
│   │   ├── assets
│   │   ├── css
│   │   └── img
│   ├── templates
│   │   ├── base.html
│   │   ├── basedashboard.html
│   │   ├── home.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── main.html
│   │   ├── register.html
│   │   ├── routes.py
│   │   └── sidebar.html
│   ├── __init__.py
├── database.py
├── instance
│   └── site.db
└── run.py

```
## Buat Database dengan nama `database.py` 
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# inisiasi ekstensi
db = SQLAlchemy()

# inisiasi aplikasi Flask
app = Flask(__name__)

# konfigurasi basis data SQLite, relatif terhadap folder instansi aplikasi
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

# inisiasi aplikasi dengan ekstensi
db.init_app(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        """
        Mengatur kata sandi pengguna setelah di-hash.

        Args:
            password (str): Kata sandi teks biasa untuk di-hash.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Memeriksa apakah kata sandi yang diberikan cocok dengan kata sandi yang di-hash.

        Args:
            password (str): Kata sandi teks biasa untuk diperiksa.

        Returns:
            bool: True jika kata sandi benar, False jika tidak.
        """
        return check_password_hash(self.password, password)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))

# Membuat tabel berdasarkan model-model yang telah didefinisikan
with app.app_context():
    db.create_all()

```
Pustaka yang diimpor dari Flask adalah bagian dari ekosistem Flask yang menyediakan fungsionalitas tambahan untuk mempermudah pengembangan aplikasi web.

1. `flask_sqlalchemy`: Ini adalah ekstensi Flask yang menyediakan integrasi dengan SQLAlchemy, yang merupakan toolkit Python untuk bekerja dengan basis data relasional. Dengan `flask_sqlalchemy`, Anda dapat dengan mudah berinteraksi dengan basis data melalui objek Python, dan melakukan operasi seperti membuat, membaca, memperbarui, dan menghapus data. Ini menyediakan cara yang lebih tinggi tingkat dan mudah digunakan daripada bekerja langsung dengan SQL.

2. `werkzeug.security.generate_password_hash` dan `werkzeug.security.check_password_hash`: Werkzeug adalah pustaka utilitas untuk web di Python. Fungsi `generate_password_hash` digunakan untuk mengamankan kata sandi dengan menghasilkan hash yang tidak dapat diubah (untuk penyimpanan di basis data). Sebaliknya, `check_password_hash` digunakan untuk memeriksa apakah kata sandi yang diberikan cocok dengan hash yang disimpan di basis data.

3. `flask_login.UserMixin`: `UserMixin` adalah kelas yang disediakan oleh ekstensi Flask-Login untuk menyediakan implementasi default dari metode-metode yang diperlukan untuk mengelola otentikasi pengguna. Dengan mewarisi `UserMixin`, kelas `User` akan memiliki metode-metode seperti `is_authenticated()`, `is_active()`, `is_anonymous()`, dan `get_id()`, yang diperlukan oleh Flask-Login untuk bekerja.

Pustaka-pustaka ini digunakan untuk mengelola pengguna dan menyimpan data mereka dalam basis data, serta untuk mengamankan kata sandi pengguna sebelum menyimpannya.

## Buat `/__init__.py` di dalam folder app 
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes
```


1. `from flask import Flask`: Ini mengimpor kelas `Flask` dari pustaka Flask, yang digunakan untuk membuat instance dari aplikasi Flask.

2. `from flask_sqlalchemy import SQLAlchemy`: Ini mengimpor ekstensi `SQLAlchemy` dari pustaka Flask-SQLAlchemy. `SQLAlchemy` adalah toolkit Python yang kuat untuk berinteraksi dengan basis data relasional. Di sini, Anda membuat instance `db` yang akan digunakan untuk berinteraksi dengan basis data.

3. `from flask_login import LoginManager`: Ini mengimpor ekstensi `LoginManager` dari pustaka Flask-Login. `LoginManager` digunakan untuk mengelola otentikasi pengguna di aplikasi Flask.

4. `app = Flask(__name__)`: Ini membuat instance dari aplikasi Flask. Parameter `__name__` adalah nama modul saat ini.

5. `app.config['SECRET_KEY'] = 'mysecret'`: Ini mengatur kunci rahasia yang digunakan oleh Flask untuk sesi dan fitur keamanan lainnya. Dalam hal ini, kunci rahasia diatur sebagai `'mysecret'`. Kunci rahasia sebenarnya harus dijaga dengan ketat dan tidak boleh didefinisikan dengan cara ini di aplikasi produksi.

6. `app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'`: Ini mengatur URI (Uniform Resource Identifier) untuk basis data yang akan digunakan. Dalam hal ini, aplikasi menggunakan SQLite dengan nama file basis data `'site.db'`.

7. `db = SQLAlchemy(app)`: Ini inisialisasi ekstensi SQLAlchemy dengan memberikan instance aplikasi Flask (`app`) sebagai argumen.

8. `login_manager = LoginManager(app)`: Inisialisasi `LoginManager` dengan memberikan instance aplikasi Flask (`app`) sebagai argumen.

9. `login_manager.login_view = 'login'`: Ini menentukan rute yang akan digunakan untuk otentikasi pengguna. Dalam hal ini, rute yang digunakan adalah `'login'`.

10. `from app import routes`: Ini mengimpor modul `routes` dari paket `app`. Modul `routes` kemungkinan berisi definisi rute dan fungsi yang terkait.

Kode ini adalah konfigurasi basis data, manajemen otentikasi pengguna, dan pengaturan kunci rahasia untuk sesi.

## Buat `models.py` dalam folder `app`
```python
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
```


1. `from app import db`: Ini mengimpor instance `db` dari modul `app`. `db` adalah instance dari SQLAlchemy yang telah diinisialisasi sebelumnya.

2. `from werkzeug.security import generate_password_hash, check_password_hash`: Ini mengimpor fungsi-fungsi dari pustaka `werkzeug.security` yang digunakan untuk mengamankan kata sandi (hashing dan pemeriksaan).

3. `from flask_login import UserMixin`: Ini mengimpor kelas `UserMixin` dari pustaka Flask-Login. Kelas ini menyediakan implementasi default dari metode-metode yang diperlukan untuk mengelola otentikasi pengguna.

4. `class User(db.Model, UserMixin):`: Ini adalah definisi dari kelas `User`. Kelas ini adalah model yang akan digunakan untuk merepresentasikan pengguna dalam basis data.

   - `id = db.Column(db.Integer, primary_key=True)`: Ini mendefinisikan kolom `id` sebagai kolom integer dengan sifat unik dan sebagai kunci utama (primary key).

   - `username = db.Column(db.String(20), unique=True, nullable=False)`: Ini mendefinisikan kolom `username` sebagai kolom string dengan panjang maksimum 20 karakter, harus unik, dan tidak boleh kosong (nullable=False).

   - `password = db.Column(db.String(120), nullable=False)`: Ini mendefinisikan kolom `password` sebagai kolom string dengan panjang maksimum 120 karakter dan tidak boleh kosong.

   - `def set_password(self, password)`: Ini adalah metode untuk mengatur kata sandi pengguna setelah di-hash. Metode ini menggunakan fungsi `generate_password_hash` dari `werkzeug.security`.

   - `def check_password(self, password)`: Ini adalah metode untuk memeriksa apakah kata sandi yang diberikan cocok dengan kata sandi yang di-hash. Metode ini menggunakan fungsi `check_password_hash` dari `werkzeug.security`.

5. `class Message(db.Model):`: Ini adalah definisi dari kelas `Message`. Kelas ini adalah model yang akan digunakan untuk merepresentasikan pesan dalam basis data.

   - `id = db.Column(db.Integer, primary_key=True)`: Ini mendefinisikan kolom `id` sebagai kolom integer dengan sifat unik dan sebagai kunci utama (primary key).

   - `message = db.Column(db.String(255))`: Ini mendefinisikan kolom `message` sebagai kolom string dengan panjang maksimum 255 karakter.

Kode ini mendefinisikan dua model (`User` dan `Message`) yang akan digunakan untuk berinteraksi dengan basis data. Model `User` digunakan untuk merepresentasikan pengguna, sementara model `Message` digunakan untuk merepresentasikan pesan.

## Buat `routes.py` dalam folder `app`
```python
from flask import render_template, url_for, flash, redirect, request
from app import app, db, login_manager
from app.models import User, Message
from flask_login import login_user, current_user, logout_user, login_required

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")

def main():
    return render_template('main.html')

@app.route("/dashboard")
@login_required
def dashboard():
    messages = Message.query.all()
    return render_template('dashboard.html', messages=messages)

@app.route("/login", methods=['GET', 'POST'])
def login():
    messages = Message.query.all()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', messages=messages)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/create', methods=['POST'])
def create():
    new_message = request.form.get('new_message')
    if new_message:
        message = Message(message=new_message)
        db.session.add(message)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for('dashboard'))

```

1. **`from flask import render_template, url_for, flash, redirect, request`**: Ini mengimpor beberapa fungsi dan kelas dari Flask yang diperlukan untuk membuat dan mengelola aplikasi web.

2. **`from app import app, db, login_manager`** dan **`from app.models import User, Message`**: Ini mengimpor instance aplikasi (`app`), instance SQLAlchemy (`db`), dan `login_manager` dari modul `app`. Selain itu, juga mengimpor kelas-kelas `User` dan `Message` dari modul `app.models`.

3. **`from flask_login import login_user, current_user, logout_user, login_required`**: Ini mengimpor beberapa fungsi dan dekorator dari Flask-Login untuk mengelola otentikasi pengguna.

4. **`@login_manager.user_loader`**: Ini adalah dekorator yang menentukan fungsi untuk memuat pengguna berdasarkan ID. Fungsi ini mengambil `user_id` dan mengembalikan objek pengguna atau `None`.

5. **`@app.route("/")`** dan **`def main():`**: Ini adalah rute utama aplikasi. Fungsi `main` akan merender template `main.html`.

6. **`@app.route("/dashboard")`** dan **`@login_required`**: Ini adalah rute untuk dashboard. Fungsi `dashboard` memerlukan pengguna untuk masuk terlebih dahulu sebelum dapat mengaksesnya. Di dalamnya, mengambil semua pesan dari basis data dan meneruskannya ke template `dashboard.html`.

7. **`@app.route("/login", methods=['GET', 'POST'])`** dan **`def login():`**: Ini adalah rute untuk halaman login. Fungsi `login` memproses formulir login dan melakukan otentikasi. Jika pengguna telah masuk atau formulir telah dikirim, pengguna akan diarahkan ke dashboard.

8. **`@app.route("/logout")`** dan **`def logout():`**: Ini adalah rute untuk logout. Fungsi `logout` melakukan logout pengguna dan mengarahkan mereka kembali ke halaman login.

9. **`@app.route("/register", methods=['GET', 'POST'])`** dan **`def register():`**: Ini adalah rute untuk halaman pendaftaran. Fungsi `register` memproses formulir pendaftaran dan membuat pengguna baru di basis data.

10. **`@app.route('/create', methods=['POST'])`** dan **`def create():`**: Ini adalah rute untuk membuat pesan baru. Fungsi `create` mengambil pesan baru dari formulir dan menyimpannya di basis data.

11. **`@app.route('/delete/<int:id>', methods=['POST'])`** dan **`def delete(id):`**: Ini adalah rute untuk menghapus pesan. Fungsi `delete` mengambil ID pesan yang akan dihapus, menemukan pesan tersebut di basis data, dan menghapusnya.

Kode ini mencakup fungsionalitas dasar untuk aplikasi web, termasuk otentikasi pengguna, manajemen pesan, dan navigasi halaman. 
Pastikan untuk membuat template HTML yang sesuai (seperti `main.html`, `dashboard.html`, `login.html`, `register.html`) untuk mengintegrasikan dengan kode ini.

## buat `run.py` di luar folder `app`
```python
from app import app

if __name__ == '__main__':
    app.run(debug=True)
```

1. **`from app import app`**: Ini mengimpor instance aplikasi Flask (`app`) dari modul `app`. Ini adalah aplikasi Flask yang telah Anda definisikan sebelumnya.

2. **`if __name__ == '__main__':`**: Ini adalah kondisi untuk memeriksa apakah skrip ini dijalankan secara langsung atau diimpor sebagai modul. Jika ini adalah skrip utama yang dijalankan secara langsung, maka blok berikutnya akan dieksekusi.

3. **`app.run(debug=True)`**: Ini adalah perintah untuk menjalankan aplikasi Flask. Fungsi `run` digunakan untuk memulai server Flask. Dalam hal ini, `debug=True` menyebabkan aplikasi berjalan dalam mode debug, yang akan memudahkan dalam pengembangan dengan memberikan informasi tambahan tentang kesalahan dan memuat ulang otomatis setelah perubahan kode.

