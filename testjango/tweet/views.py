from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
from .models import TweetModel
from .models import TweetComment
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    # 로그인 된 유저만 가져오기
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')


@login_required
def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'tweet': all_tweet})
        else:
            return redirect('/sign-in')

    elif request.method == 'POST':
        user = request.user
        content = request.POST.get('my-content', '')
        tags = request.POST.get('tag', '').split(',')
        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'error': '빈글은 저장할 수 없습니다'})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            for tag in tags:
                # 태그의 공백을 제거
                tag = tag.strip()
                if tag != '':
                    my_tweet.tags.add(tag)
            my_tweet.save()
            return redirect('/tweet')


@login_required
# 삭제해줄 게시글의 id
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')


@login_required
def detail_tweet(request, id):
    # TweetModel DB id에 user id를 넣어줌
    my_tweet = TweetModel.objects.get(id=id)
    # user id만 필터링해서 최신순으로 정렬해줌 (tweet_id = id) 이부분 주의.
    comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request, 'tweet/tweet_detail.html', {'tweet': my_tweet, 'comment': comment})
    # render와 redirect 구분 잘 하기


@login_required
def write_comment(request, id):
    if request.method == 'POST':
        comment = request.POST.get("comment", "")
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        # 이부분 이해 안감
        TC.tweet = current_tweet
        TC.author = request.user
        TC.save()

        return redirect('/tweet/'+str(id))


@login_required
def delete_comment(request, id):
    my_comment = TweetComment.objects.get(id=id)
    # redirect를 tweet로 해주려고 id를 지정
    tweet = my_comment.tweet.id
    my_comment.delete()
    return redirect('/tweet/'+str(tweet))


class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context
