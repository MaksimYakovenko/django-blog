from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView, TemplateView)
from .models import Post, Category, Comment, Profile
from .forms import PostForm, EditForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Count
from django.contrib.auth.models import User
from django.core.paginator import Paginator


# def PaginatorView(request):
#     post_list = Post.objects.all()
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return


# categories_with_post_count = Post.objects.values('category').annotate(
#     post_count=Count('id'))
# for category in categories_with_post_count:
#     print(f"Категория '{category['category']}': {category['post_count']} постов")

# def PaginatorView(request):
#     post_list = Post.objects.all()
#     p = Paginator(post_list, 9)
#     page = request.GET.get('page')
#     page_obj = p.get_page(page)
#     return render(request, "list.html", {"page_obj": page_obj})


# def RatingTop5View(request):
#     popular_posts = Post.objects.annotate(
#         total_likes_count=Count('likes')
#     ).order_by('-total_likes_count')[:5]
#     return render(request, 'home.html', {'popular_posts': popular_posts})

# def RatingView(request):
#     posts = Post.objects.annotate(
#         total_likes_count=Count('likes'),
#         total_dislikes_count=Count('dislikes')
#     ).order_by('-total_likes_count', 'total_dislikes_count')[:5]
#     return render(request, 'home.html', {'posts': posts})


def LikeDislikeView(request, pk):
    feedback = request.POST.get('feedback')
    post = get_object_or_404(Post, id=pk)
    if feedback == 'like':
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
    elif feedback == 'dislike':
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
        else:
            post.dislikes.add(request.user)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)

    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-post_date', '-id']
    paginate_by = 6

    def get_context_data(self, *args, **kwargs):
        cat_menu = Post.objects.values('category').annotate(
            post_count=Count('id'))
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        top_rated_posts = Post.objects.annotate(
            total_likes_count=Count('likes'),
            total_dislikes_count=Count('dislikes')
        ).order_by('-total_likes_count', 'total_dislikes_count')[:4]
        rated_posts = Post.objects.annotate(
            total_likes_count=Count('likes'),
            total_dislikes_count=Count('dislikes')
        ).order_by('-total_likes_count', 'total_dislikes_count')
        active_users = User.objects.annotate(
            post_count=Count('post')
        ).order_by('-post_count')[:4]
        trending_posts = Post.objects.annotate(
            comment_count=Count('comments')
        ).order_by('-comment_count')[:3]
        context['rated_posts'] = rated_posts
        context['trending_posts'] = trending_posts
        context['active_users'] = active_users
        context['top_rated_posts'] = top_rated_posts
        return context


def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list':
                                                      cat_menu_list})


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    cat_menu = Post.objects.values('category').annotate(
        post_count=Count('id'))
    top_rated_posts = Post.objects.annotate(
        total_likes_count=Count('likes'),
        total_dislikes_count=Count('dislikes')
    ).order_by('-total_likes_count', 'total_dislikes_count')[:4]
    rated_posts = Post.objects.annotate(
        total_likes_count=Count('likes'),
        total_dislikes_count=Count('dislikes')
    ).order_by('-total_likes_count', 'total_dislikes_count')
    active_users = User.objects.annotate(
        post_count=Count('post')
    ).order_by('-post_count')[:4]
    trending_posts = Post.objects.annotate(
        comment_count=Count('comments')
    ).order_by('-comment_count')[:3]

    context = {
        'cats': cats.title().replace('-', ' '),
        'category_posts': category_posts,
        'cat_menu': cat_menu,
        'rated_posts': rated_posts,
        'trending_posts': trending_posts,
        'active_users': active_users,
        'top_rated_posts': top_rated_posts
    }

    return render(request, 'categories.html', context)


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args,
                                                                  **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        total_dislikes = stuff.total_dislikes()

        if stuff.likes.filter(id=self.request.user.id).exists():
            feedback = 'like'
        elif stuff.dislikes.filter(id=self.request.user.id).exists():
            feedback = 'dislike'
        else:
            feedback = ''
        rated_posts = Post.objects.annotate(
            total_likes_count=Count('likes'),
            total_dislikes_count=Count('dislikes')
        ).order_by('-total_likes_count', 'total_dislikes_count')
        context['rated_posts'] = rated_posts
        context['cat_menu'] = cat_menu
        context['total_likes'] = total_likes
        context['total_dislikes'] = total_dislikes
        context['feedback'] = feedback
        return context


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    # fields = '__all__'


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'

    # fields = '__all__'
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.name = f"{self.request.user.first_name} {self.request.user.last_name}"
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article-detail', kwargs={'pk': self.kwargs['pk']})


class AddCategoryView(CreateView):
    model = Category
    # form_class = PostForm
    template_name = 'add_category.html'
    fields = '__all__'


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'
    success_url = '/'

    # fields = ['title', 'title_tag', 'body']

    def form_valid(self, form):
        return super().form_valid(form)


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


class AboutUsView(TemplateView):
    template_name = 'about.html'


class ContactUsView(TemplateView):
    template_name = 'contact.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'privacy.html'


class OurTeamView(TemplateView):
    template_name = 'our_team.html'
