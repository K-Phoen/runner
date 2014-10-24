runner
======

Set of tools to work with .FIT, .TCX and .GPX files.

## Installation

```
python setup.py install
```

## Usage

### runner-convert

Easily convert a file from a format to another.

```
runner-convert -i ~/2014-10-21_08-52-05_4_47.fit -o activity.tcx
```

### runner-edit

Edit a given activity.

Only time edition is currently supported.

```
runner-edit time -i activity.tcx -o activity_edited.tcx --time='+2hour'
```

### runner-merge

Merge the heart rate data from a file into another activity.

```
runner-merge -m main_activity.tcx -c cardio_activity.tcx -o merged.tcx
```

## License

This project is released under the MIT License. See the bundled LICENSE file for
details.
