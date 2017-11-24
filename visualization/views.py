from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .request_detail import get_detail_question,get_detail_answer,get_options_description
from .request_stat import stat_hospital,stat_health
from .update_backend import   update_options,update_helper,update_description,update_segment
from .create_backend import create_description
from .delete_backend import delete_description
from .extra_backend import extra_rate,extra_rate_health
from .models import DevOrgan as status,DevQuestionnairesHelper as Helper
# Create your views here.

# @login_required()
# def questionnaires(request):
#     return render(request,'components/questionnaires.html')

#TODO 有时间改一下shit code
@login_required()
def questionnaires(request):
    question_id = ['36d06675-d061-4a1c-93df-1718fd267fff','a24a4001-6285-467b-a0d5-9be02379a3b0','d7773b71-6986-4cd7-b885-f77e21bd1549']
    question_name = ['区域人口健康信息化建设调查表','医疗健康大数据调查问卷表','医院信息化建设现状调查表']
    question_count = [status.objects.filter(questionnaire_id=id).filter(questionnaire_status='5').count() for id in question_id ]
    question_responent =['省级卫计委,市级卫计委,市级医院','省级卫计委,市级卫计委,委属医院,省属医院,市级医院','委属医院,省属医院,市级医院,市级卫计委']
    question_per_responent =[]
    for id,responents in zip(question_id,question_responent):
        responent = responents.split(',')
        per_responent ={}
        for rp in responent:
            num = status.objects.filter(questionnaire_id=id).filter(questionnaire_status='5').filter(organ_level=rp).count()
            per_responent[rp] = num
        question_per_responent.append(per_responent)
    # ##print(question_per_responent)
    info = [{'name':name,'count':count,'responent':responent,'per_responent':per_rp}\
            for name,count,responent,per_rp in zip(question_name,question_count,question_responent,question_per_responent)]
    # ##print(info)
    question_list = {
        '36d06675-d061-4a1c-93df-1718fd267fff': info[0],
        'a24a4001-6285-467b-a0d5-9be02379a3b0': info[1],
        'd7773b71-6986-4cd7-b885-f77e21bd1549': info[2]
    }

    # questionnaires_name = ['区域人口健康信息化建设调查表（20170303）','医疗健康大数据调查问卷表（20170303）','医院信息化建设现状调查表（20170303）']
    ctx = {'questionnaires_list': question_list,'title':'问卷'}
    # question_list = {
    #
    # }
    # count = status.objects.filter(questionnaire_id=)
    return render(request, 'components/questionnaires.html', ctx)


def questionnaires_data(request):
    '''
    :param request: id ,offset, limit
    :return: questionnaires data in the database
    '''
    questionnaire_id = ''
    if request.GET['id']:
        questionnaire_id = request.GET['id']
    '''
    options too many I ##print it and copied into the values_list
    cause I do not know values_list accept what type data
    '''
    # value_list = ['test_questions_id', 'stem', 'test_questions_type']
    # option_list = ['option_' + str(idx) for idx in range(1, 26)]
    # value_list.extend(option_list)
    # ##print(value_list)
    res_query = Helper.objects.filter(questionnaire_id=questionnaire_id) \
        .values('test_questions_id', 'first_directory','second_directory','stem','stem_helper','type','unit', 'test_questions_type', 'option_1', 'option_2', 'option_3', 'option_4',
                     'option_5', 'option_6', 'option_7', 'option_8', 'option_9', 'option_10', 'option_11', 'option_12',
                     'option_13', 'option_14', 'option_15', 'option_16', 'option_17', 'option_18', 'option_19',
                     'option_20', 'option_21', 'option_22', 'option_23', 'option_24', 'option_25')\
        # .distinct()
        # .all() \
        # .extra({'int_test_questions_id': "CAST(test_questions_id as INTEGER)"}).order_by('int_test_questions_id')
    # ##print(type(res_query),res_query)
    # for res in res_query:
    #     ##print(type(res))
    options =['option_1', 'option_2', 'option_3', 'option_4',
                     'option_5', 'option_6', 'option_7', 'option_8', 'option_9', 'option_10', 'option_11', 'option_12',
                     'option_13', 'option_14', 'option_15', 'option_16', 'option_17', 'option_18', 'option_19',
                     'option_20', 'option_21', 'option_22', 'option_23', 'option_24', 'option_25']
    rows = [{'id': res['test_questions_id'], 'stem': res['stem_helper'],'first_dir':res['first_directory'],'second_dir':res['second_directory'],
             'type': res['test_questions_type'],
             'options': "<br/>".join([res[option_name] for option_name in options if 'option' in option_name and res[option_name]])}
            for res in res_query if res['type']!='6'
            ]
    # ##print('rows_part1',rows)
    rows_part2 = [{'id': res['test_questions_id'], 'stem': res['stem_helper'],'first_dir':res['first_directory'],'second_dir':res['second_directory'],
             'type': res['test_questions_type'],
             'options': res['unit'].replace(';',"<br/>")}
            for res in res_query if res['type']=='6'
            ]
    # ##print('rows_part2',rows_part2)
    rows.extend(rows_part2)
    # ##print('rows',rows)
    rows = sorted(rows,key=lambda x:int(x['id']))

    data = {
        'total': len(rows),
        'rows': rows
    }
    return JsonResponse(rows,safe=False)

@login_required()
def extra(request):
    options_description_h1311 = get_options_description('hospital', 1311)
    options_description_h1906 = get_options_description('hospital', 1906)
    options_description_l1110 = get_options_description('location', 1110)
    page_context = {
        'options_description_h1311': options_description_h1311,
        'options_description_h1906': options_description_h1906,
        'options_description_l1110': options_description_l1110,
    }
    return render(request,'components/extra.html', context=page_context)
#TODO 有时间改一下shit code up

# TODO 记得删除测试页面
@login_required()
def test(request):
    return render(request,'components/test.html')



@login_required()
def detail_question(request, qid, tid):
    mark = qid+str(tid)
    detail_question = get_detail_question(qid,tid)
    helper = detail_question[0]['helper']
    p_type = detail_question[0]['p_type']
    detail_answer = get_detail_answer(qid,tid,p_type)
    options_description = get_options_description(qid,tid)
    options_list = detail_question[0]['options'].split('<br>')
    page_context = {
        'qid':qid,
        'tid':tid,
        'p_type':p_type,
        'helper':helper,
        'option_list':options_list,
        'mark':mark,
        'detail_question':detail_question,
        'detail_answer':detail_answer,
        'options_description':options_description,
    }
    return render(request, 'components/detail.html', context=page_context)

@login_required()
def update_answer_options(request):
    ##print(request)
    front_id = request.GET.get('id','')
    modified_options = request.GET.get('options','None')
    status = update_options(front_id,modified_options)
    return JsonResponse(status)

@login_required()
def update_question_helper(request):
    front_qid = request.GET.get('qid','')
    front_tid = request.GET.get('tid','')
    modified_helper = request.GET.get('helper','None')
    status = update_helper(front_qid,front_tid,modified_helper)
    return JsonResponse(status)


@login_required()
def update_options_description(request):
    front_id = request.GET.get('id','')
    modified_description = request.GET.get('description','None')
    status = update_description(front_id,modified_description)
    return JsonResponse(status)

@login_required()
def update_options_segment(request):
    front_id = request.GET.get('id','')
    modified_description = request.GET.get('options','None')
    status = update_segment(front_id,modified_description)
    return JsonResponse(status)

@login_required()
def create_options_description(request):
    status = {'success':200}
    front_qid = request.POST.get('qid','')
    front_tid = request.POST.get('tid','')
    front_type = request.POST.get('p_type','')
    new_description = request.POST.get('description','')
    options = ''
    if front_type in ['3','4','5']:
        options = request.POST.get('options','')
    if front_type in ['1','2']:
        options = request.POST.getlist('options',[])
    if front_type == '':# 额外开发的比例
        options = request.POST.get('options','')
    if options!='':
        #print('create_options_description succeed')
        status = create_description(front_qid,front_tid,new_description,options)
    return JsonResponse(status)

@login_required()
def delete_options_description(request):
    id_list = request.GET.get('id')
    id_list = [int(x) for x in id_list.split(',')]
    status = delete_description(id_list)
    return JsonResponse(status)

@login_required()
def stat_answer_hospital(request):
    front_qid = request.GET.get('qid', '')
    front_tid = request.GET.get('tid', '')
    front_type = request.GET.get('p_type', '')
    ##print(front_qid,front_tid,front_type)
    # ##print('id_list',id_list)
    lines = stat_hospital(front_qid,front_tid,front_type)
    return JsonResponse({"data":lines})

@login_required()
def stat_answer_health(request):
    front_qid = request.GET.get('qid', '')
    front_tid = request.GET.get('tid', '')
    front_type = request.GET.get('p_type', '')
    ##print(front_qid,front_tid,front_type)
    # ##print('id_list',id_list)
    lines = stat_health(front_qid,front_tid,front_type)
    return JsonResponse({"data":lines})

@login_required()
def stat_extra_rate(request):
    front_qid = request.GET.get('qid', '')
    # front_tid = request.GET.getlist('tid[]', [])
    front_tid = request.GET.get('tid', 0)
    # front_type = request.GET.get('p_type', '')
    ##print('id_list',front_tid)
    lines = []
    if front_tid:
        lines = extra_rate(front_qid,front_tid)
    return JsonResponse({"data":lines})

@login_required()
def stat_extra_rate_health(request):
    front_qid = request.GET.get('qid', '')
    # front_tid = request.GET.getlist('tid[]', [])
    front_tid = request.GET.get('tid', 0)
    # front_type = request.GET.get('p_type', '')
    ##print('id_list',front_tid)
    lines = []
    if front_tid:
        lines = extra_rate_health(front_qid,front_tid)
    return JsonResponse({"data":lines})