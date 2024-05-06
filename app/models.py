from django.core.validators import MinValueValidator
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


# клас для обработки основных данных
class Tagsquestions:

    def __init__(self, post=None):
        self.posts = post

    class Questionsandtags:
        tags = []
        answers = None

        def __init__(self, question, given):
            self.tags = question.tag_id.all()
            self.answers = given

    def answers(self):
        answer = dict()
        for post in self.posts:
            tagsobject = self.Questionsandtags(post, Answers.objects.filter(question_id=post.id).count())
            answer[post] = tagsobject

        return answer


# клас для получение тегов
class Gettegs:

    def __init__(self, question):
        self.tags = question.tag_id.all()


# клас для обработки пагинации
class Paginate:
    @staticmethod
    def paginate(objects_list, request, per_page=10):
        paginator = Paginator(objects_list, per_page)

        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
            page = 1
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
            page = paginator.num_pages

        n = posts.paginator.num_pages

        ran = []

        for i in range(max(1, int(page) - 2), min(n, int(page) + 2) + 1):
            ran.append(i)

        if not (int(n) in ran):
            ran.append('...')
            ran.append(int(n))

        if not (1 in ran):
            ran = [1, '...'] + ran

        return posts, page, ran


# клас для получения основных данных по профилю
class ProfileGet:

    def __init__(self, posts):
        self.posts = posts

    class HelpQuestionsandtags:
        tags = []
        answers = None
        profile = None

        def __init__(self, question, given):
            self.tags = question.tag_id.all()
            self.answers = given
            self.profile = Profiles.objects.get(id=question.profile_id.id)

    def get_profile_and_ans(self):
        answer = dict()
        for post in self.posts:
            answer[post] = self.HelpQuestionsandtags(post, Answers.objects.filter(question_id=post.id).count())
        return answer


# клас реализующий таблицу профили
class Profiles(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(blank=True)
    create = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)


# клас реализующий таблицу теги
class Tags(models.Model):
    tag = models.CharField(max_length=255)


# клас реализующий таблицу ответы
class Answers(models.Model):
    title = models.CharField(max_length=255)
    answer = models.TextField()
    right = models.BooleanField(default=False)
    profile_id = models.ForeignKey('Profiles', on_delete=models.PROTECT)
    question_id = models.ForeignKey('Questions', on_delete=models.PROTECT)
    rating = models.IntegerField(default=0)
    create = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)


# клас обрабатывающий порядок вывода вопросов
class QuestionManager(models.Manager):
    def get_hot(self):
        return self.all().order_by('-rating', 'title')

    def get_new(self):
        return self.all().order_by('-last_update', '-create', 'title')

    def get_tag(self, tag):
        questions_by_teg = []
        for element in self.all():
            if tag in [tag.tag for tag in element.tag_id.all()]:
                questions_by_teg.append(element)

        return questions_by_teg


# клас реализующий таблицу вопросы
class Questions(models.Model):
    title = models.CharField(max_length=255)
    question = models.TextField()
    profile_id = models.ForeignKey('Profiles', on_delete=models.PROTECT)
    countanswers = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    create = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    tag_id = models.ManyToManyField('Tags')

    objects = QuestionManager()


# клас реализующий таблицу лайки для вопросов
class Likequestion(models.Model):
    marker = models.BooleanField()
    question_id = models.ForeignKey('Questions', on_delete=models.PROTECT)
    profile_id = models.ForeignKey('Profiles', on_delete=models.PROTECT)
    create = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('question_id', 'profile_id')


# клас реализующий таблицу лайки для ответов
class Likeanswers(models.Model):
    marker = models.BooleanField()
    answer_id = models.ForeignKey('Answers', on_delete=models.PROTECT)
    profile_id = models.ForeignKey('Profiles', on_delete=models.PROTECT)
    create = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('answer_id', 'profile_id')


# При генерации удалить 6 функций (тригеры)
# При удалении/добавлении данных из/в Likequestion меняем рейтинг у соответствующего вопроса
@receiver(post_delete, sender=Likequestion)
def update_question_likes(sender, instance, **kwargs):
    question = instance.question_id
    if instance.marker:
        question.rating -= 1
    else:
        question.rating += 1
    question.save()


@receiver(post_save, sender=Likequestion)
def update_question_likes(sender, instance, **kwargs):
    question = instance.question_id
    if instance.marker:
        question.rating += 1
    else:
        question.rating -= 1
    question.save()


# При удалении/добавлении данных из/в Likeanswers меняем рейтинг у соответствующего ответа
@receiver(post_delete, sender=Likeanswers)
def update_question_likes(sender, instance, **kwargs):
    answer = instance.answer_id
    if instance.marker:
        answer.rating -= 1
    else:
        answer.rating += 1
    answer.save()


@receiver(post_save, sender=Likeanswers)
def update_question_likes(sender, instance, **kwargs):
    answer = instance.answer_id
    if instance.marker:
        answer.rating += 1
    else:
        answer.rating -= 1
    answer.save()


# При удалении/добавлении данных из/в Answers изменяем количесто ответов у соответствуюего вопроса
@receiver(post_delete, sender=Answers)
def update_question_likes(sender, instance, **kwargs):
    question = instance.question_id
    question.countanswers -= 1
    question.save()


@receiver(post_save, sender=Answers)
def update_question_likes(sender, instance, **kwargs):
    question = instance.question_id
    question.countanswers += 1
    question.save()
