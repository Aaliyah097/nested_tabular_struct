# nested_tabular_struct
Nested and tabular struct of flat data with margins

Use case: flexible data retrieve and display in reporting forms

Dependencies (min):
- python 3.6
- pprint
- typing.Iterable

Features:
- define data scheme: aggregate columns and margin columns
- define margin types: count, sum, mean
- represent data: as nested struct, as tabular matrix

Properties:
- polynomial time complexity O(NlogN)
- default data structures 

Example:
```python
# Input data, flat view
data = [
    {"wagon": 1, "road": 'A', "client": "C1", "station": "st1", "revenue": 10, "days": 1},
    {"wagon": 1, "road": 'B', "client": "C1", "station": "st1", "revenue": 20, "days": 7},
    {"wagon": 2, "road": 'C', "client": "C2", "station": "st2", "revenue": 30, "days": 14},
    {"wagon": 2, "road": 'A', "client": "C3", "station": "st2", "revenue": 40, "days": 3},
    {"wagon": 3, "road": 'C', "client": "C4", "station": "st4", "revenue": 50, "days": 1},
    {"wagon": 4, "road": 'B', "client": "C4", "station": "st5", "revenue": 60, "days": 7},
    {"wagon": 4, "road": 'D', "client": "C4", "station": "st3", "revenue": 70, "days": 5},
    {"wagon": 4, "road": 'A', "client": "C2", "station": "st3", "revenue": 80, "days": 3},
    {"wagon": 4, "road": 'A', "client": "C2", "station": "st3", "revenue": 85, "days": 14},
    {"wagon": 5, "road": 'A', "client": "C1", "station": "st2", "revenue": 90, "days": 21},
    {"wagon": 6, "road": 'A', "client": "C1", "station": "st4", "revenue": 95, "days": 1},
]

# Result scheme
keys = ["road", "client", "station"]
margins = {
    "wagon": "count",
    "revenue': "sum",
    "days": "mean"
}

# Presenter instance
presenter = Presenter(data=data, keys=keys, values=margins)

# Result data, nested view
nested = presenter.nested()

"""
Output (like folders in directory):

{
    'A': {
        'C1': {
            'days': [1, 21, 1],
            'revenue': 195,
            'wagon': 3,
            'st1': {'days': [1], 'revenue': 10, 'wagon': 1},
            'st2': {'days': [21], 'revenue': 90, 'wagon': 1},
            'st4': {'days': [1], 'revenue': 95, 'wagon': 1}
        },
        'C2': {
            'days': [3, 14],
            'revenue': 165,
            'wagon': 2,
            'st3': {'days': [3, 14], 'revenue': 165, 'wagon': 2}
        },
        'C3': {
            'days': [3],
            'revenue': 40,
            'wagon': 1
            'st2': {'days': [3], 'revenue': 40, 'wagon': 1}
        },
        'days': [1, 3, 3, 14, 21, 1],
        'revenue': 400,
        'wagon': 6
    },
    'B': {
        'C1': {
            'days': [7],
            'revenue': 20,
            'wagon': 1,
            'st1': {'days': [7], 'revenue': 20, 'wagon': 1}
        },
        'C4': {
            'days': [7],
            'revenue': 60,
            'wagon': 1,
            'st5': {'days': [7], 'revenue': 60, 'wagon': 1}
        },
        'days': [7, 7],
        'revenue': 80,
        'wagon': 2
    },
    'C': {
        'C2': {
            'days': [14],
            'revenue': 30,
            'wagon': 1,
            'st2': {'days': [14], 'revenue': 30, 'wagon': 1}
        },
        'C4': {
            'days': [1],
            'revenue': 50,
            'wagon': 1,
            'st4': {'days': [1], 'revenue': 50, 'wagon': 1}
        },
        'days': [14, 1],
        'revenue': 80,
        'wagon': 2
    },
    'D': {
        'C4': {
            'days': [5],
            'revenue': 70,
            'wagon': 1,
            'st3': {'days': [5], 'revenue': 70, 'wagon': 1}
        },
        'days': [5],
        'revenue': 70,
        'wagon': 1
    },
    'days': [1, 7, 14, 3, 1, 7, 5, 3, 14, 21, 1],
    'revenue': 630,
    'wagon': 11
}
"""

# Result data, tabular view
matrix = presenter.matrix(nested)

"""
Output (all arrays have the same length):

['D', 'C4', 'st3', 1, 70, [5]]
['D', 'C4', None, 1, 70, [5]]
['D', None, None, 1, 70, [5]]
['C', 'C4', 'st4', 1, 50, [1]]
['C', 'C4', None, 1, 50, [1]]
['C', 'C2', 'st2', 1, 30, [14]]
['C', 'C2', None, 1, 30, [14]]
['C', None, None, 2, 80, [14, 1]]
['B', 'C4', 'st5', 1, 60, [7]]
['B', 'C4', None, 1, 60, [7]]
['B', 'C1', 'st1', 1, 20, [7]]
['B', 'C1', None, 1, 20, [7]]
['B', None, None, 2, 80, [7, 7]]
['A', 'C3', 'st2', 1, 40, [3]]
['A', 'C3', None, 1, 40, [3]]
['A', 'C2', 'st3', 2, 165, [3, 14]]
['A', 'C2', None, 2, 165, [3, 14]]
['A', 'C1', 'st4', 1, 95, [1]]
['A', 'C1', 'st2', 1, 90, [21]]
['A', 'C1', 'st1', 1, 10, [1]]
['A', 'C1', None, 3, 195, [1, 21, 1]]
['A', None, None, 6, 400, [1, 3, 3, 14, 21, 1]]
[None, None, None, 11, 630, [1, 7, 14, 3, 1, 7, 5, 3, 14, 21, 1]]
"""
```

Drawbacks:
- ordering in views
- mean margin as array
