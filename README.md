### Описание
Сервис видеоаналитики и отслеживания простоя техники на строительных площадках.
Приложение требует для запуска gpu.

- Запустите `docker-compose up`
- Проставьте policy в [minio s3](http://localhost:9000)
- Приложение будет доступно по ссылке [на страницу](http://localhost:8080)
- Добавьте переменные окружени frontend/.env
```
VUE_APP_BUCKET_UPLOAD_NAME=http://localhost:9000/videos/
VUE_APP_BUCKET_DOWNLOAD_NAME=http://localhost:9000/processed-videos/
VUE_APP_API_URL=http://localhost:8000
```

#### Распознаваемые классы техники:
- Грузовик-Самосвал
- Кран
- Трактор
- Экскаватор

### Пример работы
![example](crane.gif)

Для каждого найденного объекта также рассчитываются показатели простоя на стройплощадке.

