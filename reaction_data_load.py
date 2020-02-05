from matplotlib import pyplot as plt
from pickle_util import PickleUtil
import seaborn as sns
import numpy as np
from scipy import stats


data_file = "data/2001/rxn_times.p"
reaction_data = PickleUtil(data_file).safe_load()
reaction_data = np.array(reaction_data) * 1000
reaction_data = reaction_data[np.where(reaction_data < 2000)]

palette = sns.cubehelix_palette(2, start=-4.5, rot=2.4, dark=0.6, light=0.7, reverse=True)
sns.set_palette(palette)
sns.distplot(reaction_data, kde=False, fit=stats.exponnorm, label="High SRT")

mean = np.mean(reaction_data)
plt.axvline(mean, color="steelblue", label="High Mean SRT ("+str(int(mean))+"ms)")

data_file = "data/0/rxn_times.p"
reaction_data = PickleUtil(data_file).safe_load()
reaction_data = np.array(reaction_data) * 1000
reaction_data = reaction_data[np.where(reaction_data < 2000)]

sns.distplot(reaction_data, kde=False, fit=stats.exponnorm, label="Not High")

mean = np.mean(reaction_data)
plt.axvline(mean, color="rosybrown", label="Not High Mean SRT ("+str(int(mean))+"ms)")

plt.legend()
plt.show()

