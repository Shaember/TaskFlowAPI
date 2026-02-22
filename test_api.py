import requests
import time

BASE_URL = 'http://127.0.0.1:8000/api/tasks/'

def test_api():
    print("Testing CRUD operations on TaskFlowAPI...")
    
    # 1. GET empty list
    response = requests.get(BASE_URL)
    print("GET list init:", response.status_code, response.json())

    # 2. POST (Создание задачи без due_date)
    payload_1 = {
        "title": "Сдать экзамен по Django",
        "description": "Реализовать CRUD API для задач",
        "status": "in_progress",
        "priority": "high"
    }
    response = requests.post(BASE_URL, json=payload_1)
    print("POST create task:", response.status_code, response.json())
    task_id = response.json().get('id')

    # 3. POST (Создать ещё одну задачу, для списка)
    payload_2 = {
        "title": "Помыть посуду",
        "priority": "low"
    }
    requests.post(BASE_URL, json=payload_2)

    # 4. GET list again to verify order (by '-created_at')
    response = requests.get(BASE_URL)
    print("GET list populated:", response.status_code)
    for t in response.json():
        print(f" - [{t['id']}] {t['title']} (status: {t['status']}, priority: {t['priority']})")

    # 5. GET detail
    response = requests.get(f"{BASE_URL}{task_id}/")
    print("GET detail:", response.status_code, response.json()['title'])

    # 6. PATCH (Обновление статуса с помощью PATCH)
    patch_payload = {
        "status": "completed"
    }
    response = requests.patch(f"{BASE_URL}{task_id}/", json=patch_payload)
    print("PATCH update status:", response.status_code, response.json()['status'])

    # 7. DELETE (Удаление задачи)
    response = requests.delete(f"{BASE_URL}{task_id}/")
    print("DELETE task:", response.status_code)

    # 8. GET list to verify deletion
    response = requests.get(BASE_URL)
    print("GET list after deletion:", response.status_code, [t['title'] for t in response.json()])

if __name__ == '__main__':
    test_api()
