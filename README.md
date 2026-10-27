# DRFPy1

Django REST Framework asosida yaratilgan vazifalarni boshqarish API loyihasi. Foydalanuvchilar ro'yxatdan o'tishi, tizimga kirishi va o'z vazifalarini yaratishi hamda boshqarishi mumkin. Vazifaga rasm biriktirish va API hujjatlarini Swagger orqali ko'rish imkoniyati mavjud.

## Imkoniyatlar

- Foydalanuvchini ro'yxatdan o'tkazish, tizimga kiritish va chiqarish
- Vazifalarni yaratish, ko'rish, tahrirlash va o'chirish
- Har bir foydalanuvchiga faqat o'z vazifalarini ko'rsatish
- Vazifaga rasm yuklash
- Swagger va ReDoc orqali API hujjatlari

## Texnologiyalar

- Python
- Django
- Django REST Framework
- PostgreSQL
- drf-spectacular (OpenAPI, Swagger, ReDoc)

## O'rnatish va ishga tushirish

Python va PostgreSQL o'rnatilgan bo'lishi kerak.

1. Loyihani klonlang va loyiha papkasiga o'ting:

   ```bash
   git clone https://github.com/Umar-Oken/DRFPy1.git
   cd DRFPy1
   ```

2. Virtual muhit yarating va faollashtiring:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   Windows'da faollashtirish:

   ```powershell
   .venv\Scripts\activate
   ```

3. Kerakli paketlarni o'rnating:

   ```bash
   pip install -r requirements.txt
   ```

4. `.env.example` faylidan `.env` nusxa yarating va PostgreSQL ma'lumotlarini kiriting:

   ```bash
   cp .env.example .env
   ```

   `.env` ichidagi `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` va `DB_PORT` qiymatlarini o'zingizning PostgreSQL sozlamalaringizga moslang. `DJANGO_SECRET_KEY` uchun maxfiy va tasodifiy qiymat ishlating. `.env` faylini ommaga yoki GitHub'ga joylamang.

5. Ma'lumotlar bazasi migratsiyalarini bajaring va serverni ishga tushiring:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

Server odatda `http://127.0.0.1:8000/` manzilida ishlaydi.

## API va hujjatlar

Swagger interfeysi: `http://127.0.0.1:8000/`  
OpenAPI sxemasi: `http://127.0.0.1:8000/api/schema/`  
ReDoc interfeysi: `http://127.0.0.1:8000/api/schema/redoc/`  
Django admin paneli: `http://127.0.0.1:8000/admin/`

| Metod | Endpoint | Tavsif | Kirish |
|---|---|---|---|
| `POST` | `/api/register/` | Yangi foydalanuvchini ro'yxatdan o'tkazish | Ochiq |
| `POST` | `/api/login/` | Tizimga kirish | Ochiq |
| `POST` | `/api/logout/` | Tizimdan chiqish | Kerak |
| `GET` | `/api/tasks/` | Foydalanuvchining vazifalarini olish | Kerak |
| `POST` | `/api/tasks/` | Yangi vazifa yaratish | Kerak |
| `GET` | `/api/tasks/{id}/` | Bitta vazifani ko'rish | Kerak |
| `PUT`, `PATCH` | `/api/tasks/{id}/` | Vazifani to'liq yoki qisman tahrirlash | Kerak |
| `DELETE` | `/api/tasks/{id}/` | Vazifani o'chirish | Kerak |

Ro'yxatdan o'tish uchun JSON namunasi:

```json
{
  "username": "foydalanuvchi",
  "password": "KuchliParol123!",
  "password2": "KuchliParol123!"
}
```

Kirish uchun `username` va `password` yuboriladi. Autentifikatsiya Django session orqali ishlaydi. `Task` yaratish yoki rasm biriktirishda `multipart/form-data` yuboring; vazifa maydonlari `title`, `is_done` va ixtiyoriy `photo`. `owner` va `created_at` server tomonidan belgilanadi.

## Testlar

```bash
python manage.py test
```
