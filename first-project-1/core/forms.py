from django.core.exceptions import ValidationError

class BookingForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        dog = cleaned_data.get('dog')
        kennel = cleaned_data.get('kennel')
        if dog and kennel:
            size_compatibility = {
                'small': ['small', 'medium', 'large'],
                'medium': ['medium', 'large'],
                'large': ['large']
            }
            if kennel.size not in size_compatibility.get(dog.size, ['large']):
                raise ValidationError(f"A {dog.get_size_display()} dog cannot be placed in a {kennel.get_size_display()} kennel.")
        return cleaned_data 