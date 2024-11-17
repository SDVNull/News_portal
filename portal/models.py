from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    author_user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="author"
    )
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return f'{self.author_user.username}'

    def update_rating(self):
        post_rating = self.post_set.aggregate(p_rating=Sum("rating")).get("p_rating")
        if post_rating is None:
            post_rating = 0
        comm_rating = self.author_user.comment_set.aggregate(
            c_rating=Sum("rating")
        ).get("c_rating")
        if comm_rating is None:
            comm_rating = 0
        post_comm_rating = (
            Comment.objects.filter(user_comment__author=self)
            .aggregate(pc_rating=Sum("rating"))
            .get("pc_rating")
        )
        if post_comm_rating is None:
            post_comm_rating = 0
        self.rating = post_rating * 3 + comm_rating + post_comm_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Категория: {self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    CHOICE = [
        ("NW", "Новость"),
        ("AR", "Статья"),
    ]
    field_choice = models.CharField(max_length=2, choices=CHOICE, default="NW")
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    header = models.CharField(max_length=150)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('portal:detail_news', args=[str(self.id)])

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()

    def preview(self):
        return self.content[:123] + "..."

    def __str__(self):
        return f"{self.author}"

    def __repr__(self):
        return self.__str__()


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time_comment = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Subscription(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='subscriptions')
