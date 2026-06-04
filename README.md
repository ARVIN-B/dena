# Dena Task Agent

یک Agent گفت‌وگومحور فارسی برای کار با داده‌های تسک و کاربر، ساخته‌شده با `LangGraph` و `AutoGen` و مجهز به:

- Planner برای تبدیل درخواست به plan اجرایی
- Tool execution برای خواندن و تغییر داده‌ها
- Memory کوتاه‌مدت برای follow-up
- Clarification برای سؤال‌های مبهم
- API برای تست و مصرف بیرونی

## ویژگی‌ها

- پاسخ‌گویی فارسی به درخواست‌های آماری، جستجو، تحلیل و عملیات
- پشتیبانی از `conversation_id` برای حفظ context بین پیام‌ها
- resolve کردن نام کاربر به `assignee_id` برای ساخت تسک
- خواندن و نوشتن امن CSV با `utf-8-sig` برای جلوگیری از خراب شدن متن فارسی
- endpointهای سبک برای تست سریع

## ساختار پروژه

- `app/agent/` منطق اصلی agent، state، memory، planner و response
- `app/api/` API با FastAPI
- `app/tools/` ابزارهای داخلی برای query و action
- `app/services/` لایه سرویس برای کار با داده‌ها
- `app/repositories/` لایه دسترسی به CSV
- `data/` فایل‌های `tasks.csv` و `users.csv`

## پیش‌نیازها

- Python 3.13 یا سازگار
- فایل‌های داده در `data/tasks.csv` و `data/users.csv`
- کلید OpenRouter در فایل `.env`

نمونه `.env`:

```env
OPENROUTER_API_KEY=your_key_here
MODEL_NAME=openrouter/owl-alpha
```

## نصب

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## اجرای API

```bash
.venv\Scripts\python.exe -m uvicorn app.api.server:app --reload
```

بعد از اجرا:

- `GET /health`
- `POST /chat`

## اجرای CLI تستی

```bash
.venv\Scripts\python.exe -m app.test_agent
```

## نمونه درخواست API

```http
POST /chat
Content-Type: application/json

{
  "message": "چند تسک باز داریم؟"
}
```

نمونه پاسخ:

```json
{
  "conversation_id": "uuid",
  "answer": "تعداد تسک‌های باز 27 مورد است.",
  "plan": [
    {
      "tool": "count",
      "params": {
        "source": "tasks",
        "status": "Open"
      }
    }
  ]
}
```

## رفتار حافظه

- حافظه‌ی کوتاه‌مدت در `SessionStore` نگه‌داری می‌شود.
- اگر `conversation_id` را در پیام بعدی بفرستی، agent context قبلی را می‌بیند.
- برای همین، سؤال‌های follow-up مثل `حالا چندتاش حیاتی هستن؟` می‌توانند به پیام قبلی ارجاع دهند.

## ابزارها

- `count`
- `search`
- `aggregate`
- `create_task`
- `update_task`
- `delete_task`
- `create_user`
- `update_user`
- `delete_user`

## نکات مهم طراحی

- پاسخ نهایی تا حد ممکن deterministic تولید می‌شود تا hallucination کم شود.
- برای سؤال‌های شمارشی رایج، planner از heuristic استفاده می‌کند تا وابستگی به مدل کمتر شود.
- `create_task` می‌تواند `assignee_name` بگیرد و آن را به `assignee_id` resolve کند.
- اگر planner در plan مرحله‌ی `search` قبل از `create_task` بدهد، executor می‌تواند از نتیجه‌ی search شناسه را پر کند.

## تست سریع

1. سرویس را بالا بیاور.
2. یک درخواست به `POST /chat` بفرست.
3. یک پیام follow-up با همان `conversation_id` بفرست.
4. یک سناریوی ایجاد تسک با نام کاربر را امتحان کن.

## محدودیت فعلی

- حافظه فعلاً in-memory است و با restart سرویس پاک می‌شود.
- برای نسخه production بهتر است `SessionStore` به Redis یا دیتابیس منتقل شود.
- داده‌ها فعلاً از CSV خوانده و نوشته می‌شوند، نه دیتابیس واقعی.

## مسیرهای مهم

- API: [app/api/server.py](app/api/server.py)
- Routes: [app/api/routes.py](app/api/routes.py)
- Runtime: [app/agent/runtime.py](app/agent/runtime.py)
- Planner: [app/agent/nodes/planner_node.py](app/agent/nodes/planner_node.py)
- Response: [app/agent/nodes/response_node.py](app/agent/nodes/response_node.py)
- Session store: [app/agent/session_store.py](app/agent/session_store.py)

## پیشنهاد برای قدم بعدی

- اضافه کردن persistence برای حافظه با Redis
- اضافه کردن تست‌های خودکار برای `/chat`
- اضافه کردن Dockerfile و راه‌اندازی containerized

