
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

print("===== ANOVA INTERACTIVE SYSTEM =====")

# Step 1: Ask number of groups
num_groups = int(input("Enter number of groups: "))

groups = []
names = []

# Step 2: Take input for each group
for i in range(num_groups):
    name = input(f"Enter name of group {i+1}: ")
    names.append(name)
    
    values = list(map(float, input(f"Enter values for {name} (space-separated): ").split()))
    groups.append(values)

# Step 3: Perform ANOVA
f_stat, p_value = stats.f_oneway(*groups)

# Step 4: Print results
print("\n===== ANOVA RESULT =====")
print("F-value:", f_stat)
print("P-value:", p_value)

# Step 5: Decision logic
if p_value < 0.05:
    print("Conclusion: Significant difference exists (Reject H0)")
else:
    print("Conclusion: No significant difference (Accept H0)")

# Step 6: Mean values
print("\n===== MEAN VALUES =====")
means = []
for i, group in enumerate(groups):
    mean_val = np.mean(group)
    means.append(mean_val)
    print(f"Mean {names[i]}:", mean_val)

# Step 7: Box Plot
plt.boxplot(groups)
plt.xticks(range(1, num_groups + 1), names)
plt.title("ANOVA Comparison (Box Plot)")
plt.xlabel("Groups")
plt.ylabel("Values")
plt.show()

# Step 8: Bar Graph (Mean comparison)
plt.bar(names, means)
plt.title("Mean Comparison")
plt.xlabel("Groups")
plt.ylabel("Mean Value")
plt.show()

print("\n===== THANK YOU =====")