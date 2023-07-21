
import re 
import matplotlib.pyplot as plt



def extract(filename, attack):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                lines.append(line)
    float_regex = r"\d+\.\d+"
    floats = []
    for line in lines:
        matches = re.findall(float_regex, line) 
        for match in matches:
            try:
                floats.append(float(match))
            except ValueError:
                pass


    plt.plot(range(len(floats)), floats)
    plt.xlabel('La durée d\'exécution d\'une batch')
    plt.ylabel('durée en second')
    plt.title(attack)
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    #extract('LLC_data.txt', 'LLC_attack')
    #extract('LOCKING_data.txt', 'atomic locking attack')
    extract('ML_DATA.txt', 'model training on MNIST data')
    extract('LLC_ML.txt', 'model training on MNIST data')
