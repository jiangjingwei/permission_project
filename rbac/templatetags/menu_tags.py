from django.template import Library
from django.conf import settings
import re, os
from django.utils.safestring import mark_safe

register = Library()


def men_data(request):
    permission_all_menu = request.session[settings.PERMISSION_ALL_MENU]
    permission_user_menu = request.session[settings.PERMISSION_USER_MENU]

    # menu_permission_list = request.session[settings.SESSION_PERMISSION_MENU_URL_KEY]
    # permission_list = menu_permission_list['k1']  # 获取需要挂靠在菜单上显示的权限
    # menu_list = menu_permission_list['k2']  # 获取全部菜单
    all_menu_dict = {}
    # status 是用户全部权限，挂靠显示的菜单；
    # open 当前url（权限）对应的父级菜单展开？
    # 把用户所有的权限挂靠到对应的菜单
    for item in permission_all_menu:
        item['child'] = []
        item['status'] = False
        item['open'] = False
        all_menu_dict[item['id']] = item

    current_url = request.path_info

    for row in permission_user_menu:
        row['status'] = True
        row['open'] = False
        if re.match('^%s$' % (row['permission__url']), current_url):
            row['open'] = True
        all_menu_dict[row['permission__menu_id']]['child'].append(row)
        pid = row['permission__menu_id']
        while pid:
            all_menu_dict[pid]['status'] = True
            pid = all_menu_dict[pid]['parent_caption']
        if row['open']:
            PID = row['permission__menu_id']
            while PID:
                all_menu_dict[PID]['open'] = True
                PID = all_menu_dict[PID]['parent_caption']
    # 把用户所有菜单挂父级菜单
    res = []
    for k, v in all_menu_dict.items():
        if not v.get('parent_caption'):
            res.append(v)
        else:
            pid = v.get('parent_caption')
            all_menu_dict[pid]['child'].append(v)
    return res


# 生成菜单所用HTML
def process_menu_html(menu_list):
    print(menu_list)
    # 盛放菜单所用HTML标签
    tpl1 = """
               <div class='rbac-menu-item'>
                   <div class='rbac-menu-header'>{0}</div>
                   <div class='rbac-menu-body {2}'>{1}</div>
               </div>
           """
    # 盛放权限的HTML
    tpl2 = """
               <a href='{0}' class='{1}'>{2}</a>
           """
    html = ''
    for item in menu_list:
        if not item['status']:
            continue
        else:
            if item.get('permission__url'):
                # 权限
                html += tpl2.format(item['permission__url'], 'rbac_active' if item['open'] else '', item['permission__title'])
            else:
                # 菜单
                html += tpl1.format(item['caption'], process_menu_html(item['child']),
                                    '' if item['open'] else 'rbac-hide')

    return mark_safe(html)


@register.simple_tag
def rbac_menus(request):
    res = men_data(request)
    html = process_menu_html(res)
    return html


@register.simple_tag
def rbac_css():
    file_path = os.path.join('rbac', 'theme', 'rbac.css')
    if os.path.exists(file_path):
        return mark_safe(open(file_path, 'r', encoding='utf-8').read())
    else:
        raise Exception('rbac主题CSS文件不存在')


@register.simple_tag
def rbac_js():
    file_path = os.path.join('rbac', 'theme', 'rbac.js')
    if os.path.exists(file_path):
        return mark_safe(open(file_path, 'r', encoding='utf-8').read())
    else:
        raise Exception('rbac主题JavaScript文件不存在')
