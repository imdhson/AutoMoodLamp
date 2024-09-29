from django.shortcuts import render

def client_main_view(request):
    #태영이 수정해야 할 것

    #로그인 된 유저의 sequenceData를 받아오기
    # 받아와서 context에 넣어서 client_main.html에서 적절하게 화면에 표시
    context = {}
    return render(request, 'client_main.html', context)