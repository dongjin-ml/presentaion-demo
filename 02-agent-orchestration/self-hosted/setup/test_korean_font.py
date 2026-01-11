import matplotlib.pyplot as plt
import numpy as np

# Generate data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create graph
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Sine function')
plt.plot(x, -y, label='-Sine function')
plt.title('Korean Font Test: Sine Function Graph')
plt.xlabel('x-axis label')
plt.ylabel('y-axis label')
plt.legend()
plt.grid(True)
plt.savefig('korean_font_test.png')
plt.show()

print("Test complete! Please check the korean_font_test.png file.")
