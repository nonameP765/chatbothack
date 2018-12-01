from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .models import KakaoUser, Question, Constitution

DEMO_END_SCORE = 15

DEFAULT_BUTTONS = {
    "type": "buttons",
    "buttons": ["사상체질 진단검사 진행", "빠른 진단검사(데모)"]
}

DEFAULT_BUTTONS_AFTER = {
    "type": "buttons",
    "buttons": ['내 체질 분석', "사상체질 진단검사 진행", "빠른 진단검사(데모)"]
}

DEFAULT_BUTTONS_RESULT = {
    "type": "buttons",
    "buttons": ['주의사항', "음식", "한의사 권유처방", "처음으로"]
}


def keyboard(req):
    if req.method == 'GET':
        return JsonResponse(DEFAULT_BUTTONS)


def friend(req):
    if req.method == 'POST':
        req_data = json.loads(req.body.decode("utf-8"))
        user = KakaoUser(user_id=req_data['user_key'])
        user.save()

        return JsonResponse({})


def friend_delete(req, user_id):
    if req.method == 'DELETE':
        user = KakaoUser.objects.get(user_id=user_id)
        user.delete()
        return JsonResponse({})


def message(req):
    if req.method == 'POST':
        req_data = json.loads(req.body.decode("utf-8"))
        content: str = req_data['content']

        if not KakaoUser.objects.filter(user_id=req_data['user_key']).exists():
            rDict = dict()
            rDict['message'] = dict()
            rDict['message']['text'] = '친구추가 후 이용해주세요.'
            rDict['keyboard'] = DEFAULT_BUTTONS
            return JsonResponse(rDict)

        user = KakaoUser.objects.get(user_id=req_data['user_key'])
        # '주의사항', "음식", "한의사 권유처방", "처음으로"

        if content == '주의사항':
            if len(user.result.split(',')) == 1:
                rDict = dict()
                rDict['message'] = dict()
                rDict['message']["message_button"] = dict()
                rDict['message']["message_button"]['label'] = "동국 분당 한방 병원"
                rDict['message']["message_button"]['url'] = "https://www.dumc.or.kr/index03.jsp"

                rDict['message']['text'] = Constitution.objects.get(name=user.result).warning
                rDict['keyboard'] = DEFAULT_BUTTONS_RESULT
                return JsonResponse(rDict)
        if content == '음식':
            if len(user.result.split(',')) == 1:
                rDict = dict()
                rDict['message'] = dict()
                rDict['message']["message_button"] = dict()
                rDict['message']["message_button"]['label'] = "동국 분당 한방 병원"
                rDict['message']["message_button"]['url'] = "https://www.dumc.or.kr/index03.jsp"
                rDict['message']['text'] = Constitution.objects.get(name=user.result).food
                rDict['keyboard'] = DEFAULT_BUTTONS_RESULT
                return JsonResponse(rDict)
        if content == '한의사 권유처방':
            if len(user.result.split(',')) == 1:
                rDict = dict()
                rDict['message'] = dict()
                rDict['message']["message_button"] = dict()
                rDict['message']["message_button"]['label'] = "동국 분당 한방 병원"
                rDict['message']["message_button"]['url'] = "https://www.dumc.or.kr/index03.jsp"
                rDict['message']['text'] = Constitution.objects.get(name=user.result).prescription
                rDict['keyboard'] = DEFAULT_BUTTONS_RESULT
                return JsonResponse(rDict)
        if content == '처음으로':
            if user.result == '':
                rDict = dict()
                rDict['message'] = dict()
                rDict['message']['text'] = '안녕하세요. 체질 분석 봇입니다.'
                rDict['keyboard'] = DEFAULT_BUTTONS
            else:
                rDict = dict()
                rDict['message'] = dict()
                rDict['message']['text'] = '안녕하세요. 체질 분석 봇입니다.'
                rDict['keyboard'] = DEFAULT_BUTTONS_AFTER

            return JsonResponse(rDict)

        if content == '내 체질 분석':
            if user.result:
                rDict = dict()
                rDict['message'] = dict()
                rDict['message']['text'] = user.result + '이시군요.'
                rDict['keyboard'] = DEFAULT_BUTTONS_RESULT
                return JsonResponse(rDict)

        if content == "사상체질 진단검사 진행":
            user.now_num = 1
            user.taU = 0
            user.taY = 0
            user.soY = 0
            user.soU = 0
            user.testMode = 0
            user.save()
            question = Question.objects.get(num=user.now_num)
            selections = question.selection_set.order_by('num')

            rKeyboard = list()
            for i in selections:
                rKeyboard.append(i.text)
            rKeyboard.append("처음으로")

            rDict = dict()
            rDict['message'] = dict()
            rDict['message']['text'] = question.text
            rDict['keyboard'] = dict()
            rDict['keyboard']['type'] = 'buttons'
            rDict['keyboard']['buttons'] = rKeyboard

            return JsonResponse(rDict)

        if content == "빠른 진단검사(데모)":
            user.now_num = 1
            user.taU = 0
            user.taY = 0
            user.soY = 0
            user.soU = 0
            user.testMode = 1
            user.save()
            question = Question.objects.get(num=user.now_num)
            selections = question.selection_set.order_by('num')

            rKeyboard = list()
            for i in selections:
                rKeyboard.append(i.text)
            rKeyboard.append("처음으로")

            rDict = dict()
            rDict['message'] = dict()
            rDict['message']['text'] = question.text
            rDict['keyboard'] = dict()
            rDict['keyboard']['type'] = 'buttons'
            rDict['keyboard']['buttons'] = rKeyboard

            return JsonResponse(rDict)

        question = Question.objects.get(num=user.now_num)
        selections = question.selection_set.order_by('num')
        if user.testMode == 1:
            if question.isOX:
                if content == '그렇다.':
                    selected = selections.get(text=content)
                    user.soU += selected.soU_rank
                    user.soY += selected.soY_rank
                    user.taU += selected.taU_rank
                    user.taY += selected.taY_rank

                    if user.soU >= DEMO_END_SCORE or user.soY >= DEMO_END_SCORE \
                            or user.taY >= DEMO_END_SCORE or user.taU >= DEMO_END_SCORE:
                        user.now_num = 0
                        user.save()

                        rDict = dict()
                        rDict['message'] = dict()
                        rDict['message']['text'] = '질문이 끝났습니다.\n'

                        max_rank = user.taU
                        max_mode = '태음인'
                        if max_rank == user.taY:
                            max_mode += ',태양인'
                        if max_rank < user.taY:
                            max_mode = '태양인'
                            max_rank = user.taY

                        if max_rank == user.soY:
                            max_mode += ',소양인'

                        if max_rank < user.soY:
                            max_mode = '소양인'
                            max_rank = user.soY

                        if max_rank == user.soU:
                            max_mode += '소음인'

                        if max_rank < user.soU:
                            max_mode = '소음인'

                        user.result = max_mode
                        user.save()

                        rDict['message']['text'] += '당신의 체질은\n' + max_mode + "입니다."

                        rDict['keyboard'] = DEFAULT_BUTTONS_AFTER

                        return JsonResponse(rDict)

                    user.now_num += 1

                    user.save()

                    qo = Question.objects
                    if qo.filter(num=user.now_num).exists():

                        question = Question.objects.get(num=user.now_num)

                        rKeyboard = ['그렇다.', '아니다.', '처음으로']

                        rDict = dict()
                        rDict['message'] = dict()
                        rDict['message']['text'] = question.text
                        rDict['keyboard'] = dict()
                        rDict['keyboard']['type'] = 'buttons'
                        rDict['keyboard']['buttons'] = rKeyboard

                        return JsonResponse(rDict)

                    else:
                        user.now_num = 0
                        user.save()

                        rDict = dict()
                        rDict['message'] = dict()
                        rDict['message']['text'] = '질문이 끝났습니다.\n'

                        max_rank = user.taU
                        max_mode = '태음인'
                        if max_rank == user.taY:
                            max_mode += ',태양인'
                        if max_rank < user.taY:
                            max_mode = '태양인'
                            max_rank = user.taY

                        if max_rank == user.soY:
                            max_mode += ',소양인'

                        if max_rank < user.soY:
                            max_mode = '소양인'
                            max_rank = user.soY

                        if max_rank == user.soU:
                            max_mode += '소음인'

                        if max_rank < user.soU:
                            max_mode = '소음인'

                        user.result = max_mode
                        user.save()

                        rDict['message']['text'] += '당신의 체질은\n' + max_mode + "입니다."

                        rDict['keyboard'] = DEFAULT_BUTTONS_AFTER

                        return JsonResponse(rDict)
                if content == '아니다.':

                    user.now_num += 1

                    user.save()

                    qo = Question.objects
                    if qo.filter(num=user.now_num).exists():

                        question = Question.objects.get(num=user.now_num)

                        rKeyboard = ['그렇다.', '아니다.', '처음으로']

                        rDict = dict()
                        rDict['message'] = dict()
                        rDict['message']['text'] = question.text
                        rDict['keyboard'] = dict()
                        rDict['keyboard']['type'] = 'buttons'
                        rDict['keyboard']['buttons'] = rKeyboard

                        return JsonResponse(rDict)

                    else:
                        user.now_num = 0
                        user.save()

                        rDict = dict()
                        rDict['message'] = dict()
                        rDict['message']['text'] = '질문이 끝났습니다.\n'

                        max_rank = user.taU
                        max_mode = '태음인'
                        if max_rank == user.taY:
                            max_mode += ',태양인'
                        if max_rank < user.taY:
                            max_mode = '태양인'
                            max_rank = user.taY

                        if max_rank == user.soY:
                            max_mode += ',소양인'

                        if max_rank < user.soY:
                            max_mode = '소양인'
                            max_rank = user.soY

                        if max_rank == user.soU:
                            max_mode += '소음인'

                        if max_rank < user.soU:
                            max_mode = '소음인'

                        user.result = max_mode
                        user.save()
                        rDict['message']['text'] += '당신의 체질은\n' + max_mode + "입니다."

                        rDict['keyboard'] = DEFAULT_BUTTONS_AFTER

                        return JsonResponse(rDict)
            else:
                if selections.filter(text=content).exists():
                    selected = selections.get(text=content)
                    user.soU += selected.soU_rank
                    user.soY += selected.soY_rank
                    user.taU += selected.taU_rank
                    user.taY += selected.taY_rank
                    if user.soU >= DEMO_END_SCORE or user.soY >= DEMO_END_SCORE \
                            or user.taY >= DEMO_END_SCORE or user.taU >= DEMO_END_SCORE:
                        user.now_num = 0
                        user.save()

                        rDict = dict()
                        rDict['message'] = dict()
                        rDict['message']['text'] = '질문이 끝났습니다.\n'

                        max_rank = user.taU
                        max_mode = '태음인'
                        if max_rank == user.taY:
                            max_mode += ',태양인'
                        if max_rank < user.taY:
                            max_mode = '태양인'
                            max_rank = user.taY

                        if max_rank == user.soY:
                            max_mode += ',소양인'

                        if max_rank < user.soY:
                            max_mode = '소양인'
                            max_rank = user.soY

                        if max_rank == user.soU:
                            max_mode += '소음인'

                        if max_rank < user.soU:
                            max_mode = '소음인'

                        user.result = max_mode
                        user.save()

                        rDict['message']['text'] += '당신의 체질은\n' + max_mode + "입니다."

                        rDict['keyboard'] = DEFAULT_BUTTONS_AFTER

                        return JsonResponse(rDict)

                    user.now_num += 1

                    user.save()

                    question = Question.objects.get(num=user.now_num)
                    if question.isOX:
                        rKeyboard = ['그렇다.', '아니다.', '처음으로']
                    else:
                        selections = question.selection_set.order_by('num')

                        rKeyboard = list()
                        for i in selections:
                            rKeyboard.append(i.text)
                        rKeyboard.append('처음으로')

                    rDict = dict()
                    rDict['message'] = dict()
                    rDict['message']['text'] = question.text
                    rDict['keyboard'] = dict()
                    rDict['keyboard']['type'] = 'buttons'
                    rDict['keyboard']['buttons'] = rKeyboard

                    return JsonResponse(rDict)
        if user.testMode == 0:
            if question.isOX:
                if content == '그렇다.':
                    selected = selections.get(text=content)
                    user.soU += selected.soU_rank
                    user.soY += selected.soY_rank
                    user.taU += selected.taU_rank
                    user.taY += selected.taY_rank

                    user.now_num += 1

                    user.save()

                    qo = Question.objects
                    if qo.filter(num=user.now_num).exists():

                        question = Question.objects.get(num=user.now_num)

                        rKeyboard = ['그렇다.', '아니다.', '처음으로']

                        rDict = dict()
                        rDict['message'] = dict()
                        rDict['message']['text'] = question.text
                        rDict['keyboard'] = dict()
                        rDict['keyboard']['type'] = 'buttons'
                        rDict['keyboard']['buttons'] = rKeyboard

                        return JsonResponse(rDict)

                    else:
                        user.now_num = 0
                        user.save()

                        rDict = dict()
                        rDict['message'] = dict()
                        rDict['message']['text'] = '질문이 끝났습니다.\n'

                        max_rank = user.taU
                        max_mode = '태음인'
                        if max_rank == user.taY:
                            max_mode += ',태양인'
                        if max_rank < user.taY:
                            max_mode = '태양인'
                            max_rank = user.taY

                        if max_rank == user.soY:
                            max_mode += ',소양인'

                        if max_rank < user.soY:
                            max_mode = '소양인'
                            max_rank = user.soY

                        if max_rank == user.soU:
                            max_mode += '소음인'

                        if max_rank < user.soU:
                            max_mode = '소음인'

                        user.result = max_mode
                        user.save()

                        rDict['message']['text'] += '당신의 체질은\n' + max_mode + "입니다."

                        rDict['keyboard'] = DEFAULT_BUTTONS_AFTER

                        return JsonResponse(rDict)
                if content == '아니다.':

                    user.now_num += 1

                    user.save()

                    qo = Question.objects
                    if qo.filter(num=user.now_num).exists():

                        question = Question.objects.get(num=user.now_num)

                        rKeyboard = ['그렇다.', '아니다.', '처음으로']

                        rDict = dict()
                        rDict['message'] = dict()
                        rDict['message']['text'] = question.text
                        rDict['keyboard'] = dict()
                        rDict['keyboard']['type'] = 'buttons'
                        rDict['keyboard']['buttons'] = rKeyboard

                        return JsonResponse(rDict)

                    else:
                        user.now_num = 0
                        user.save()

                        rDict = dict()
                        rDict['message'] = dict()
                        rDict['message']['text'] = '질문이 끝났습니다.\n'

                        max_rank = user.taU
                        max_mode = '태음인'
                        if max_rank == user.taY:
                            max_mode += ',태양인'
                        if max_rank < user.taY:
                            max_mode = '태양인'
                            max_rank = user.taY

                        if max_rank == user.soY:
                            max_mode += ',소양인'

                        if max_rank < user.soY:
                            max_mode = '소양인'
                            max_rank = user.soY

                        if max_rank == user.soU:
                            max_mode += '소음인'

                        if max_rank < user.soU:
                            max_mode = '소음인'

                        user.result = max_mode
                        user.save()
                        rDict['message']['text'] += '당신의 체질은\n' + max_mode + "입니다."

                        rDict['keyboard'] = DEFAULT_BUTTONS_AFTER

                        return JsonResponse(rDict)
            else:
                if selections.filter(text=content).exists():
                    selected = selections.get(text=content)
                    user.soU += selected.soU_rank
                    user.soY += selected.soY_rank
                    user.taU += selected.taU_rank
                    user.taY += selected.taY_rank

                    user.now_num += 1

                    user.save()

                    question = Question.objects.get(num=user.now_num)
                    if question.isOX:
                        rKeyboard = ['그렇다.', '아니다.', '처음으로']
                    else:
                        selections = question.selection_set.order_by('num')

                        rKeyboard = list()
                        for i in selections:
                            rKeyboard.append(i.text)

                    rDict = dict()
                    rDict['message'] = dict()
                    rDict['message']['text'] = question.text
                    rDict['keyboard'] = dict()
                    rDict['keyboard']['type'] = 'buttons'
                    rDict['keyboard']['buttons'] = rKeyboard

                    return JsonResponse(rDict)
