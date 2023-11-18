import shutil

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, TestCase
from django.urls import reverse

from feedback.forms import FeedbackForm, FeedbackInfoForm
from feedback.models import Feedback, FeedbackFile


class FormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base_form = FeedbackForm()
        cls.base_info_form = FeedbackInfoForm()

    def test_context(self):
        response = self.client.get(reverse("feedback:feedback"))
        self.assertIn("form", response.context)
        self.assertIn("info_form", response.context)
        self.assertIn("file_form", response.context)

    def test_help_texts(self):
        response = self.client.get(reverse("feedback:feedback"))
        form = response.context.get("form")
        info_form = response.context.get("info_form")
        text_ht = form.fields["text"].help_text
        mail_ht = info_form.fields["mail"].help_text
        self.assertEqual(text_ht, self.base_form.fields["text"].help_text)
        self.assertEqual(mail_ht, self.base_info_form.fields["mail"].help_text)

    def test_labels(self):
        response = self.client.get(reverse("feedback:feedback"))
        form = response.context.get("form")
        info_form = response.context.get("info_form")
        text_label = form.fields["text"].label
        mail_label = info_form.fields["mail"].label
        self.assertEqual(text_label, self.base_form.fields["text"].label)
        self.assertEqual(mail_label, self.base_info_form.fields["mail"].label)

    def test_redirects(self):
        form_data = {"text": "zxc", "mail": "zxc@ya.ru"}
        response = self.client.post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse("feedback:feedback"))

    def test_form_errors(self):
        form_data = {"text": "", "mail": "zxc"}
        response = self.client.post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertFormError(
            form=response.context.get("form"),
            field="text",
            errors="Обязательное поле.",
        )
        self.assertFormError(
            form=response.context.get("info_form"),
            field="mail",
            errors="Введите правильный адрес электронной почты.",
        )

    def test_form_valid(self):
        forms_count = Feedback.objects.count()
        form_data = {"text": "zxc", "mail": "zxc@ya.ru"}
        self.client.post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertEqual(Feedback.objects.count(), forms_count + 1)

    @override_settings(MEDIA_ROOT="temp")
    def test_upload_file(self):
        file_count = FeedbackFile.objects.count()
        file = SimpleUploadedFile("test_file.txt", b"file_content")
        response = self.client.post(
            reverse("feedback:feedback"),
            {"files": file, "text": "zxc", "mail": "zxc@ya.ru"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FeedbackFile.objects.count(), file_count + 1)
        shutil.rmtree("temp")


__all__ = []
