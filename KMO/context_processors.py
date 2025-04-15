from datetime import datetime

from KMO.models import Kmodet, Kmo_responsible
from Main.models import Profile


def get_kmodetlist(request):
    try:
        #  Получим подразделение пользователя
        depart = Profile.objects.get(user=request.user)
    except:
        depart = None
    #  Найдём в справочнике "ответственных за устранение" этого ответственного(связь по этому работнику и службе,
    #  так как данный работник может быть ошибочно указан ответственным и в другом подразделении)
    try:
        kmo_responsible = Kmo_responsible.objects.get(idprofile__user=request.user.pk, iddepartment=depart.iddepartment.pk)
    except:
        kmo_responsible = None
    if kmo_responsible:
        # получаем все неустранённые неисправности, где ответственный == авторизованному пользователю
        # rows = Kmodet.objects.filter(idresponsible=kmo_responsible.pk, eliminated=False)
        # for row in rows:
        #     print(row)
        kmodet_master = Kmodet.objects.filter(idresponsible=kmo_responsible.pk, eliminated=False)
        # kmo_master = Kmodet.objects.filter(idresponsible=kmo_responsible.pk, eliminated=False).values('idkmo').group_by('idkmo')
        # print('kmo_master => ', kmo_master)
        qty_kmodet_master = kmodet_master.count
    else:
        kmodet_master = None
        qty_kmodet_master = 0
    return {"kmodet_list": kmodet_master, "kmodet_qty": qty_kmodet_master, 'datenow': datetime.now().date()}
