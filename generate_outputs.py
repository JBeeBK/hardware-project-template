import os

project = "Project_Name"
hw_dir = "00 - Hardware"
pcb_file = f"{hw_dir}/{project}.kicad_pcb"
sch_file = f"{hw_dir}/{project}.kicad_sch"
pcb_out = "03 - Output_PCB"
asm_out = "04 - Output_Assembly"
docs_out = "01 - Docs"

os.makedirs(pcb_out, exist_ok=True)
os.makedirs(asm_out, exist_ok=True)
os.makedirs(docs_out, exist_ok=True)

os.system(f'kicad-cli pcb export gerbers "{pcb_file}" --output "{pcb_out}"')
os.system(f'kicad-cli pcb export drills "{pcb_file}" --output "{pcb_out}"')
os.system(f'kicad-cli pcb export pdf "{pcb_file}" -o "{pcb_out}/{project}_PCB_layers.pdf"')
os.system(f'kicad-cli sch export pdf "{sch_file}" -o "{docs_out}/{project}_schematic.pdf"')
os.system(f'kicad-cli sch export bom "{sch_file}" -o "{asm_out}/{project}_BOM.csv"')
os.system(f'kicad-cli pcb export pos "{pcb_file}" -o "{asm_out}/{project}_CPL.csv"')

print("All outputs generated and sorted!")
