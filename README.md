# Actiwatch 

Actiwatch is a Python module built for interacting with files from [Philips Actiwatch actigraphy devices](https://www.usa.philips.com/healthcare/product/HC1044809/actiwatch-2-activity-monitor).

Philips Actiwatches are wrist-worn accelerometers/luxometers that allow clinicians and researchers to track activity, light-exposure, and sleep-patterns of their patients.

## Table of Contents

- [Getting Started](#getting-started)
- [Usage](#usage)
- [Development](#development)
- [Credits](#credits)
- [License](#license)

## Getting Started

```$ pip install actiwatch```

### Prerequisites

Currently requires Python 3.6 with `pipenv` installed.

## Usage

```python
>>> import actiwatch
>>> watch = actiwatch.Actiwatch(path="/path/to/file/.../example.csv",
                                start_time=16,
                                sleep_threshold=40,
                                manually_scored=False)
>>> watch
<Actiwatch [A12345]>
>>> watch.header
{'watch_ID': 'A12345', 'patient_sex': 'Male', ..., 'threshold_light': 1000.0}
>>> watch.patient_id
'A12345'

>>> watch.sleep_metrics
     Split_Day Interval  Sleep  Wake  TST_Min  WASO_Min         SE  watch_ID
0            1     Rest    132    59    264.0     118.0  69.109948  A12345
1            2     Rest    135    23    270.0      46.0  85.443038  A12345
2            3     Rest    143    48    286.0      96.0  74.869110  A12345
...        ...      ...    ...   ...      ...       ...        ...  ...

>>> watch.sleep_latency
    Split_Day  Sleep_Latency_Min  Wake_Latency_Min  watch_ID
0           1               42.0              38.0  A12345
1           2               24.0              80.0  A12345
2           3               44.0              38.0  A12345
...       ...                ...               ...  ...

>>> watch.bedtime
    Split_Day                Rest           Waking_Up   Time_Bed  Time_Wake  watch_ID
0           0                 NaT                 NaT        NaN        NaN  A12345
1           1 2018-02-16 01:36:00 2018-02-16 07:58:00   1.600000   7.966667  A12345
2           2 2018-02-17 01:48:00 2018-02-17 07:04:00   1.800000   7.066667  A12345
...       ...                 ...                 ...        ...        ...  ...

>>> watch.relative_amplitude
    Split_Day        RA  watch_ID
0           0       NaN  A12345
1           1  0.896660  A12345
2           2  0.852598  A12345
...       ...       ...  ...

>>> watch.total_values
    Split_Day  Activity      Light  watch_ID
0           0     97430    1591.58  A12345
1           1    186100    2077.75  A12345
2           2    112832    1364.61  A12345
...       ...       ...        ...  ...
```

## Development

### Contributing

Please checkout a development branch for whatever features you want to work on.

### Running Tests

#### Functional Tests

`make dev-tests`

#### Style Tests

`make dev-format`

### Versioning

Our group uses [Semantic Versioning](http://semver.org/) for versioning.

## Credits

### Authors

- **Ryan Opel**

## License

This project is licensed under the GNU General Public License v2.0 - see [LICENSE](LICENSE) for details.