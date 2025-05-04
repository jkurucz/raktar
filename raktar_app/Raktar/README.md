# Raktárkezelő REST API

Ez a projekt egy Flask + APIFlask alapú RESTful backend, amely egy raktározási és szállítási rendszer alapfolyamatait modellezi.  
A cél a legfontosabb szerepkörök és adategységek (rendelés, szállítás, raktárkészlet, panaszkezelés stb.) lefedése – nem pedig egy teljes vállalati rendszer implementálása.

---

## Futtatás

1. Projekt klónozása:
   ```
   git clone http://github.com/jkurucz/raktar/
   ```

2. Virtuális környezet létrehozása:
   ```
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   ```

3. Függőségek telepítése:
   ```
   pip install -r requirements.txt
   ```

4. Adatbázis inicializálása:
   ```bash
   flask db init
   ```
   
   ```bash   
   flask db migrate
   ```
   
   ```bash
   flask db upgrade
   ```
   
   ```bash
   python init_db.py
   ```

5. Alkalmazás indítása:
   ```
   python run.py
   ```

- API elérhetősége: `http://localhost:5000/api`  
- Swagger dokumentáció: `http://localhost:5000/docs`

---

## Technológiák

- Python 3.11+
- Flask & APIFlask
- SQLAlchemy ORM
- SQLite (lokális fejlesztéshez)
- JWT token alapú autentikáció
- Role-based access control
- Swagger UI automatikus dokumentáció

---

## Szerepkörök

| Szerepkör            | Jogosultság |
|----------------------|-------------|
| `Administrator`      | Teljes adminisztráció |
| `LogisticsManager`   | Termékek, készlet, szállítás kezelése |
| `Courier`            | Saját szállítás frissítése |
| `User`               | Saját rendelések, panasz beküldése |
| `Chef`               | (jelenleg nem használjuk) |

---

## Tesztfelhasználók (ini_db.py alapján)

| Email                  | Jelszó        | Szerepkör           |
|------------------------|---------------|----------------------|
| `admin@example.com`    | `admin123`    | Administrator        |
| `courier@example.com`  | `courier123`  | Courier              |
| `user@example.com`     | `user123`     | User                 |
| `logistics@example.com`| `manager123`  | LogisticsManager     |

A `init_db.py` betöltése után ezek automatikusan létrejönnek.