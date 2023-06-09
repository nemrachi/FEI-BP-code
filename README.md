# FEI STU bachelor thesis: mocap-python
Python BVH data parser and render for Axis Studio of Noitom Perception Neuron 3 motion capture suit

### Instal libraries
`pip install -r requirements.txt`

### Start
`py bvhrender.py` = expects live data from Axis Studio

`py bvhrender.py --bvh=./resources/zdvihnutie_p_ruky_chr01.bvh`

### Structure of project:
- `docs/` = MocapApi SDK official documentation and files from analysis
- `mocap_api_example/` = MocapApi SDK python package by cachtayl-peeldev and some demo scripts
    - `mocap_api/` = MocapApi SDK python package by cachtayl-peeldev
        - `__pycache__/` = created when mocap_api.py is imported and run
        - `__init__.py` = required part of packages (imports functions from mocap_api.py)
        - `mocap_api.py` = MocapApi SDK python rework (used ctypes)
    - `windows/` = MocapApi SDK .dll
    - `pn3.py` = MocapApi playground
    - `remote_record.py` = MocapApi demo
    - `send_data.py` = Axis Studio playground
- `.gitignorr` = ignored files for git
- `basic_hierarchy.bvh` = BVH hierarchy, when live motion data is used (in live data no hierarchy is provided)
- `bvhrender.py` = script for parsing and rendering data
- `live_data.txt` = captured mocap data for analysis purposes
- `README.md` = readme

## TODO
- **LIVE PROCESSING** + bonus: Axis Studio on another pc
- ~~add package (project) to PyPI (pyproject.toml, run python -m pip install .) (save project as library/module?)~~

### Source links:
- [MocapApi official repo](https://github.com/pnmocap/MocapApi)
  - [MocapApi official? python repo](https://github.com/cachtayl-peeldev/MocapApi)
- [NEURON MOCAP LIVE Plugin for C4D official repo](https://github.com/pnmocap/neuron_mocap_live-c4d)
- [BVH format explained](https://www.cs.cityu.edu.hk/~howard/Teaching/CS4185-5185-2007-SemA/Group12/BVH.html)
- [Perception Neuron docs](https://support.neuronmocap.com/hc/en-us)

<!-- black - autoformatting code -->
<!-- pylint - linter -->
<!-- invoke -> @task clean -> invoke clean (kind of maven/gradle) -->