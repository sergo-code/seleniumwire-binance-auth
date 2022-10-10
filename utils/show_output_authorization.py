def show_data(data, tokens):
    if data['status']:
        for dictionary in [data, tokens]:
            del dictionary['status']
            for key, value in dictionary.items():
                print(f'{key}: {value}')
    else:
        print('POST запрос не прошел.')
        for key, value in tokens.items():
            print(f'{key}: {value}')