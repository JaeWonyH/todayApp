from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import PostForm
from .models import Post ,Comment

#글 삭제
@ login_required
def post_remove(request, pk):
    post = Post.objects.get(pk=pk) # post = get_object_or_404(Post, pk=pk)과 같은 구문
    post.delete()
    return redirect('free_post_list')


# 글 수정
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = Post(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = Post(instance=post)
    return render(request, 'todayblog/free_post_edit.html', {'postform': form})


#글 등록
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
            return redirect('free_post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'todayblog/free_post_edit.html', {'postform': form})

# 글목록
def post_list(request):

    return render(request, 'todayblog/post_list.html')

#자유게시판 글목록
def free_post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'todayblog/free_post_list.html', {'post_list': posts})

#자유게시판 글 상세정보
def free_post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request, 'todayblog/free_post_detail.html', {'post_key':post})

