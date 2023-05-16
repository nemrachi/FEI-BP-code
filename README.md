# FEI STU bachelor thesis: mocap-python
Python data processor for Axis Studio of NOITOM Perception Neuron 3 motion capture suit

### Start
run mocap_api/mocap_api.py

### Structure of project:
- `docs/` = MocapApi SDK official documentation
- `mocap_api/` = MocapApi SDK python package by cachtayl-peeldev
    - `__pycache__/` = created when mocap_api.py is imported and run
    - `__init__.py` = required part of packages (imports functions from mocap_api.py)
    - `mocap_api.py` = MocapApi SDK python rework (used ctypes)
- `windows/` = MocapApi SDK .dll
- `captured_data.txt` = captured mocap data
- `pn3.py` = playground
- `remote_record.py` = testing?



## TODO
- **DRAW DATA** with something
- **LIVE PROCESSING** + bonus: server without Axis Studio
- **popisat projekt ako SWI projekt (schema poprepajania, viac technicky popis)**
- porovnat nejake kniznice na bvh spracovanie/vykreslovanie (ak nepojde live processing)
- print gestures in console + to file?
- ~~add package (project) to PyPI (pyproject.toml, run python -m pip install .) (save project as library/module?)~~

### Source/repository links:
- [MocapApi official repo](https://github.com/pnmocap/MocapApi)
  - [MocapApi official? python repo](https://github.com/cachtayl-peeldev/MocapApi)
- [NEURON MOCAP LIVE Plugin for C4D official repo](https://github.com/pnmocap/neuron_mocap_live-c4d)
- [BVH format explained](https://www.cs.cityu.edu.hk/~howard/Teaching/CS4185-5185-2007-SemA/Group12/BVH.html)
- [Perception Neuron docs](https://support.neuronmocap.com/hc/en-us)

<!-- black - autoformatting code -->
<!-- pylint - linter -->
<!-- invoke -> @task clean -> invoke clean (kind of maven/gradle) -->