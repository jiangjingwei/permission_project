from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect, HttpResponse
import re


class PermissionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        path_url = request.path_info

        for url in settings.ALLOWED_URL:
            if re.match(url, path_url):
                return None

        user = request.session.get('user')
        if not user:
            return redirect('/login/')

        permission_user_url = request.session[settings.PERMISSION_USER_URL]

        flag = False

        for per_url in permission_user_url:
            pattern = settings.REGEX_URL.format(per_url)
            # print(per_url, path_url)
            if re.match(pattern, path_url):
                # print('match', path_url)
                flag = True
                break

        if not flag:
            if settings.DEBUG:
                html = '<br/>'.join(permission_user_url)
                return HttpResponse('无权访问，你可以访问：%s' % html)

            else:
                return HttpResponse('没有权限')


