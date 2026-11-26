"""Regenerates Bulletin of Volcanology 2024 Fig. 2 as SVG from the Iceland 2023 expedition notebook.

Runs the notebook's setup cells from ~/dev/iceland-2023-expedition, draws the day 2 outbound
transect with the published styling (no title, plain "Gaussian fit" legend label), and saves it
to images/publications/bullvolc-2024-fig2.svg.

Usage: python3 scripts/build_bullvolc_fig2.py
"""
import json
import os
import sys

notebook_dir = os.path.expanduser("~/dev/iceland-2023-expedition")
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images", "publications", "bullvolc-2024-fig2.svg")
os.chdir(notebook_dir)
sys.path.insert(0, notebook_dir)
import matplotlib
matplotlib.use("svg")

notebook = json.load(open("Iceland July 2023.ipynb"))
namespace = {"__name__": "__notebook__"}
for cell in notebook["cells"][:9]:
    if cell["cell_type"] != "code":
        continue
    source = "\n".join(line for line in "".join(cell["source"]).splitlines() if not line.lstrip().startswith(("%", "!")))
    exec(compile(source, "notebook", "exec"), namespace)

plt = namespace["plt"]
plt.rcParams["svg.fonttype"] = "path"
figure, axes = plt.subplots(1, 1, figsize=(7.2, 4.2))
data = namespace["day2_flight1a"]
namespace["render_distance_data"](data[0], data, 410, "Day 2 Transect out", axes,
                                  min_distance=250, limit_distance=700, max_co2=1000, legend=True, angle=namespace["math"].pi / 4)
axes.set_title("")
handles, labels = axes.get_legend_handles_labels()
labels = ["Gaussian fit" if label.startswith("Gaussian fit") else label for label in labels]
axes.legend(handles, labels, fontsize="small")
figure.savefig(output_path, format="svg", bbox_inches="tight")
print("ok")
