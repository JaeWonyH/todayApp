from django.shortcuts import render

# Create your views here.

# 글목록
def post_list_first(request):

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html',{'post_list':posts} )
