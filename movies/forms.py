from django import forms


from .models import Reviews


class ReviewForm(forms.ModelForm):
    """Форма отправки отзывов"""
    class Meta:
        # ! От какой модели наследуемся
        model = Reviews
        # ! Какие поля из модели будут в форме
        fields = ("name", "email", "text")
