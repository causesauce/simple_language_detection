def translate_and_categorize(f, language):
    parts = list()
    for i in f:
        a = str(i, 'utf-8')
        parts.append(''.join(j for j in a if 64 < ord(j) < 91 or 96 < ord(j) < 123).lower())

    result = [''.join(parts), language]
    return result


def convert_from_letters_to_frequencies(dataset):
    dataset_converted = list()
    for i in dataset:
        label = i[1]
        data = find_freq(i[0])
        dataset_converted.append([data, label])
    return dataset_converted


def find_freq(data_string):
    letters_dict = dict()
    for j in range(97, 123):
        letters_dict[chr(j)] = 0
    for j in data_string:
        letters_dict[j] += 1
    text_len = len(data_string)
    values = [j / text_len for j in letters_dict.values()]
    return values


def key_value(val, dictionary):
    for key in dictionary.keys():
        if dictionary[key] == val:
            return key
    return -1


class Perceptron:

    def __init__(self, epochs, label):
        self.epochs = epochs
        self.alpha = 0.001
        self.weights = [0.0 for _ in range(0, 26)]
        self.label = label
        self.threshold = 0.0

    def train(self, dataset, label):
        dot = 0.0
        for i in range(len(dataset)):
            dot += self.weights[i] * dataset[i]
        predicted = dot - self.threshold
        actual = 0.0
        # if the label of the chunk is the same as for the perceptron then actual is 1
        if label == self.label:
            actual = 1.0
        # calculating error
        error = actual - predicted
        # updating weights
        for i in range(len(dataset)):
            self.weights[i] = self.weights[i] + dataset[i] * self.alpha * error
        # normalizing weights
        weights_sum = sum(self.weights)
        if weights_sum == 0.0:
            weights_sum = 1.0
        for i in range(len(self.weights)):
            self.weights[i] = self.weights[i] / weights_sum
        # updating threshold
        self.threshold = self.threshold - self.alpha * error

    def test(self, dataset):
        dot = 0
        for j in range(len(dataset)):
            dot += self.weights[j] * dataset[j]
        return dot - self.threshold, self.label

    def train_perceptron(self, source):
        for i in range(self.epochs):
            for j in source:
                train_data_row = j[0]
                label = j[1]
                self.train(train_data_row, label)


def test_from_file(test_path, neurons, language_label):
    f = open(test_path, 'rb')
    # list of letters
    test_data = translate_and_categorize(f, language_label)
    # frequencies and label separated
    test_data, label = find_freq(test_data[0]), test_data[1]

    result = list()

    for n in neurons:
        result.append(n.test(test_data))

    maximum = 0
    text = ''
    for i in result:
        print(f'{i[1]}: probability is {round(i[0] * 100, 2)}%')
        if i[0] > maximum:
            maximum = i[0]
            text = i[1]

    print(f'the language is "{text}"')
    print(f'actual language is "{label}"')

    f.close()
