from mail import Mailer


def main():
    mailer = Mailer()
    data = {
        "my_string": "Wheee!",
        "my_list": [0, 1, 2, 3]
    }
    rendered = mailer.render_template('templates/demo.html', data)
    mailer.send_mail('a@b.com', 'test', rendered)
    print("Email Sent")


if __name__ == '__main__':
    main()
