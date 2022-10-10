import re


def change_env_config(tokens):
    config = []
    with open(".env", "r") as file:
        for line in file:
            if 'P20T' in line:
                line = re.sub(r"P20T=web.\d+\.\w+", f'P20T={tokens["p20t_token"]}', line)
            elif 'CSRF' in line:
                line = re.sub(r"CSRF=\w+", f'CSRF={tokens["csrf_token"]}', line)
            config.append(line)

    with open(".env", "w") as file:
        for line in config:
            file.writelines(line)