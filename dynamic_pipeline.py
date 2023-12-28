from prettytable import PrettyTable


class Task:
    def __init__(self, node_id, time):
        self.id = node_id
        self.children = []
        self.time = time


class DynamicPipeline:
    def __init__(self, layers_number):
        self.execution_times = {"+": 1, "-": 2, "*": 3, "/": 4}
        self.tasks = []
        self.layers_number = layers_number
        self.layers = [[] for _ in range(layers_number)]
        self.read = []
        self.write = []

    def convert_tree_to_tasks(self, node, parent=None, level=0):
        if node.id is not None:
            task = Task(node.id, self.get_execution_time(node))
            if len(self.tasks) > level:
                self.tasks[level].append(task)
            else:
                self.tasks.append([task])
            if parent is not None:
                parent.children.append(node.id)
            current = level + 1
            for child in node.children:
                self.convert_tree_to_tasks(child, task, current)

    def print(self):
        read_column = self.read.copy()
        for i in range(len(read_column)):
            if read_column[i] != "":
                read_column[i] = f"{read_column[i]}=>"
        read_column.extend([""] * max(0, len(self.write) - len(read_column)))
        table = PrettyTable()
        table.add_column("T", range(1, len(self.write) + 1))
        table.add_column("Read", read_column)
        for layer in self.layers:
            layer_column = layer.copy()
            for i in range(len(layer_column)):
                if layer_column[i] != "":
                    layer_column[i] = f"[{layer_column[i]}]"
            layer_column.extend([""] * max(0, len(self.write) - len(layer_column)))
            table.add_column(f"S{self.layers.index(layer) + 1}", layer_column)
        write_column = self.write.copy()
        for i in range(len(write_column)):
            if write_column[i] != "":
                write_column[i] = f"=>{write_column[i]}"
        table.add_column("Write", write_column)
        print(table)
        execution_time, acceleration_coefficient, efficiency_coefficient = self.get_statistics()
        print(f"Час виконання: {round(execution_time, 2)}")
        print(f"Коефіцієнт прискорення: {round(acceleration_coefficient, 2)}")
        print(f"Коефіцієнт ефективності: {round(efficiency_coefficient, 2)}")

    def immerse(self, node):
        self.convert_tree_to_tasks(node)
        tasks = [t for r in reversed(self.tasks) for t in r]
        self.add_task(tasks[0], 1)
        prev = tasks[0].id
        for task in tasks[1:]:
            possible_indices = [layer.index(prev) for layer in self.layers[1:]]
            if len(task.children) > 0:
                for child in task.children:
                    possible_indices = [i for i in possible_indices if i > self.write.index(child)]
                    if len(possible_indices) == 0:
                        possible_indices = [self.write.index(child) + 2]
            self.add_task(task, min(possible_indices))
            prev = task.id

    def add_task(self, task, index):
        self.read.extend([""] * max(0, index - len(self.read) + 1))
        self.read[index - 1] = task.id
        temp_index = index - 1
        for n in range(len(self.layers)):
            for m in range(task.time):
                temp_index += 1
                if n != len(self.layers) - 1 and m == 0:
                    for j in range(len(self.layers) - n):
                        while len(self.layers[n + j]) > temp_index and self.layers[n + j][temp_index] != "" and self.layers[n + j].index(self.layers[n + j][temp_index]) != temp_index:
                            temp_index += 1
                if len(self.layers[n]) > temp_index:
                    temp_index = len(self.layers[n])
                    self.layers[n].append(task.id)
                else:
                    self.layers[n].extend([""] * max(0, temp_index - len(self.layers[n]) + 1))
                    self.layers[n][temp_index] = task.id
                if n != len(self.layers) - 1 and m != 0:
                    for j in range(len(self.layers) - n):
                        if len(self.layers[n + j]) > temp_index and self.layers[n + j].index(self.layers[n + j][temp_index]) == temp_index:
                            value = self.layers[n + j][temp_index]
                            insert_number = task.time - m
                            while len(self.layers[n + j - 1]) > temp_index + insert_number and self.layers[n + j - 1][temp_index + insert_number] == value:
                                insert_number += task.time
                            for _ in range(insert_number):
                                self.layers[n + j].insert(temp_index, "")
                            if n + j == len(self.layers) - 1:
                                if value in self.write:
                                    self.write[self.write.index(value)] = ""
                                write_index = len(self.layers[n + j]) - self.layers[n + j][::-1].index(value)
                                self.write.extend([""] * max(0, write_index - len(self.write) + 1))
                                self.write[write_index] = value
        temp_index += 1
        self.write.extend([""] * max(0, temp_index - len(self.write) + 1))
        self.write[temp_index] = task.id

    def get_execution_time(self, node):
        value = node.value

        if value in self.execution_times.keys():
            return self.execution_times[value]
        else:
            if not node.is_function:
                return 0

            print(f"Enter execution time for function {value}: ", end="")
            function_execution_time = int(input())
            self.execution_times[value] = function_execution_time
            return function_execution_time

    def get_statistics(self):
        execution_time = len(self.write)
        acceleration_coefficient = (sum(t.time for r in self.tasks for t in r) * 4 + 2) / execution_time
        efficiency_coefficient = acceleration_coefficient / self.layers_number
        return execution_time, acceleration_coefficient, efficiency_coefficient
