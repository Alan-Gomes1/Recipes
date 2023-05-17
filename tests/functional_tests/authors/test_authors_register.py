from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


class AuthorsRegisterTest(AuthorsBaseTest):
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder}"]'
            )

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 10)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email')
        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Ex.: John')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('Write your first name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Ex.: Doe')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('Write your last name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, 'Your username')
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('This field is required', form.text)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'Your e-mail')
            email_field.send_keys(' ')
            email_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Informe um endereço de email válido.', form.text)
        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match_error_message(self):
        def callback(form):
            password = self.get_by_placeholder(form, 'Type your password here')
            password2 = self.get_by_placeholder(form, 'Repeat your password')
            password.send_keys('P@ssw0rd')
            password2.send_keys('P@ssw0rd_different')
            password2.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn(
                'Password and confirm password must be equal', form.text
            )
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_placeholder(form, 'Ex.: John').send_keys('John')
        self.get_by_placeholder(form, 'Ex.: Doe').send_keys('Doe')
        self.get_by_placeholder(form, 'Your username').send_keys('JohnDoe')
        self.get_by_placeholder(
            form, 'Your e-mail').send_keys('dummy@email.com')
        self.get_by_placeholder(
            form, 'Type your password here').send_keys('P@ssw0rd')
        self.get_by_placeholder(
            form, 'Repeat your password').send_keys('P@ssw0rd')
        form.submit()

        self.assertIn(
            'Your user is created, please log in.',
            self.browser.find_element(By.TAG_NAME, 'body').text)
