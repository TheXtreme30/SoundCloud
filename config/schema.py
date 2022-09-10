from drf_spectacular.extensions import OpenApiAuthenticationExtension


class MyAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'rest_framework_simplejwt.authentication.JWTAuthentication'  # full import path OR class ref
    name = 'Authentication'  # name used in the schema

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
        }
