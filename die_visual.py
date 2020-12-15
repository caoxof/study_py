import pygal
from die import Die

#创建两个D6骰子
die_1 = Die()
die_2 = Die()
die_3 = Die(12)

results = []
for roll_num in range(1000):
    result = die_1.roll() + die_2.roll() + die_3.roll()
    results.append(result)
#print(results)
#分析结果
frequencies = []
values = []
max_result = die_1.num_sides + die_2.num_sides + die_3.num_sides
for value in range(2,max_result+1):
    frequency = results.count(value)
    frequencies.append(frequency)
    values.append(str(value))
print(frequencies)

#对结果进行可视化
hist = pygal.Bar()

hist.title = 'Result of roll three D6 1000 times'
hist.x_labels = values
hist.x_title = 'result'
hist.y_title = 'frequency of result'

hist.add('D6+D6+D12',frequencies)
hist.render_to_file('die_visual2.svg')