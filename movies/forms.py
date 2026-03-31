from django import forms
from .models import UserMovie

class UserMovieForm(forms.ModelForm):
    class Meta:
        model = UserMovie
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} ⭐') for i in range(1, 11)],
                attrs={'class': 'form-select'}
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Напиши что думаешь о фильме...'
                }
            ),
        }
        labels = {
            'rating': 'Твоя оценка',
            'comment': 'Комментарий',
        }