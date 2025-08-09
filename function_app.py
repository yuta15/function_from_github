import azure.functions as func
import logging

from blueprints.resource_group import BP as resource_group_bp

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
app.register_blueprint(resource_group_bp)