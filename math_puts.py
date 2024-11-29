import numpy as np

def gradient_descent(f, df, initial_guess, learning_rate, max_iterations):
    x = initial_guess
    loss = None

    for _ in range(max_iterations):
        grad = df(x)
        x -= learning_rate * grad

        if loss is None or np.abs(loss - last_loss) < 1e-6:
            break

        last_loss = loss

    return x

def example_function(x):
    return x**2 + 2*x + 3

def example_derivative(x):
    return 2*x + 2

x = 5.0
result_square = example_function(x)
print(f"The square of {x} is {result_square}")

result_derivative = example_derivative(x)
print(f"The derivative of the function {example_function.__name__} at x={x} is {result_derivative}")

initial_guess = 0.01
learning_rate = 0.01
max_iterations = 1000

solution = gradient_descent(example_function, example_derivative, initial_guess, learning_rate, max_iterations)
print("The solution is:", solution)

import matplotlib.pyplot as plt
x_values = np.linspace(-5, 5, 1000)
y_values = [example_function(x) for x in x_values]

plt.plot(x_values, y_values)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Gradient Descent Solution')
plt.legend()
plt.show()
