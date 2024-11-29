import numpy as np

def gradient_descent(f, df, initial_guess, learning_rate, max_iterations):
    # Initialize variables
    x = initial_guess
    loss = None
    
    # Iterate until the convergence condition is met
    for _ in range(max_iterations):
        # Calculate the gradient of the function at the current point
        grad = df(x)
        
        # Update the current point based on the gradient and learning rate
        x -= learning_rate * grad
        
        # Check if the loss has improved, which means we are close to a minimum
        if loss is None or np.abs(loss - last_loss) < 1e-6:
            break
        
        # Store the current point
        last_loss = loss
    
    return x

# Example function and its derivative
def example_function(x):
    """
    This function takes a single argument x and returns the square of x plus two times x plus three.
    
    Parameters:
    - x (float): The input value to compute the square of.
    
    Returns:
    - float: The computed result.
    """
    return x**2 + 2*x + 3

def example_derivative(x):
    """
    This function takes a single argument x and returns the derivative of the function
    'example_function'.
    
    Parameters:
    - x (float): The input value to compute the derivative with respect to.
    
    Returns:
    - float: The computed derivative.
    """
    return 2*x + 2

# Example usage
x = 5.0
result_square = example_function(x)
print(f"The square of {x} is {result_square}")

result_derivative = example_derivative(x)
print(f"The derivative of the function {example_function.__name__} at x={x} is {result_derivative}")

# Initial guess, learning rate, and maximum iterations
initial_guess = 0.01
learning_rate = 0.01
max_iterations = 1000

# Calculate the solution using gradient descent
solution = gradient_descent(example_function, example_derivative, initial_guess, learning_rate, max_iterations)
print("The solution is:", solution)

# Plotting the function to verify convergence
import matplotlib.pyplot as plt
x_values = np.linspace(-5, 5, 1000)
y_values = [example_function(x) for x in x_values]

plt.plot(x_values, y_values)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Gradient Descent Solution')
# Adding a legend to the plot
plt.legend()
plt.show()
