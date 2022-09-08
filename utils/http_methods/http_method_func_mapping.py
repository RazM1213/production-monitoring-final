from send.get_request_sender import GetRequestSender
from send.post_request_sender import PostRequestSender
from utils.http_methods.http_methods_enum import HttpMethodsEnum

HTTP_METHODS_FUNCS = {
    HttpMethodsEnum.GET.value: lambda request, session: GetRequestSender(request).send_request(session),
    HttpMethodsEnum.POST.value: lambda request, session: PostRequestSender(request).send_request(session)
}
