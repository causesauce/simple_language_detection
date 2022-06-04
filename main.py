import os

from Perceptron import *

while True:
    users_choice = input('if you want to test your text type down 1, otherwise 0, anything else to exit: ')
    if users_choice != '0' and users_choice != '1':
        break
    print('wait please')
    print('***reading and formatting data***')

    # block for dataset creation

    nn = list()
    train_data = list()
    train_path = 'train/'
    folders = os.listdir(train_path)
    # loop for creating dataset and instances of a neuron for every language
    for i in folders:
        language_folder = os.listdir(train_path + i + '/')
        p = Perceptron(8000, i)
        nn.append(p)
        for j in language_folder:
            source = train_path + i + '/' + j
            f = open(source, 'rb')
            language_label = i
            train_data.append(translate_and_categorize(f, language_label))
            f.close()

    # block for training

    # converting from letters to the frequencies marked with their labels
    train_data = convert_from_letters_to_frequencies(train_data)
    # loop for training neurons
    print('***training***')
    for p in nn:
        p.train_perceptron(train_data)

    # block for testing

    if users_choice == '0':
        test_path = 'test/'
        folders = os.listdir(test_path)
        # loop to test and print all the test data
        for i in folders:
            language_folder = os.listdir(test_path + i + '/')
            for j in language_folder:
                source = test_path + i + '/' + j
                language_label = i
                test_from_file(source, nn, language_label)
            print('---------------------')
    else:
        test_path = 'test_manually/text_test.txt'
        data_raw = input('your data: ')
        print(data_raw)
        actual_language_label = input('actual language: ')
        f = open(test_path, encoding='utf-8', mode='w+')
        f.write(data_raw)
        f.close()
        test_from_file(test_path, nn, actual_language_label)
        input()
