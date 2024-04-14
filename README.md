## Project Integration
```sh

python -m venv venv
linux => source/bin/activate
windows => venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py runserver
```

Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:8000
```

docker build -t panasa_image .
docker run -p 4000:80 panasa_image


