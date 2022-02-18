from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .api import check_covid
from .forms import PostForm, PostModelForm, CommentModelFrom
from .models import Post ,Comment


#댓글 승인
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('free_post_detail', pk=comment.post.pk)

#댓글 삭제
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('free_post_detail', pk=post_pk)


#댓글 등록
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form =CommentModelFrom(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post #새로 등록하는 comment가 어떤 post에 달리는지에 대한 정보
            comment.save()
            return redirect('free_post_detail', pk=post.pk)
    else:
        form = CommentModelFrom()
    return render(request, 'todayblog/add_comment_to_post.html', {'form': form})


#자유게시판 글 삭제
@ login_required
def post_remove(request, pk):
    post = Post.objects.get(pk=pk) # post = get_object_or_404(Post, pk=pk)과 같은 구문
    post.delete()
    return redirect('free_post_list')


# 자유게시판 글 수정
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('free_post_detail', pk=post.pk)
    else:
        form = PostModelForm(instance=post)
    return render(request, 'todayblog/free_post_edit.html', {'postform': form})


#자유게시판 글 등록
@login_required
def post_new(request):
    if request.method =='POST':
        form= PostForm(request.POST)
        if form.is_valid():
            #검증을 통과한 입력 데이터
            print(form.cleaned_data)
            clean_data_dict = form.cleaned_data
            #create()함수가 호출되면 등록처리가 이루어진다.
            post = Post.objects.create(
                author = request.user,
                title = clean_data_dict['title'],
                text = clean_data_dict['text'],
                published_date= timezone.now()
            )
            return redirect('free_post_list')
    else:
        form = PostForm()
    return render(request, 'todayblog/free_post_edit.html', {'postform': form})

# 자유게시판 글목록
def post_list(request):

    return render(request, 'todayblog/post_list.html')


#자유게시판 글 페이지 목록 pagination
def free_post_list(request):
    post_queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    #Paginator 객체 생성
    paginator = Paginator(post_queryset,2)

    try:
        # page 번호를 화면마다 받을 것임.
        page_number = request.GET.get('page')
        #받아온 페이지 번호로 page 객체 생성
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'todayblog/free_post_list.html', {'post_list': page})

# #자유게시판 글목록
# def free_post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
#     return render(request, 'todayblog/free_post_list.html', {'post_list': posts})

#자유게시판 글 상세정보
def free_post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request, 'todayblog/free_post_detail.html', {'post_key':post})

# 코로나 페이지
def covid_post_list(request):
    date, data = check_covid()
    return render(request, 'todayblog/covid_main.html',
                  {'date': date, 'today_patient': data[0], 'average_patient': data[1],
                   'today_die': data[2], 'average_die': data[3], 'accumulated_die': data[4],
                   'accumulated_patient': data[5]})






