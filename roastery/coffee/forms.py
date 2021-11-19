from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Column, Div, Hidden, Layout, Row, Submit
from django import forms

from .models import Extraction, Roast


class RoastForm(forms.ModelForm):
    class Meta:
        model = Roast
        fields = ["green_bean", "degree", "roast_date"]

    roast_date = forms.DateField(widget=forms.SelectDateWidget())


class ExtractionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop("user_id")
        self.action = kwargs.pop("action")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"

        self.helper.layout = Layout(
            "roasted_bean",
            Row(
                Column("method", css_class="col-6"),
                Column("grinder", css_class="col-6"),
            ),
            Row(
                Column("dose", css_class="col-6"),
                Column("grind_setting", css_class="col-6"),
            ),
            "temperature",
            "notes",
            Hidden("created_by", self.user_id),
        )

        if self.action == "add":
            self.helper.layout.append(
                Div(
                    Submit("add", "Add", css_class="btn btn-success"),
                    css_class="d-flex justify-content-center",
                )
            )

        if self.action == "update":
            self.helper.layout.append(
                Div(
                    Submit("update", "Update", css_class="btn btn-warning mx-2"),
                    Button(
                        "delete",
                        "Delete",
                        onclick='window.location.href="{}"'.format("../delete"),
                        css_class="btn btn-danger mx-2",
                    ),
                    css_class="d-flex justify-content-center",
                )
            )

    class Meta:
        model = Extraction
        fields = "__all__"
