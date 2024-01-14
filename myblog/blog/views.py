from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.db.models import Count


# def home(request):
#     return render(request, 'home.html', {})

def RatingView(request):
    posts = Post.objects.annotate(
        total_likes_count=Count('likes'),
        total_dislikes_count=Count('dislikes')
    ).order_by('-total_likes_count', 'total_dislikes_count')

    return render(request, 'rating-list.html', {'posts': posts})


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
    ordering = ['-post_date']

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context


def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list':
                                                      cat_menu_list})


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'categories.html', {'cats': cats.title().replace(
        '-', ' '),
        'category_posts': category_posts})


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

    success_url = reverse_lazy('home')


class AddCategoryView(CreateView):
    model = Category
    # form_class = PostForm
    template_name = 'add_category.html'
    fields = '__all__'


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'
    # fields = ['title', 'title_tag', 'body']


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')
