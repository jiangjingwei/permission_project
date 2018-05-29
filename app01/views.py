from django.shortcuts import render, redirect, HttpResponse
from rbac import models, forms
from django.conf import settings


def init_permission(request, user_obj):
    # 所有菜单
    permission_all_menu = models.Menu.objects.values('id', 'caption', 'parent_caption')

    permission_list = user_obj.roles.values('id', 'permission__title', 'permission__url', 'permission__menu_id')

    permission_user_url = []
    permission_user_menu = []
    for item in permission_list:
        permission_user_url.append(item['permission__url'])
        if item['permission__menu_id']:
            permission_user_menu.append(item)

    request.session[settings.PERMISSION_ALL_MENU] = list(permission_all_menu)
    request.session[settings.PERMISSION_USER_URL] = list(permission_user_url)
    request.session[settings.PERMISSION_USER_MENU] = list(permission_user_menu)


def login(request):
    response_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = models.UserInfo.objects.filter(username=username, password=password).first()

        if not user:
            response_msg['error'] = '用户名密码错误'
        else:
            request.session['user'] = username
            # 初始化数据写入session
            init_permission(request, user)
            return redirect('/index/')

    return render(request, 'login.html', {'response_msg': response_msg})


def index(request):
    if request.session.get('user'):

        user_list = models.UserInfo.objects.all()
        # permission_all_menu = request.session[settings.PERMISSION_ALL_MENU]
        # permission_user_menu = request.session[settings.PERMISSION_USER_MENU]
        # print('permission_all_menu', permission_all_menu)
        # print('permission_user_menu', permission_user_menu)

        # all_menu_dict = {}
        #
        # for item in permission_all_menu:
        #     item['child'] = []

        return render(request, 'index.html', locals())
    else:
        return redirect('/login/')


def user_add(request):

    if request.method == 'POST':
        user_form = forms.UserModel(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('/index/')
    user_form = forms.UserModel()
    return render(request, 'app01/user_add.html', locals())


def user_change(request, id):
    user = models.UserInfo.objects.filter(id=id).first()
    if request.method == 'POST':
        user_form = forms.UserModel(request.POST, instance=user)
        user_form.save()
        return redirect('/index/')
    user_form = forms.UserModel(instance=user)
    return render(request, 'app01/user_change.html', locals())


def user_delete(request, id):
    
    return render(request, 'app01/user_delete.html')


