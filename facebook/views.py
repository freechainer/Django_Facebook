from django.shortcuts import render
from facebook.models import Article
from facebook.models import Comment
from django.shortcuts import render
from django.shortcuts import redirect


# Create your views here.

def play(request):
    return render(request, 'play.html')

def play2(request):
    heoinhaeng = '허인행'
    return render(request, 'play2.html', { 'name': heoinhaeng})

def my_profile(request):
    return render(request, 'profile.html')

def fail(request):
    return render(request, 'fail.html')

def help(request):
    return render(request, 'help.html')

def warn(request):
    return render(request, 'warn.html')

def event(request):
    return render(request, 'event.html')


def newsfeed(request):
    articles = Article.objects.all()

    return render(request, 'newsfeed.html', { 'articles': articles })

def detail_feed(request, pk):
    article = Article.objects.get(pk=pk)

    if request.method == 'POST':  # new comment
        Comment.objects.create(
            article=article,
            author=request.POST['nickname'],
            text=request.POST['reply'],
            password=request.POST['password']
        )

        return redirect(f'/feed/{ article.pk }')

    return render(request, 'detail_feed.html', {'feed': article})



# 중간생략

def new_feed(request):
    if request.method == 'POST': # 폼이 전송되었을 때만 아래 코드를 실행
        if request.POST['author'] != '' and request.POST['title'] != '' and request.POST['content'] != '' and request.POST['password'] != '':
            text = request.POST['content']
            text = text + ' - 추신: 감사합니다.'

            new_article = Article.objects.create(
                author=request.POST['author'],
                title=request.POST['title'],
                text=text,
                password=request.POST['password']
            )

            # 새글 등록 끝
            return redirect(f'/feed/{ new_article.pk }')

    return render(request, 'new_feed.html')

def remove_feed(request, pk):
    article = Article.objects.get(pk=pk)

    if request.method == 'POST':
        if request.POST['password'] == article.password:
            article.delete()
            return redirect('/') # 첫페이지로 이동하기

        else:
            return redirect('/fail/')  # 비밀번호 오류 페이지 이동하기

    return render(request, 'remove_feed.html', {'feed': article})

def edit_feed(request, pk):
    article = Article.objects.get(pk=pk)

    if request.method == 'POST':
        if request.POST['password'] == article.password:
            article.author = request.POST['author']
            article.title = request.POST['title']
            article.text = request.POST['content']
            article.save()
            return redirect(f'/feed/{ article.pk }')
        else:
            return redirect('/fail/')  # 비밀번호 오류 페이지 이동하기

    return render(request, 'edit_feed.html', {'feed': article})