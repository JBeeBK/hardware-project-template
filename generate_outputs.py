import os
import glob

HW_DIR = "00_Hardware"
PCB_OUT = "03_Output_PCB"
ASM_OUT = "04_Output_Assembly"

# --- Auto-detect project files ---
pcb_files = glob.glob(f"{HW_DIR}/*.kicad_pcb")
sch_files = glob.glob(f"{HW_DIR}/*.kicad_sch")

if not pcb_files or not sch_files:
    print(f"ERROR: Could not find .kicad_pcb or .kicad_sch in {HW_DIR}")
    exit(1)

pcb_file = pcb_files[0]
sch_file = sch_files[0]
PROJECT = os.path.splitext(os.path.basename(pcb_file))[0]

# ---- CHECK FILES EXIST ----
if not (os.path.isfile(pcb_file) and os.path.isfile(sch_file)):
    print(f"ERROR: Could not find {pcb_file} or {sch_file}")
    exit(1)

# ---- CHECK OUTPUT FOLDERS EXIST ----
for folder in [PCB_OUT, ASM_OUT]:
    if not os.path.isdir(folder):
        print(f"ERROR: Output folder '{folder}' not found. Please create it.")
        exit(1)

# ---- GENERATE GERBERS (modern extensions) ----
#-------Assumes all of my PCBs are 4 layers ------
print("Exporting Gerbers...")
os.system(f'kicad-cli pcb export gerbers "{pcb_file}" --output "{PCB_OUT}" --no-protel-ext --layers F.Cu,In1.Cu,In2.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,F.Paste,B.Paste,Edge.Cuts')

# ---- GENERATE DRILL FILES ----
print("Exporting Drill files...")
os.system(f'kicad-cli pcb export drill "{pcb_file}" --output "{PCB_OUT}"')

# ---- PCB LAYERS PDF ----
print("Exporting PCB PDF...")
os.system(f'kicad-cli pcb export pdf "{pcb_file}" -o "{PCB_OUT}/{PROJECT}_PCB_layers.pdf" --layers F.Cu,In1.Cu,In2.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,F.Paste,B.Paste,Edge.Cuts')

# ---- PCB STEP EXPORT ----
print("Exporting Step File...")
os.system(f'kicad-cli pcb export step "{pcb_file}" -o "{ASM_OUT}/{PROJECT}_3D.step"')

# ---- SCHEMATIC PDF ----
print("Exporting schematic PDF...")
os.system(f'kicad-cli sch export pdf "{sch_file}" -o "{PCB_OUT}/{PROJECT}_schematic.pdf"')

# ---- BOM ----
print("Exporting Grouped BOM...")
os.system(f'kicad-cli sch export bom "{sch_file}" -o "{ASM_OUT}/{PROJECT}_BOM_grouped.csv" --fields Reference,Value,Description,Footprint,Datasheet,Mfr1,MPN1,Mfr2,MPN2 --group-by Value,Footprint')

print("Exporting UngroupedBOM...")
os.system(f'kicad-cli sch export bom "{sch_file}" -o "{ASM_OUT}/{PROJECT}_BOM_ungrouped.csv" --fields Reference,Value,Description,Footprint,Datasheet,Mfr1,MPN1,Mfr2,MPN2')

# ---- PICK AND PLACE (CPL) ----
print("Exporting Pick & Place (CPL)...")
os.system(f'kicad-cli pcb export pos "{pcb_file}" -o "{ASM_OUT}/{PROJECT}_CPL.csv"')

print("\nAll outputs generated and sorted!")

# ---- OPTIONAL: OPEN OUTPUT FOLDER (uncomment for Windows) ----
# os.system(f'start "" "{os.path.abspath(PCB_OUT)}"')