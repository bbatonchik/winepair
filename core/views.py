from django.shortcuts import render
from .models import Wine, RecommendationLog, Subscriber
from django.db.models import Count, Avg


def home(request):
    wines = []
    best_wine = None
    email_message = None

    avg_budget = 0
    popular = []
    popular_sauce = None
    budget_ranges = [0, 0, 0, 0]

    if request.method == "POST":

        # ===============================
        # ФОРМА ПОДБОРА ВИНА
        # ===============================
        if "get_recommendation" in request.POST:

            ingredient = request.POST.get("ingredient")
            sauce = request.POST.get("sauce")
            budget_str = request.POST.get("budget")

            try:
                budget = int(budget_str)
            except (TypeError, ValueError):
                budget = None

            if budget:

                # сохраняем запрос
                RecommendationLog.objects.create(
                    ingredient=ingredient,
                    sauce=sauce,
                    budget=budget
                )

                wines_queryset = Wine.objects.filter(price__lte=budget)
                recommended = []

                for wine in wines_queryset:
                    score = 0
                    explanation = []

                    # Тип блюда
                    if ingredient == "мясо" and wine.type == "red":
                        score += 3
                        explanation.append("Красное вино идеально подходит к мясу")

                    if ingredient == "рыба" and wine.type == "white":
                        score += 3
                        explanation.append("Белое вино хорошо сочетается с рыбой")

                    # Соус
                    if sauce == "сливочный" and wine.acidity >= 3:
                        score += 2
                        explanation.append("Кислотность балансирует сливочный соус")

                    if sauce == "томатный" and wine.acidity >= 4:
                        score += 2
                        explanation.append("Высокая кислотность подходит к томатам")

                    # Сладость
                    if ingredient == "рыба" and wine.sweetness <= 2:
                        score += 1
                        explanation.append("Низкая сладость лучше для рыбы")

                    # Уровень уверенности
                    confidence = min(score * 20, 100)

                    recommended.append({
                        "wine": wine,
                        "score": score,
                        "explanation": explanation,
                        "confidence": confidence
                    })

                recommended.sort(key=lambda x: x["score"], reverse=True)

                wines = recommended

                if wines:
                    best_wine = wines[0]

        # ===============================
        # ФОРМА ПОДПИСКИ
        # ===============================
        elif "subscribe" in request.POST:

            email = request.POST.get("email")

            if email:
                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(email=email)
                    email_message = "Вы успешно подписаны!"
                else:
                    email_message = "Вы уже подписаны."

    # ===============================
    # АНАЛИТИКА
    # ===============================

    logs = RecommendationLog.objects.all()

    if logs.exists():

        avg_budget = logs.aggregate(avg=Avg('budget'))['avg'] or 0

        popular = (
            logs.values('ingredient')
            .annotate(count=Count('id'))
            .order_by('-count')[:3]
        )

        sauce_counts = (
            logs.values('sauce')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        if sauce_counts.exists():
            popular_sauce = sauce_counts[0]

        for log in logs:
            if log.budget <= 1000:
                budget_ranges[0] += 1
            elif log.budget <= 3000:
                budget_ranges[1] += 1
            elif log.budget <= 5000:
                budget_ranges[2] += 1
            else:
                budget_ranges[3] += 1

    return render(request, "home.html", {
        "wines": wines,
        "best_wine": best_wine,
        "popular": popular,
        "popular_sauce": popular_sauce,
        "avg_budget": avg_budget,
        "budget_ranges": budget_ranges,
        "email_message": email_message,
    })