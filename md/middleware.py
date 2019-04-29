from django.shortcuts import render,HttpResponse,redirect

class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class M1(MiddlewareMixin):
    def process_request(self,request):
        print('@@@@m1.process_request')

        if request.path_info == '/login/':
            request.session.flush()
            print('##############')
            return None

        username = request.session.get('username',None)
        print('################',username)
        if not username:
            return redirect('/login/')
    def process_exception(self,request,exception):
        return render(request, '500.html')
    def process_response(self,request, response):
        if response.status_code==404:
            return render(request,'404.html')
        return response