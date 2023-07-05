from typing import Iterable
import pprint


class Presenter:
    def __init__(self, data: list[dict], keys: list[str], values: dict[str, str]):
        self.data = data
        self.keys = keys
        self.values = values
        self.columns = keys + [k for k in values]
        self.columns_length = len(self.columns)
        self.pp = pprint.PrettyPrinter()

    def _down_went(self, d: dict, path: list[str]) -> dict:
        local_d = d

        for idx, p in enumerate(path):
            if p not in local_d:
                local_d[p] = {}
                for key, value in self.values.items():
                    if key not in local_d:
                        local_d[key] = [] if value == 'mean' else 0
                    if key not in local_d[p]:
                        local_d[p][key] = [] if value == 'mean' else 0

            yield local_d
            local_d = local_d[p]

    def print(self, nested_data: dict) -> None:
        self.pp.pprint(nested_data)

    def nested(self) -> dict:
        result = {}

        for d in self.data:
            local_keys = [d[key] for key in self.keys]
            agr_key = local_keys[-1]

            levels = self._down_went(result, local_keys)
            for level in levels:
                for margin in self.values:
                    if self.values[margin] == 'sum':
                        value = d[margin] or 0
                    elif self.values[margin] == 'count':
                        value = 1
                    elif self.values[margin] == 'mean':
                        value = [d[margin]] or []
                    else:
                        continue

                    if agr_key in level:
                        level[agr_key][margin] += value

                    level[margin] += value

        return result

    def matrix(self, d: dict, path: list = None) -> list[list]:
        result = []
        for r in self._matrix(d, path):
            result.append(r)
        return sorted(
            result,
            key=lambda x: (x[-1] if x[-1] else 0, x[0] if x[0] else "")
        )

    def _matrix(self, d: dict, path: list = None) -> Iterable[list]:
        if not path:
            path = []

        memory = {}

        for key, value in d.items():
            if type(value) == dict:
                new_path = path + [key]
                for nested_value in self._matrix(value, new_path):
                    yield nested_value
            else:
                new_path = path
                path_hash = hash("".join(new_path))
                if path_hash in memory:
                    continue

                memory[path_hash] = None
                add_path = []
                for k, v in d.items():
                    if type(v) != dict:
                        add_path.append(v)

                new_path = new_path + add_path

                if len(new_path) != self.columns_length:
                    last_str_index = 0
                    for i in range(len(new_path)):
                        if type(new_path[i]) != str:
                            last_str_index = i - 1
                            break

                    for i in range(self.columns_length - len(new_path)):
                        new_path.insert(last_str_index + 1, None)

                yield new_path


if __name__ == '__main__':
    keys = ['road', 'client', 'station']
    margins = {
        'wagon': 'count',
        'revenue': 'sum',
    }

    data = [
        {'wagon': 1, 'road': 'A', 'client': "C1", 'revenue': 10, 'station': 'st1'},
        {'wagon': 1, 'road': 'B', 'client': "C1", 'revenue': 20, 'station': 'st1'},
        {'wagon': 2, 'road': 'C', 'client': "C2", 'revenue': 30, 'station': 'st2'},
        {'wagon': 2, 'road': 'A', 'client': "C3", 'revenue': 40, 'station': 'st2'},
        {'wagon': 3, 'road': 'C', 'client': "C4", 'revenue': 50, 'station': 'st4'},
        {'wagon': 4, 'road': 'B', 'client': "C4", 'revenue': 60, 'station': 'st5'},
        {'wagon': 4, 'road': 'D', 'client': "C4", 'revenue': 70, 'station': 'st3'},
        {'wagon': 4, 'road': 'A', 'client': "C2", 'revenue': 80, 'station': 'st3'},
        {'wagon': 5, 'road': 'A', 'client': "C1", 'revenue': 90, 'station': 'st2'},
        {'wagon': 6, 'road': 'A', 'client': "C1", 'revenue': 95, 'station': 'st4'},
    ]

    p = Presenter(data, keys, margins)
    nested = p.nested()
    p.print(nested)

    matrix = p.matrix(nested)
    for row in matrix:
        print(row)

