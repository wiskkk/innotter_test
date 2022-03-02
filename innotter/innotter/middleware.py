import json

import jwt
import logging
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

# Initialize logger

logger = logging.getLogger(__name__)

# Get JWT secret key
env = Env()
env.read_env()
SECRET_KEY = env("JWT_SECRET_KEY")


def create_response(request_id, code, message):
    try:
        req = str(request_id)
        data = {"data": message, "code": int(code), "request_id": req}
        return data
    except Exception as creation_error:
        logger.error(f'create_response:{creation_error}')


class CustomMiddleware(MiddlewareMixin):
    def process_request(self, request):

        """
        Custom middleware handler to check authentication for a user with JWT authentication
        :param request: Request header containing authorization tokens
        :type request: Django Request Object
        :return: HTTP Response if authorization fails, else None
        """

        jwt_token = request.headers.get('authorization', None)
        logger.info(f"request received for endpoint {str(request.path)}")

        # If token Exists
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
                userid = payload['user_id']
                company_id = payload['company_id'] if 'company_id' in payload else None
                logger.info(f"Request received from user - {userid}, company - {company_id}")
                return None
            except jwt.ExpiredSignatureError:
                response = create_response("", 4001, {"message": "Authentication token has expired"})
                logger.info(f"Response {response}")
                return HttpResponse(json.dumps(response), status=401)
            except (jwt.DecodeError, jwt.InvalidTokenError):
                response = create_response("", 4001, {"message": "Authorization has failed, Please send valid token."})
                logger.info(f"Response {response}")
                return HttpResponse(json.dumps(response), status=401)
        else:
            response = create_response(
                "", 4001, {"message": "Authorization not found, Please send valid token in headers"}
            )
            logger.info(f"Response {response}")
            return HttpResponse(json.dumps(response), status=401)
