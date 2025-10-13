def apply_user_template(template: str, username):
    if not template:
        return None

    template = template.replace("{name}", username)
    return template