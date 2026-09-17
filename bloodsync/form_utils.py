class BootstrapFormMixin:
    """Adds Bootstrap 'form-control' / 'form-select' classes to every field widget."""

    def apply_bootstrap_classes(self):
        for field in self.fields.values():
            widget = field.widget
            existing = widget.attrs.get('class', '')
            if widget.__class__.__name__ in ('Select', 'SelectMultiple'):
                css_class = 'form-select'
            elif widget.__class__.__name__ == 'CheckboxInput':
                css_class = 'form-check-input'
            elif widget.__class__.__name__ == 'ClearableFileInput':
                css_class = 'form-control'
            else:
                css_class = 'form-control'
            widget.attrs['class'] = (existing + ' ' + css_class).strip()
