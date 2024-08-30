template = {
    "swagger": "2.0",
    "info": {
        "version": "1.0.0",
        "title": "Bookmarks API",
        "description": "Bookmark API where users can retrieve existing bookmark details",
        "termsOfService": "https://twitter.com/nehemiah_bosire",
        "contact": {
            "name": "Nehemiah",
            "url": "https://twitter.com/nehemiah_bosire",
            "email": "nehem@mail.com"
        }
    },
    "servers": [
        {
            "url": "http://localhost:5000/api/v1",  
            "description": "Development server"
        }
    ],
    "components": {
        "securitySchemes": {
            "Bearer": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
            }
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}
