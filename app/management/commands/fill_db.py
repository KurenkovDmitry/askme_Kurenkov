from django.core.management.base import BaseCommand
from app.models import Tags, Questions, Answers, Profiles, User, Likequestion, Likeanswers


class Command (BaseCommand):
    help = 'Fill Tags model with random elements based on given ratio'

    @staticmethod
    def delete():
        Likequestion.objects.all().delete()
        Likeanswers.objects.all().delete()
        Answers.objects.all().delete()
        Questions.objects.all().delete()
        Profiles.objects.all().delete()
        User.objects.all().delete()
        Tags.objects.all().delete()

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs=1, type=int, help='Number of random elements to create')

    def handle(self, *args, **options):
        ratio = options['ratio'][0]

        ratio = max(ratio, 8)

        # Удаляем все данные из таблиц
        self.delete()

        # Создаем данные в каличестве зависимом от ratio
        # Tags
        for i in range(ratio):
            tag_name = f'Tag {i}'
            Tags.objects.create(tag=tag_name)

            # User and profile
            username_test = f'Username{i}'
            password_test = f'Password{i}'
            user = User.objects.create(username=username_test, password=password_test)
            fio = f'Никнейм{i}'
            Profiles.objects.create(name=fio, user=user)

        count = 200 * ratio
        user = []
        for i in range(max(ratio // 4, 10)):
            name_test = f'Никнейм{i}'
            user.append(Profiles.objects.get(name=name_test).id)

        # Questions
        for i in range(10 * ratio):
            title_test = f'Title - {i}'
            question_test = f'Question {i}?'
            Questions.objects.create(title=title_test, question=question_test,
                                     profile_id_id=user[i % min(10, ratio // 4)], countanswers=10)

            quest = Questions.objects.get(title=title_test)

            # Answer
            for j in range(10):
                title_test = f'Title - {i * 10 + j}'
                answer_test = f'Answer {i * 10 + j}'
                Answers.objects.create(profile_id_id=user[(i * 10 + j) % min(10, ratio // 4)], question_id_id=quest.id,
                                       title=title_test, answer=answer_test, right=False)

            # Like
            ans = Answers.objects.get(title=title_test)
            for k in range(0, min(ratio // 4, count)):
                count -= 1
                ids = user[k]
                if k % 2 == 0:
                    Likeanswers.objects.create(marker=True, answer_id_id=ans.id, profile_id_id=ids)
                    Likequestion.objects.create(marker=False, question_id_id=quest.id,
                                                profile_id_id=ids)
                else:
                    Likeanswers.objects.create(marker=False, answer_id_id=ans.id, profile_id_id=ids)
                    Likequestion.objects.create(marker=True, question_id_id=quest.id,
                                                profile_id_id=ids)

        self.stdout.write(self.style.SUCCESS("Successfully created bd"))
