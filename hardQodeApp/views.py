from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse

from hardQodeApp.models import Product, LessonView


def get_lessons(request):
    user = request.user

    # Получаем все продукты, к которым пользователь имеет доступ
    products = Product.objects.filter(owner=user)

    lessons_data = []

    for product in products:
        lessons = product.lesson_set.all()

        for lesson in lessons:
            try:
                lesson_view = LessonView.objects.get(lesson=lesson, user=user)
                status = lesson_view.status
                viewed_time = lesson_view.viewed_time
            except LessonView.DoesNotExist:
                status = "Не просмотрено"
                viewed_time = None

            # Формируем данные урока
            lesson_data = {
                "name": lesson.name,
                "video_link": lesson.video_link,
                "duration": lesson.duration.total_seconds(),
                "status": status,
                "viewed_time": viewed_time.total_seconds() if viewed_time else None
            }

            lessons_data.append(lesson_data)

    return JsonResponse(lessons_data, safe=False)


def get_lessons_by_product(request, product_id):
    user = request.user

    try:
        product = Product.objects.get(id=product_id, owner=user)
    except Product.DoesNotExist:
        return HttpResponse({"error": "Продукт не найден или не принадлежит пользователю"})

    lessons = product.lesson_set.all()

    lessons_data = []

    for lesson in lessons:
        try:
            lesson_view = LessonView.objects.get(lesson=lesson, user=user)
            status = lesson_view.status
            viewed_time = lesson_view.viewed_time
        except LessonView.DoesNotExist:
            status = "Не просмотрено"
            viewed_time = None

        lesson_data = {
            "name": lesson.name,
            "video_link": lesson.video_link,
            "duration": lesson.duration.total_seconds(),
            "status": status,
            "viewed_time": viewed_time.total_seconds() if viewed_time else None,
            "last_viewed_time": lesson_view.created_time if viewed_time else None
        }

        lessons_data.append(lesson_data)

    return HttpResponse(lessons_data)


def product_stat(request, product_id):
    product = Product.objects.get(id=product_id)

    num_viewed_lessons = LessonView.objects.filter(lesson__products=product, status="Просмотрено").count()

    total_viewing_time = LessonView.objects.filter(lesson__products=product).aggregate(total_time=Sum('viewed_time'))[
        'total_time']

    num_students = User.objects.filter(lessonview__lesson__products=product).distinct().count()

    num_users = User.objects.count()
    num_accesses = product.lesson_set.count()
    purchase_percent = (num_accesses / num_users) * 100

    data = {
        "product_name": product.name,
        "num_viewed_lessons": num_viewed_lessons,
        "total_viewing_time": total_viewing_time,
        "num_students": num_students,
        "purchase_percent": purchase_percent
    }

    return JsonResponse(data)
