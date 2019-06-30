import logging
import requests

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response


# ngrok url or public ip, replace with your own
SKILL_NAME = "robot voice commands"
API_ENDPOINT = "http://replace_with_your_own"
HELP_MESSAGE = "You can left 50, right 100, forward replacing the numbers with degrees values. Or " \
               "you can say lights on and lights off"
HELP_REPROMPT = "What can I help you with?"
LAUNCH_MESSAGE = "Tell me your command"
STOP_MESSAGE = "Goodbye!"
EXCEPTION_MESSAGE = "Sorry. Some problems occured"
SENDING_MESSAGE = "Sending"


sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)



class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        handler_input.response_builder.speak(LAUNCH_MESSAGE).ask("hmm should reprompt")
        return handler_input.response_builder.response


class SteeringCommand(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return (is_intent_name("SteeringCommand")(handler_input))

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("In SteeringCommand")
        given_command = handler_input.request_envelope.request.intent.slots["Command"].value
        angle = str(handler_input.request_envelope.request.intent.slots["number"].value)
        requests.post(url=API_ENDPOINT + '/api/motors', data={'command': given_command, 'angle': angle})
        handler_input.response_builder.speak(SENDING_MESSAGE).ask("hmm should reprompt")
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        handler_input.response_builder.speak(HELP_MESSAGE).ask(HELP_REPROMPT).\
            set_card(SimpleCard(SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("In CancelOrStopIntentHandler")
        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("In FallbackIntentHandler")
        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        logger.info("Session ended reason: {}".format(handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input: HandlerInput, exception: Exception) -> bool:
        return True

    def handle(self, handler_input: HandlerInput, exception: Exception) -> Response:
        logger.error(exception, exc_info=True)
        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(HELP_REPROMPT)

        return handler_input.response_builder.response


class RequestLogger(AbstractRequestInterceptor):
    def process(self, handler_input: HandlerInput) -> None:
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    def process(self, handler_input: HandlerInput, response: Response):
        logger.debug("Alexa Response: {}".format(response))



# Register intent handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SteeringCommand())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()