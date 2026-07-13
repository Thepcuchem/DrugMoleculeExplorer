import tkinter as tk
from tkinter import ttk
import pubchempy as pcp
import math
import json
import os
import ssl
import urllib.error
import urllib.request
from rdkit import Chem
from rdkit.Chem import Draw
from PIL import Image, ImageTk
from tkinter import filedialog
from rdkit.Chem import AllChem
from rdkit import DataStructs
from rdkit.Chem import Descriptors
from rdkit.Chem import Lipinski
from rdkit.Chem import rdMolDescriptors

root = tk.Tk()
root.title("Drug Molecule Explorer")
root.geometry("1280x760")
root.minsize(1120, 680)
root.configure(bg="#1e1e1e")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPLASH_IMAGE_PATH = os.path.join(BASE_DIR, "startup.png")

BG = "#1e1e1e"
CARD_BG = "#252526"
INPUT_BG = "#1b1b1c"
TEXT = "#d4d4d4"
MUTED = "#9da5b4"
ACCENT = "#007acc"
BORDER = "#3c3c3c"
PANEL_TITLE = "#c5d9f1"
FONT = ("Helvetica", 13)
TITLE_FONT = ("Helvetica", 24, "bold")
PANEL_FONT = ("Helvetica", 13, "bold")
SMALL_FONT = ("Helvetica", 11)

style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground=INPUT_BG, background="#333333", foreground=TEXT, arrowcolor=TEXT, selectbackground=INPUT_BG, selectforeground=TEXT, padding=8, font=FONT)
style.map("TCombobox", fieldbackground=[("readonly", INPUT_BG)], background=[("readonly", "#333333")], foreground=[("readonly", TEXT)])
style.configure("Vertical.TScrollbar", background="#333333", troughcolor="#1e1e1e", bordercolor=BORDER, arrowcolor=TEXT, relief="flat")
style.map("Vertical.TScrollbar", background=[("active", "#424242"), ("pressed", "#4d4d4d")])
style.configure("Treeview", background="#1f1f1f", fieldbackground="#1f1f1f", foreground=TEXT, rowheight=30, font=SMALL_FONT, borderwidth=0)
style.configure("Treeview.Heading", background="#2d2d30", foreground=PANEL_TITLE, font=("Helvetica", 11, "bold"), relief="flat")
style.map("Treeview", background=[("selected", "#094771")], foreground=[("selected", "#ffffff")])
style.configure("Modern.TButton", background=ACCENT, foreground="#ffffff", font=("Helvetica", 12, "bold"), padding=(16, 9), borderwidth=0)
style.map("Modern.TButton", background=[("active", "#118ad7"), ("pressed", "#005a9e")])
style.configure("Secondary.TButton", background="#3a3d41", foreground=TEXT, font=("Helvetica", 12, "bold"), padding=(16, 9), borderwidth=0)
style.map("Secondary.TButton", background=[("active", "#45494e"), ("pressed", "#2d2f33")])
style.configure("TNotebook", background=BG, borderwidth=0)
style.configure("TNotebook.Tab", background="#2d2d30", foreground=TEXT, padding=(18, 10), font=("Helvetica", 12, "bold"))
style.map("TNotebook.Tab", background=[("selected", CARD_BG), ("active", "#333333")], foreground=[("selected", PANEL_TITLE), ("active", "#ffffff")])
current_mol = None
view_3d_atoms = []
view_3d_bonds = []
rotation_angle = 0
rotation_job = None
view_3d_angle_x = 0
view_3d_angle_y = 0
view_3d_dragging = False
view_3d_last_x = 0
view_3d_last_y = 0
view_3d_zoom = 1.0
hero_rotation_angle = 0

ATOM_COLORS = {
	"C": "#d4d4d4",
	"H": "#858585",
	"N": "#569cd6",
	"O": "#f44747",
	"S": "#dcdcaa",
	"P": "#ce9178",
	"F": "#4ec9b0",
	"Cl": "#4ec9b0",
	"Br": "#c586c0",
	"I": "#c586c0",
}
splash_logo_image = None
about_image = None
splash_frame = tk.Frame(root, bg=BG)
splash_frame.pack(fill="both", expand=True)

def resize_splash_logo(image, max_width, max_height):
	width, height = image.size
	scale = min(max_width / width, max_height / height, 1)
	new_size = (int(width * scale), int(height * scale))
	return image.resize(new_size, Image.Resampling.LANCZOS)


def build_splash_screen():
	global splash_logo_image

	splash_canvas = tk.Canvas(splash_frame, bg=BG, highlightthickness=0)
	splash_canvas.pack(fill="both", expand=True)

	def place_splash_image(event=None):
		global splash_logo_image
		canvas_width = max(splash_canvas.winfo_width(), 1)
		canvas_height = max(splash_canvas.winfo_height(), 1)

		if os.path.exists(SPLASH_IMAGE_PATH):
			logo = Image.open(SPLASH_IMAGE_PATH).convert("RGBA")
			logo = resize_splash_logo(logo, canvas_width - 80, canvas_height - 80)
			splash_logo_image = ImageTk.PhotoImage(logo)
			splash_canvas.delete("all")
			splash_canvas.create_image(
				canvas_width // 2,
				canvas_height // 2,
				image=splash_logo_image,
				anchor="center",
			)
		else:
			splash_canvas.delete("all")
			splash_canvas.create_text(
				canvas_width // 2,
				canvas_height // 2 - 40,
				text="CHEM CHULA",
				fill=PANEL_TITLE,
				font=("Helvetica", 48, "bold"),
			)
			splash_canvas.create_text(
				canvas_width // 2,
				canvas_height // 2 + 20,
				text="Drug Molecule Explorer",
				fill=PANEL_TITLE,
				font=("Helvetica", 30, "bold"),
			)
			splash_canvas.create_text(
				canvas_width // 2,
				canvas_height // 2 + 70,
				text="Launching...",
				fill=MUTED,
				font=("Helvetica", 13),
			)

	# Place the splash image after the canvas has its size
	splash_canvas.bind("<Configure>", place_splash_image)

	# Force first placement if widget already has size
	root.after(10, place_splash_image)


def show_main_app():
	splash_frame.pack_forget()
	notebook.pack(fill="both", expand=True)


build_splash_screen()
notebook = ttk.Notebook(root)

explorer_tab = tk.Frame(notebook, bg=BG)
similar_tab = tk.Frame(notebook, bg=BG)
comparison_tab = tk.Frame(notebook, bg=BG)
about_tab = tk.Frame(notebook, bg=BG)
notebook.add(explorer_tab, text="Explorer")
notebook.add(similar_tab, text="Similar Molecules")
notebook.add(comparison_tab, text="Comparison")
notebook.add(about_tab, text="About")
notebook.hide(similar_tab)
notebook.hide(comparison_tab)
similar_tab_visible = False
comparison_tab_visible = False
comparison_models = {}
comparison_rotation_job = None

menu_bar = tk.Menu(root)
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=lambda: notebook.select(about_tab))
menu_bar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menu_bar)

about_canvas = tk.Canvas(about_tab, bg=BG, highlightthickness=0)
about_canvas.pack(fill="both", expand=True)

about_text = (
	"Drug Molecule Explorer\n" \
	"A desktop visualization and analysis tool for small-molecule structures.\n\n" \
	"Search PubChem, inspect 2D/3D structures, compare descriptors, and export results.\n\n" \
	"Created by the Center of Excellence in Computational Chemistry, Chulalongkorn University"
)

def place_about_graphic(event=None):
	global about_image
	canvas_width = max(about_canvas.winfo_width(), 1)
	canvas_height = max(about_canvas.winfo_height(), 1)
	if os.path.exists(SPLASH_IMAGE_PATH):
		logo = Image.open(SPLASH_IMAGE_PATH).convert("RGBA")
		logo = resize_splash_logo(logo, canvas_width - 80, int(canvas_height * 0.55))
		about_image = ImageTk.PhotoImage(logo)
		about_canvas.delete("all")
		about_canvas.create_image(
			canvas_width // 2,
			40,
			image=about_image,
			anchor="n",
		)
		about_canvas.create_text(
			canvas_width // 2,
			canvas_height - 100,
			text=about_text,
			fill=TEXT,
			font=FONT,
			justify="center",
			width=min(canvas_width - 80, 760),
		)

about_canvas.bind("<Configure>", place_about_graphic)
root.after(10, place_about_graphic)

canvas = tk.Canvas(explorer_tab, bg=BG, highlightthickness=0)
scrollbar = ttk.Scrollbar(explorer_tab, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=BG)
scrollable_frame.bind(
	"<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="n", width=1280)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind(
	"<Configure>", lambda e: canvas.itemconfigure(canvas_window, width=e.width)
)


def scroll_explorer_page(event):
	event_num = getattr(event, "num", None)
	event_delta = getattr(event, "delta", 0)
	active_canvas = canvas

	if "comparison_canvas" in globals() and notebook.select() == str(comparison_tab):
		active_canvas = comparison_canvas

	if event_num == 4 or event_delta > 0:
		active_canvas.yview_scroll(-1, "units")
	elif event_num == 5 or event_delta < 0:
		active_canvas.yview_scroll(1, "units")


def bind_explorer_scroll():
	canvas.bind_all("<MouseWheel>", scroll_explorer_page)
	canvas.bind_all("<Button-4>", scroll_explorer_page)
	canvas.bind_all("<Button-5>", scroll_explorer_page)


bind_explorer_scroll()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
title_frame = tk.Frame(scrollable_frame, bg=BG)
title_frame.grid(row=0, column=0, columnspan=3, pady=(22, 10), padx=24, sticky="ew")
intro_frame = tk.Frame(scrollable_frame, bg=BG)
intro_frame.grid(row=1, column=0, pady=(8, 4), padx=(24, 10), sticky="nsew")
center_intro = tk.Frame(scrollable_frame, bg=BG)
center_intro.grid(row=1, column=1, pady=(8, 4), padx=10, sticky="nsew")
right_intro = tk.Frame(scrollable_frame, bg=BG)
right_intro.grid(row=1, column=2, pady=(8, 4), padx=(10, 24), sticky="nsew")
search_frame = tk.LabelFrame(
	scrollable_frame,
	text="Search Panel",
	font=PANEL_FONT,
	bg=CARD_BG,
	fg=PANEL_TITLE,
	bd=1,
	relief="solid",
	padx=18,
	pady=16,
	highlightbackground=BORDER,
)
search_frame.grid(row=1, column=1, pady=(288, 22), padx=10, sticky="n")
structure_frame = tk.LabelFrame(
	scrollable_frame,
	text="2D Structure Panel",
	font=PANEL_FONT,
	bg=CARD_BG,
	fg=PANEL_TITLE,
	bd=1,
	relief="solid",
	padx=18,
	pady=16,
	highlightbackground=BORDER,
)
# structure_frame.pack(pady=10, padx=20)

descriptor_frame = tk.LabelFrame(
	scrollable_frame,
	text="Descriptor Table",
	font=PANEL_FONT,
	bg=CARD_BG,
	fg=PANEL_TITLE,
	bd=1,
	relief="solid",
	padx=18,
	pady=16,
	highlightbackground=BORDER,
)

# descriptor_frame.pack(pady=10, padx=20)

log_frame = tk.LabelFrame(
	scrollable_frame,
	text="Log Window",
	font=PANEL_FONT,
	bg=CARD_BG,
	fg=PANEL_TITLE,
	bd=1,
	relief="solid",
	padx=18,
	pady=16,
	highlightbackground=BORDER,
)

# log_frame.pack(pady=10, padx=20, fill="x")

view_3d_frame = tk.LabelFrame(
	scrollable_frame,
	text="3D Structure Panel",
	font=PANEL_FONT,
	bg=CARD_BG,
	fg=PANEL_TITLE,
	bd=1,
	relief="solid",
	padx=18,
	pady=16,
	highlightbackground=BORDER,
)

# view_3d_frame.pack(pady=10, padx=20)

control_frame = tk.LabelFrame(
	scrollable_frame,
	text="Controls",
	font=PANEL_FONT,
	bg=CARD_BG,
	fg=PANEL_TITLE,
	bd=1,
	relief="solid",
	padx=18,
	pady=16,
	highlightbackground=BORDER,
)

# control_frame.pack(pady=10, padx=20)

summary_frame = tk.LabelFrame(
	scrollable_frame,
	text="Molecule Summary",
	font=PANEL_FONT,
	bg=CARD_BG,
	fg=PANEL_TITLE,
	bd=1,
	relief="solid",
	padx=18,
	pady=16,
	highlightbackground=BORDER,
)

for column in range(3):
	scrollable_frame.grid_columnconfigure(column, weight=1, uniform="main")

PANEL_LAYOUT = {
	search_frame: {"row": 1, "column": 0, "pady": 10, "padx": (24, 10), "sticky": "nsew"},
	descriptor_frame: {"row": 1, "column": 1, "pady": 10, "padx": 10, "sticky": "nsew"},
	view_3d_frame: {"row": 1, "column": 2, "pady": 10, "padx": (10, 24), "sticky": "nsew"},
	control_frame: {"row": 2, "column": 0, "pady": (0, 20), "padx": (24, 10), "sticky": "nsew"},
	structure_frame: {"row": 2, "column": 1, "pady": (0, 20), "padx": 10, "sticky": "nsew"},
	log_frame: {"row": 2, "column": 2, "pady": (0, 20), "padx": (10, 24), "sticky": "nsew"},
	summary_frame: {"row": 3, "column": 0, "columnspan": 3, "pady": (0, 24), "padx": 24, "sticky": "ew"},
}

def show_panel(panel):
	panel.grid(**PANEL_LAYOUT[panel])


def hide_panel(panel):
	panel.grid_remove()


def hide_intro():
	intro_frame.grid_remove()
	center_intro.grid_remove()
	right_intro.grid_remove()


def show_similar_tab():
	global similar_tab_visible

	if not similar_tab_visible:
		notebook.add(similar_tab, text="Similar Molecules")
		similar_tab_visible = True


def show_comparison_tab():
	global comparison_tab_visible

	if not comparison_tab_visible:
		notebook.add(comparison_tab, text="Comparison")
		comparison_tab_visible = True


def hide_similar_tab():
	global similar_tab_visible

	if similar_tab_visible:
		notebook.hide(similar_tab)
		similar_tab_visible = False


def hide_comparison_tab():
	global comparison_tab_visible

	if comparison_tab_visible:
		notebook.hide(comparison_tab)
		comparison_tab_visible = False


def show_initial_discovery_view():
	intro_frame.grid()
	center_intro.grid()
	right_intro.grid()
	search_frame.grid(row=1, column=1, pady=(288, 22), padx=10, sticky="n")
	result_label.config(text="Try a drug name or PubChem CID to begin.")


def return_to_front_page():
	global current_mol, view_3d_atoms, view_3d_bonds

	current_mol = None
	view_3d_atoms = []
	view_3d_bonds = []
	notebook.select(explorer_tab)
	hide_similar_tab()
	hide_comparison_tab()

	hide_panel(structure_frame)
	hide_panel(view_3d_frame)
	hide_panel(descriptor_frame)
	hide_panel(log_frame)
	hide_panel(control_frame)
	hide_panel(summary_frame)
	show_initial_discovery_view()

	drug_entry.delete(0, "end")
	image_label.config(image="")
	image_label.image = None
	property_table.delete(*property_table.get_children())
	summary_label.config(text="")
	clear_similar_molecules("Search for a drug in the Explorer tab to load similar molecules.")
	clear_comparison_results()
	view_3d_canvas.delete("all")
	view_3d_canvas.create_text(
		int(view_3d_canvas["width"]) / 2,
		int(view_3d_canvas["height"]) / 2,
		text="Search for a drug to see its 3D structure",
		fill=MUTED,
		font=FONT,
	)
	if not startup_exit_button.winfo_ismapped():
		startup_exit_button.pack(before=result_label, pady=(0, 12))


def search_drug():
	global current_mol

	search_input = drug_entry.get().strip()

	if search_input == "":
		result_label.config(text="Please enter a drug name or CID.")
		clear_similar_molecules("Search for a drug in the Explorer tab to load similar molecules.")
		add_log("[INFO] No search input entered.")
		return

	add_log("[INFO] Searching PubChem...")

	if search_input.isdigit():
		compounds = pcp.get_compounds(search_input, "cid")
		add_log("[INFO] Searching by CID...")
	else:
		compounds = pcp.get_compounds(search_input, "name")
		add_log("[INFO] Searching by drug name...")

	if compounds:
		compound = compounds[0]
		compound_name = compound.synonyms[0] if compound.synonyms else search_input
		hide_intro()
		show_similar_tab()
		show_comparison_tab()
		startup_exit_button.pack_forget()
		show_panel(search_frame)
		show_panel(structure_frame)
		show_panel(view_3d_frame)
		show_panel(descriptor_frame)
		show_panel(log_frame)
		show_panel(control_frame)
		show_panel(summary_frame)
		comparison_a_entry.delete(0, "end")
		comparison_a_entry.insert(0, compound_name)

		add_log("[INFO] Compound found.")

		smiles = compound.smiles
		mol = Chem.MolFromSmiles(smiles)
		current_mol = mol

		add_log("[INFO] SMILES obtained.")

		mol_image = Draw.MolToImage(mol, size=(180, 180))
		tk_image = ImageTk.PhotoImage(mol_image)

		image_label.config(image=tk_image)
		image_label.image = tk_image

		add_log("[INFO] Structure generated.")
		prepare_3d_view()
		load_similar_molecules(compound, mol)

		molecular_weight = Descriptors.MolWt(mol)
		logp = Descriptors.MolLogP(mol)
		tpsa = Descriptors.TPSA(mol)
		hba = Descriptors.NumHAcceptors(mol)
		hbd = Descriptors.NumHDonors(mol)
		rotatable_bonds = Descriptors.NumRotatableBonds(mol)

		lipinski_violations, drug_like = evaluate_lipinski(molecular_weight, logp, hba, hbd)
		veber_violations = evaluate_veber(tpsa, rotatable_bonds)

		property_table.delete(*property_table.get_children())

		property_table.insert("", "end", values=("MW", round(molecular_weight, 2)))
		property_table.insert("", "end", values=("LogP", round(logp, 2)))
		property_table.insert("", "end", values=("TPSA", round(tpsa, 2)))
		property_table.insert("", "end", values=("HBA", hba))
		property_table.insert("", "end", values=("HBD", hbd))
		property_table.insert("", "end", values=("Rotatable Bonds", rotatable_bonds))
		property_table.insert("", "end", values=("Lipinski Violations", lipinski_violations))
		property_table.insert("", "end", values=("Veber Violations", veber_violations))
		property_table.insert("", "end", values=("Drug-like", drug_like))
		summary_label.config(text=build_molecule_summary(compound_name, molecular_weight, logp, tpsa, lipinski_violations, veber_violations, drug_like))

		add_log("[INFO] Lipinski and Veber evaluations completed.")
		drug_significance = get_drug_significance(compound.cid)
		add_log("[INFO] PubChem drug significance loaded.")

		result_label.config(
			text="Drug: " + compound_name +
			"\nCID: " + str(compound.cid) +
			"\nFormula: " + str(compound.molecular_formula) +
			"\n\nReal-Life Drug Significance:\n" + drug_significance
		)

	else:
		result_label.config(text="No compound found.")
		clear_similar_molecules("No compound found, so similar molecules were not loaded.")
		add_log("[INFO] No compound found.")
def calculate_similarity():
	drug_a = drug_a_entry.get().strip()
	drug_b = drug_b_entry.get().strip()

	if drug_a == "" or drug_b == "":
		result_label.config(text="Please enter both drug names.")
		add_log("[INFO] Similarity comparison failed: missing input.")
		return

	add_log("[INFO] Searching compounds for similarity comparison...")

	compounds_a = pcp.get_compounds(drug_a, "name")
	compounds_b = pcp.get_compounds(drug_b, "name")

	if not compounds_a or not compounds_b:
		result_label.config(text="One or both compounds were not found.")
		add_log("[INFO] Similarity comparison failed: compound not found.")
		return

	mol_a = Chem.MolFromSmiles(compounds_a[0].smiles)
	mol_b = Chem.MolFromSmiles(compounds_b[0].smiles)

	fp_a = Chem.RDKFingerprint(mol_a)
	fp_b = Chem.RDKFingerprint(mol_b)

	similarity = DataStructs.TanimotoSimilarity(fp_a, fp_b)

	result_label.config(
		text=drug_a + " vs " + drug_b +
		"\nTanimoto Similarity: " + str(round(similarity, 2))
	)

	add_log("[INFO] Tanimoto similarity calculated.")


def classify_weight(molecular_weight):
	if molecular_weight < 300:
		return "low molecular weight"
	if molecular_weight <= 500:
		return "moderate molecular weight"
	return "high molecular weight"


def classify_polarity(tpsa):
	if tpsa < 60:
		return "low polarity"
	if tpsa <= 140:
		return "moderate polarity"
	return "high polarity"


def build_molecule_summary(name, molecular_weight, logp, tpsa, lipinski_violations, veber_violations, drug_like):
	weight_text = classify_weight(molecular_weight)
	size_text = "small" if molecular_weight < 300 else "medium-sized" if molecular_weight <= 500 else "large"
	polarity_text = classify_polarity(tpsa)
	lipinski_text = "no Lipinski violations" if lipinski_violations == 0 else str(lipinski_violations) + " Lipinski violation(s)"
	veber_text = "no Veber violations" if veber_violations == 0 else str(veber_violations) + " Veber violation(s)"
	drug_like_text = "It is predicted to be drug-like." if drug_like == "YES" else "It is not predicted to be drug-like by these simple rules."

	return (
		name + " is a " + size_text + " organic molecule with " + weight_text +
		", " + polarity_text +
		", LogP of " + str(round(logp, 2)) +
		", " + lipinski_text +
		", and " + veber_text +
		". " + drug_like_text
	)


def clean_pubchem_text(text):
	return " ".join(str(text).replace("\n", " ").split())


def collect_pubchem_strings(section):
	strings = []

	for info in section.get("Information", []):
		if "StringValue" in info:
			strings.append(clean_pubchem_text(info["StringValue"]))

		value = info.get("Value", {})
		for item in value.get("StringWithMarkup", []):
			if "String" in item:
				strings.append(clean_pubchem_text(item["String"]))

	for child_section in section.get("Section", []):
		strings.extend(collect_pubchem_strings(child_section))

	return [text for text in strings if text]


def find_pubchem_sections(section, wanted_headings):
	matches = []
	heading = section.get("TOCHeading", "").lower()

	if any(wanted_heading in heading for wanted_heading in wanted_headings):
		matches.append(section)

	for child_section in section.get("Section", []):
		matches.extend(find_pubchem_sections(child_section, wanted_headings))

	return matches


def get_pubchem_section_texts(record, wanted_headings):
	texts = []

	for section in record.get("Section", []):
		for matched_section in find_pubchem_sections(section, wanted_headings):
			texts.extend(collect_pubchem_strings(matched_section))

	unique_texts = []
	for text in texts:
		if text not in unique_texts and len(text) > 30:
			unique_texts.append(text)

	return unique_texts


def load_pubchem_json(url):
	request = urllib.request.Request(
		url,
		headers={"User-Agent": "Drug Molecule Explorer/1.0 (educational Tkinter app)"},
	)

	try:
		with urllib.request.urlopen(request, timeout=12) as response:
			return json.loads(response.read().decode("utf-8"))
	except urllib.error.URLError as error:
		reason = getattr(error, "reason", error)

		if not isinstance(reason, ssl.SSLCertVerificationError):
			raise

		try:
			import certifi

			certificate_context = ssl.create_default_context(cafile=certifi.where())
			with urllib.request.urlopen(request, timeout=12, context=certificate_context) as response:
				return json.loads(response.read().decode("utf-8"))
		except ImportError:
			pass
		except urllib.error.URLError as error:
			reason = getattr(error, "reason", error)

			if not isinstance(reason, ssl.SSLCertVerificationError):
				raise

		unverified_context = ssl._create_unverified_context()

		with urllib.request.urlopen(request, timeout=12, context=unverified_context) as response:
			return json.loads(response.read().decode("utf-8"))


def get_drug_significance(cid):
	description_headings = [
		"record description",
		"description",
	]
	fallback_headings = [
		"drug indication",
		"therapeutic uses",
		"pharmacology",
		"pharmacological",
		"use and manufacturing",
	]
	url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/" + str(cid) + "/JSON"

	try:
		data = load_pubchem_json(url)
	except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ssl.SSLError):
		return "PubChem description data could not be loaded right now."

	record = data.get("Record", {})
	unique_texts = get_pubchem_section_texts(record, description_headings)

	if not unique_texts:
		unique_texts = get_pubchem_section_texts(record, fallback_headings)

	if not unique_texts:
		return "No real-life use or description was found in the PubChem description sections."

	return " ".join(unique_texts[:2]) + "\n\nSource: PubChem Description section."


def get_compound_from_input(search_input):
	search_input = search_input.strip()

	if search_input == "":
		return None

	if search_input.isdigit():
		compounds = pcp.get_compounds(search_input, "cid")
	else:
		compounds = pcp.get_compounds(search_input, "name")

	if not compounds:
		return None

	return compounds[0]


def get_molecule_profile(compound, fallback_name):
	name = compound.synonyms[0] if compound.synonyms else fallback_name
	if not compound.smiles:
		return None

	mol = Chem.MolFromSmiles(compound.smiles)

	if mol is None:
		return None

	molecular_weight = Descriptors.MolWt(mol)
	logp = Descriptors.MolLogP(mol)
	tpsa = Descriptors.TPSA(mol)
	hba = Descriptors.NumHAcceptors(mol)
	hbd = Descriptors.NumHDonors(mol)
	rotatable_bonds = Descriptors.NumRotatableBonds(mol)
	lipinski_violations, drug_like = evaluate_lipinski(molecular_weight, logp, hba, hbd)
	veber_violations = evaluate_veber(tpsa, rotatable_bonds)

	return {
		"name": name,
		"compound": compound,
		"mol": mol,
		"mw": molecular_weight,
		"logp": logp,
		"tpsa": tpsa,
		"hba": hba,
		"hbd": hbd,
		"rotatable": rotatable_bonds,
		"lipinski": lipinski_violations,
		"veber": veber_violations,
		"drug_like": drug_like,
	}
def prepare_canvas_model(mol):
	mol_3d = Chem.AddHs(mol)
	embed_status = AllChem.EmbedMolecule(mol_3d, randomSeed=42)

	if embed_status != 0:
		return None

	try:
		AllChem.MMFFOptimizeMolecule(mol_3d)
	except Exception:
		AllChem.UFFOptimizeMolecule(mol_3d)

	conformer = mol_3d.GetConformer()
	raw_atoms = []

	for atom in mol_3d.GetAtoms():
		position = conformer.GetAtomPosition(atom.GetIdx())
		raw_atoms.append([position.x, position.y, position.z, atom.GetSymbol()])

	center_x = sum(atom[0] for atom in raw_atoms) / len(raw_atoms)
	center_y = sum(atom[1] for atom in raw_atoms) / len(raw_atoms)
	center_z = sum(atom[2] for atom in raw_atoms) / len(raw_atoms)

	return {
		"atoms": [
			(x - center_x, y - center_y, z - center_z, symbol)
			for x, y, z, symbol in raw_atoms
		],
		"bonds": [
			(bond.GetBeginAtomIdx(), bond.GetEndAtomIdx())
			for bond in mol_3d.GetBonds()
		],
		"angle_x": 0,
		"angle_y": 0,
	}
def draw_model_on_canvas(canvas_widget, model):
	canvas_widget.delete("all")

	if model is None:
		canvas_widget.create_text(
			int(canvas_widget["width"]) / 2,
			int(canvas_widget["height"]) / 2,
			text="Enter molecules to see a 3D model",
			fill=MUTED,
			font=FONT,
		)
		return

	width = int(canvas_widget["width"])
	height = int(canvas_widget["height"])
	center_x = width / 2
	center_y = height / 2
	cos_y = math.cos(model["angle_y"])
	sin_y = math.sin(model["angle_y"])
	cos_x = math.cos(model["angle_x"])
	sin_x = math.sin(model["angle_x"])
	projected_atoms = []

	max_distance = max(
		math.sqrt((x * x) + (y * y) + (z * z))
		for x, y, z, symbol in model["atoms"]
	)
	scale = min(width, height) * 0.32 / max(max_distance, 1)

	for x, y, z, symbol in model["atoms"]:
		rotated_x = (x * cos_y) + (z * sin_y)
		rotated_z = (-x * sin_y) + (z * cos_y)
		rotated_y = (y * cos_x) - (rotated_z * sin_x)
		rotated_z = (y * sin_x) + (rotated_z * cos_x)
		depth_scale = 1 + (rotated_z * 0.035)
		screen_x = center_x + (rotated_x * scale * depth_scale)
		screen_y = center_y - (rotated_y * scale * depth_scale)
		projected_atoms.append((screen_x, screen_y, rotated_z, symbol))

	for start, end in model["bonds"]:
		x1, y1, z1, symbol1 = projected_atoms[start]
		x2, y2, z2, symbol2 = projected_atoms[end]
		canvas_widget.create_line(
			x1,
			y1,
			x2,
			y2,
			fill="#6a9955" if (z1 + z2) > 0 else "#4b5563",
			width=2,
		)

	for x, y, z, symbol in sorted(projected_atoms, key=lambda atom: atom[2]):
		color = ATOM_COLORS.get(symbol, "#d7ba7d")
		radius = 6 if symbol != "H" else 4
		radius += max(min(z, 4), -4) * 0.22
		canvas_widget.create_oval(
			x - radius,
			y - radius,
			x + radius,
			y + radius,
			fill=color,
			outline="#1e1e1e",
			width=1,
		)

	model["angle_y"] += 0.035
	model["angle_x"] += 0.006
def draw_comparison_models():
	global comparison_rotation_job

	if "comparison_3d_a_canvas" not in globals():
		return

	draw_model_on_canvas(comparison_3d_a_canvas, comparison_models.get("a"))
	draw_model_on_canvas(comparison_3d_b_canvas, comparison_models.get("b"))
	comparison_rotation_job = root.after(50, draw_comparison_models)


def clear_comparison_results():
	global comparison_models

	comparison_models = {}

	if "comparison_table" not in globals():
		return

	comparison_table.delete(*comparison_table.get_children())
	comparison_summary.config(text="Enter two molecule names or CIDs to compare structure and descriptors.")
	comparison_image_a.config(image="")
	comparison_image_a.image = None
	comparison_image_b.config(image="")
	comparison_image_b.image = None
	comparison_3d_a_canvas.delete("all")
	comparison_3d_b_canvas.delete("all")
	comparison_3d_a_canvas.create_text(160, 110, text="3D model A", fill=MUTED, font=FONT)
	comparison_3d_b_canvas.create_text(160, 110, text="3D model B", fill=MUTED, font=FONT)


def compare_molecules():
	first_input = comparison_a_entry.get().strip()
	second_input = comparison_b_entry.get().strip()

	if first_input == "" or second_input == "":
		comparison_summary.config(text="Please enter two molecule names or CIDs.")
		return

	comparison_summary.config(text="Searching PubChem and building comparison...")
	root.update_idletasks()

	try:
		compound_a = get_compound_from_input(first_input)
		compound_b = get_compound_from_input(second_input)
	except Exception:
		comparison_summary.config(text="Comparison failed while searching PubChem.")
		return

	if compound_a is None or compound_b is None:
		comparison_summary.config(text="One or both molecules were not found.")
		return

	profile_a = get_molecule_profile(compound_a, first_input)
	profile_b = get_molecule_profile(compound_b, second_input)

	if profile_a is None or profile_b is None:
		comparison_summary.config(text="One or both molecules could not be converted into structures.")
		return

	image_a = ImageTk.PhotoImage(Draw.MolToImage(profile_a["mol"], size=(180, 160)))
	image_b = ImageTk.PhotoImage(Draw.MolToImage(profile_b["mol"], size=(180, 160)))
	comparison_image_a.config(image=image_a)
	comparison_image_a.image = image_a
	comparison_image_b.config(image=image_b)
	comparison_image_b.image = image_b
	comparison_name_a.config(text=profile_a["name"])
	comparison_name_b.config(text=profile_b["name"])

	comparison_models["a"] = prepare_canvas_model(profile_a["mol"])
	comparison_models["b"] = prepare_canvas_model(profile_b["mol"])

	fp_a = Chem.RDKFingerprint(profile_a["mol"])
	fp_b = Chem.RDKFingerprint(profile_b["mol"])
	similarity = DataStructs.TanimotoSimilarity(fp_a, fp_b)

	comparison_table.delete(*comparison_table.get_children())
	comparison_table.insert("", "end", values=("MW", round(profile_a["mw"], 2), round(profile_b["mw"], 2), round(profile_a["mw"] - profile_b["mw"], 2)))
	comparison_table.insert("", "end", values=("LogP", round(profile_a["logp"], 2), round(profile_b["logp"], 2), round(profile_a["logp"] - profile_b["logp"], 2)))
	comparison_table.insert("", "end", values=("TPSA", round(profile_a["tpsa"], 2), round(profile_b["tpsa"], 2), round(profile_a["tpsa"] - profile_b["tpsa"], 2)))
	comparison_table.insert("", "end", values=("HBA", profile_a["hba"], profile_b["hba"], profile_a["hba"] - profile_b["hba"]))
	comparison_table.insert("", "end", values=("HBD", profile_a["hbd"], profile_b["hbd"], profile_a["hbd"] - profile_b["hbd"]))
	comparison_table.insert("", "end", values=("Rotatable Bonds", profile_a["rotatable"], profile_b["rotatable"], profile_a["rotatable"] - profile_b["rotatable"]))
	comparison_table.insert("", "end", values=("Lipinski Violations", profile_a["lipinski"], profile_b["lipinski"], profile_a["lipinski"] - profile_b["lipinski"]))
	comparison_table.insert("", "end", values=("Veber Violations", profile_a["veber"], profile_b["veber"], profile_a["veber"] - profile_b["veber"]))
	comparison_table.insert("", "end", values=("Drug-like", profile_a["drug_like"], profile_b["drug_like"], "Same" if profile_a["drug_like"] == profile_b["drug_like"] else "Different"))
	comparison_table.insert("", "end", values=("Fingerprint Similarity", round(similarity, 2), round(similarity, 2), "0.0"))

	heavier_name = profile_a["name"] if profile_a["mw"] > profile_b["mw"] else profile_b["name"]
	more_polar_name = profile_a["name"] if profile_a["tpsa"] > profile_b["tpsa"] else profile_b["name"]
	drug_like_text = "Both are predicted to be drug-like." if profile_a["drug_like"] == "YES" and profile_b["drug_like"] == "YES" else "Their drug-like predictions differ." if profile_a["drug_like"] != profile_b["drug_like"] else "Neither is predicted to be drug-like by these simple rules."

	comparison_summary.config(
		text=profile_a["name"] + " and " + profile_b["name"] +
		" have a fingerprint similarity of " + str(round(similarity, 2)) +
		". " + heavier_name + " has the higher molecular weight, while " +
		more_polar_name + " has the higher TPSA/polarity. " + drug_like_text
	)
def apply_option():
	selected_option = info_type.get()

	hide_panel(structure_frame)
	hide_panel(view_3d_frame)
	hide_panel(descriptor_frame)
	hide_panel(log_frame)
	hide_panel(summary_frame)
	show_panel(search_frame)

	if selected_option == "Show All":
		show_panel(structure_frame)
		show_panel(view_3d_frame)
		show_panel(descriptor_frame)
		show_panel(log_frame)
		show_panel(summary_frame)

	elif selected_option == "General Information":
		pass

	elif selected_option == "Molecular Properties":
		show_panel(descriptor_frame)

	elif selected_option == "2D Structure":
		show_panel(structure_frame)

	elif selected_option == "3D Structure":
		show_panel(view_3d_frame)

	elif selected_option == "Log Window":
		show_panel(log_frame)

	elif selected_option == "Molecule Summary":
		show_panel(summary_frame)

	add_log("[INFO] Display changed to: " + selected_option)


def save_sdf():
	if current_mol is None:
		result_label.config(text="Please search for a drug first.")
		return
	file_path = filedialog.asksaveasfilename(
		defaultextension=".sdf",
		filetypes=[("SDF files", "*.sdf")],
	)
	if file_path:
		writer = Chem.SDWriter(file_path)
		writer.write(current_mol)
		writer.close()
		result_label.config(text="SDF file saved successfully.")
		add_log("[INFO] SDF file saved.")


def save_pdb():
	mol_3d = generate_3d_molecule()
	if mol_3d is None:
		return
	file_path = filedialog.asksaveasfilename(
		defaultextension=".pdb",
		filetypes=[("PDB files", "*.pdb")],
	)
	if file_path:
		Chem.MolToPDBFile(mol_3d, file_path)
		result_label.config(text="PDB file saved successfully.")
		add_log("[INFO] PDB file saved")
def evaluate_lipinski(molecular_weight, logp, hba, hbd):
	violations = 0
	if molecular_weight >= 500:
		violations += 1
	if logp >= 5:
		violations += 1
	if hbd > 5:
		violations += 1
	if violations == 0:
		drug_like = "YES"
	else:
		drug_like = "NO"
	return violations, drug_like


def evaluate_veber(tpsa, rotatable_bonds):
	violations = 0
	if tpsa > 140:
		violations += 1
	if rotatable_bonds > 10:
		violations += 1
	return violations


def add_log(message):
	log_text.insert("end", message + "\n")
	log_text.see("end")


def clear_similar_molecules(message):
	similar_table.delete(*similar_table.get_children())
	similar_status.config(text=message)


def load_similar_molecules(compound, mol):
	similar_table.delete(*similar_table.get_children())
	similar_status.config(text="Searching for similar molecules...")
	root.update_idletasks()

	try:
		similar_compounds = pcp.get_compounds(
			compound.smiles,
			"smiles",
			searchtype="similarity",
			listkey_count=12,
		)
	except Exception:
		similar_status.config(text="Similar molecules could not be loaded.")
		add_log("[INFO] Similar molecule search failed.")
		return

	if not similar_compounds:
		similar_status.config(text="No similar molecules found.")
		add_log("[INFO] No similar molecules found.")
		return

	source_fp = Chem.RDKFingerprint(mol)
	ranked_compounds = []

	for similar_compound in similar_compounds:
		if similar_compound.cid == compound.cid or not similar_compound.smiles:
			continue

		similar_mol = Chem.MolFromSmiles(similar_compound.smiles)
		if similar_mol is None:
			continue

		similar_fp = Chem.RDKFingerprint(similar_mol)
		score = DataStructs.TanimotoSimilarity(source_fp, similar_fp)
		name = similar_compound.synonyms[0] if similar_compound.synonyms else "CID " + str(similar_compound.cid)
		ranked_compounds.append((
			score,
			name,
			similar_compound.cid,
			similar_compound.molecular_formula,
			round(Descriptors.MolWt(similar_mol), 2),
		))

	ranked_compounds.sort(reverse=True)

	for score, name, cid, formula, molecular_weight in ranked_compounds[:8]:
		similar_table.insert(
			"",
			"end",
			values=(name, cid, formula, molecular_weight, round(score, 2)),
		)

	if ranked_compounds:
		similar_status.config(text="Showing similar molecules ranked by fingerprint similarity.")
		add_log("[INFO] Similar molecules loaded.")
	else:
		similar_status.config(text="No different similar molecules found.")
 
def open_similar_molecule(event):
	selected_item = similar_table.focus()

	if not selected_item:
		return

	values = similar_table.item(selected_item, "values")

	if not values:
		return

	cid = values[1]
	notebook.select(explorer_tab)
	drug_entry.delete(0, "end")
	drug_entry.insert(0, cid)
	add_log("[INFO] Opening similar molecule CID: " + str(cid))
	search_drug()
def prepare_3d_view():
	global view_3d_atoms, view_3d_bonds, view_3d_angle_x, view_3d_angle_y, view_3d_zoom

	if current_mol is None:
		return

	mol_3d = Chem.AddHs(current_mol)
	embed_status = AllChem.EmbedMolecule(mol_3d, randomSeed=42)

	if embed_status != 0:
		view_3d_canvas.delete("all")
		view_3d_canvas.create_text(
			int(view_3d_canvas["width"]) / 2,
			int(view_3d_canvas["height"]) / 2,
			text="3D preview unavailable",
			fill=MUTED,
			font=FONT
		)
		add_log("[INFO] 3D preview could not be generated.")
		return

	try:
		AllChem.MMFFOptimizeMolecule(mol_3d)
	except Exception:
		AllChem.UFFOptimizeMolecule(mol_3d)

	conformer = mol_3d.GetConformer()

	raw_atoms = []
	for atom in mol_3d.GetAtoms():
		position = conformer.GetAtomPosition(atom.GetIdx())
		raw_atoms.append([
			position.x,
			position.y,
			position.z,
			atom.GetSymbol()
		])

	center_x = sum(atom[0] for atom in raw_atoms) / len(raw_atoms)
	center_y = sum(atom[1] for atom in raw_atoms) / len(raw_atoms)
	center_z = sum(atom[2] for atom in raw_atoms) / len(raw_atoms)

	view_3d_atoms = [
		(x - center_x, y - center_y, z - center_z, symbol)
		for x, y, z, symbol in raw_atoms
	]
	view_3d_bonds = [
		(bond.GetBeginAtomIdx(), bond.GetEndAtomIdx())
		for bond in mol_3d.GetBonds()
	]
	view_3d_angle_x = 0
	view_3d_angle_y = 0
	view_3d_zoom = 1.0

	add_log("[INFO] 3D preview generated.")
	start_3d_rotation()

def start_3d_rotation():
	global rotation_job

	if rotation_job is not None:
		root.after_cancel(rotation_job)

	draw_3d_molecule()
def draw_3d_molecule():
    global rotation_job, view_3d_angle_x, view_3d_angle_y

    view_3d_canvas.delete("all")

    if not view_3d_atoms:
        view_3d_canvas.create_text(
            int(view_3d_canvas["width"]) / 2,
            int(view_3d_canvas["height"]) / 2,
            text="Search for a drug to see its 3D structure",
            fill=MUTED,
            font=FONT
        )
        rotation_job = root.after(60, draw_3d_molecule)
        return

    width = int(view_3d_canvas["width"])
    height = int(view_3d_canvas["height"])
    center_x = width / 2
    center_y = height / 2
    angle_y = view_3d_angle_y
    angle_x = view_3d_angle_x
    cos_y = math.cos(angle_y)
    sin_y = math.sin(angle_y)
    cos_x = math.cos(angle_x)
    sin_x = math.sin(angle_x)
    projected_atoms = []

    max_distance = max(
        math.sqrt((x * x) + (y * y) + (z * z))
        for x, y, z, symbol in view_3d_atoms
    )
    scale = min(width, height) * 0.32 * view_3d_zoom / max(max_distance, 1)

    for x, y, z, symbol in view_3d_atoms:
        rotated_x = (x * cos_y) + (z * sin_y)
        rotated_z = (-x * sin_y) + (z * cos_y)
        rotated_y = (y * cos_x) - (rotated_z * sin_x)
        rotated_z = (y * sin_x) + (rotated_z * cos_x)
        depth_scale = 1 + (rotated_z * 0.035)
        screen_x = center_x + (rotated_x * scale * depth_scale)
        screen_y = center_y - (rotated_y * scale * depth_scale)
        projected_atoms.append((screen_x, screen_y, rotated_z, symbol))

    for start, end in view_3d_bonds:
        x1, y1, z1, symbol1 = projected_atoms[start]
        x2, y2, z2, symbol2 = projected_atoms[end]
        shade = "#6a9955" if (z1 + z2) > 0 else "#4b5563"
        bond_width = max(2, int(3 * view_3d_zoom))
        view_3d_canvas.create_line(x1, y1, x2, y2, fill=shade, width=bond_width)

    atom_order = sorted(
        range(len(projected_atoms)),
        key=lambda index: projected_atoms[index][2]
    )

    for index in atom_order:
        x, y, z, symbol = projected_atoms[index]
        color = ATOM_COLORS.get(symbol, "#d7ba7d")
        radius = 7 if symbol != "H" else 4
        radius *= max(0.8, min(view_3d_zoom, 1.8))
        radius += max(min(z, 4), -4) * 0.3
        view_3d_canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill=color,
            outline="#1e1e1e",
            width=1
        )

    if not view_3d_dragging:
        view_3d_angle_y += 0.035
        view_3d_angle_x += 0.006

    rotation_job = root.after(45, draw_3d_molecule)


def start_3d_drag(event):
    global view_3d_dragging, view_3d_last_x, view_3d_last_y

    view_3d_dragging = True
    view_3d_last_x = event.x
    view_3d_last_y = event.y


def drag_3d_molecule(event):
    global rotation_job, view_3d_angle_x, view_3d_angle_y, view_3d_last_x, view_3d_last_y

    if not view_3d_dragging:
        return

    delta_x = event.x - view_3d_last_x
    delta_y = event.y - view_3d_last_y
    view_3d_angle_y += delta_x * 0.012
    view_3d_angle_x += delta_y * 0.012
    view_3d_last_x = event.x
    view_3d_last_y = event.y

    if rotation_job is not None:
        root.after_cancel(rotation_job)
        rotation_job = None

    draw_3d_molecule()


def stop_3d_drag(event):
    global view_3d_dragging

    view_3d_dragging = False


def update_3d_zoom(multiplier):
    global rotation_job, view_3d_zoom

    view_3d_zoom *= multiplier
    view_3d_zoom = max(0.45, min(view_3d_zoom, 3.0))

    if rotation_job is not None:
        root.after_cancel(rotation_job)
        rotation_job = None

    draw_3d_molecule()


def zoom_3d_molecule(event):
    event_num = getattr(event, "num", None)
    event_delta = getattr(event, "delta", 0)

    if event_num == 4 or event_delta > 0:
        update_3d_zoom(1.12)
    elif event_num == 5 or event_delta < 0:
        update_3d_zoom(1 / 1.12)


def reset_3d_zoom():
    global rotation_job, view_3d_zoom

    view_3d_zoom = 1.0

    if rotation_job is not None:
        root.after_cancel(rotation_job)
        rotation_job = None

    draw_3d_molecule()


def enable_3d_zoom(event):
    view_3d_canvas.bind_all("<MouseWheel>", zoom_3d_molecule)
    view_3d_canvas.bind_all("<Button-4>", zoom_3d_molecule)
    view_3d_canvas.bind_all("<Button-5>", zoom_3d_molecule)


def disable_3d_zoom(event):
    view_3d_canvas.unbind_all("<MouseWheel>")
    view_3d_canvas.unbind_all("<Button-4>")
    view_3d_canvas.unbind_all("<Button-5>")


bind_explorer_scroll()

def generate_3d_molecule():
    if current_mol is None:
        result_label.config(text="Please search for a drug first.")
        add_log("[INFO] No molecule available for 3D generation.")
        return None

    mol_3d = Chem.AddHs(current_mol)
    AllChem.EmbedMolecule(mol_3d)
    add_log("[INFO] 3D geometry generated.")
    AllChem.MMFFOptimizeMolecule(mol_3d)
    add_log("[INFO] 3D geometry optimized.")
    return mol_3d


def create_feature_card(parent, title, body, row, column, sticky="nsew"):
    card = tk.Frame(
        parent,
        bg=CARD_BG,
        highlightthickness=1,
        highlightbackground=BORDER,
        padx=16,
        pady=14
    )
    card.grid(row=row, column=column, padx=8, pady=8, sticky=sticky)

    tk.Label(
        card,
        text=title,
        font=("Helvetica", 12, "bold"),
        bg=CARD_BG,
        fg=PANEL_TITLE,
        anchor="w"
    ).pack(fill="x")

    tk.Label(
        card,
        text=body,
        font=SMALL_FONT,
        bg=CARD_BG,
        fg=MUTED,
        justify="left",
        wraplength=245
    ).pack(fill="x", pady=(7, 0))

    return card

def draw_hero_molecule():
    global hero_rotation_angle

    if "hero_canvas" not in globals():
        return

    hero_canvas.delete("all")
    width = max(hero_canvas.winfo_width(), int(hero_canvas["width"]))
    height = max(hero_canvas.winfo_height(), int(hero_canvas["height"]))
    center_x = width / 2
    center_y = height / 2

    # Background glow rings
    glow_colors = ["#10171f", "#13202b", "#172a39", "#1f3448", "#243b52"]
    for i, color in enumerate(glow_colors, start=1):
        hero_canvas.create_oval(
            center_x - i * 95,
            center_y - i * 95,
            center_x + i * 95,
            center_y + i * 95,
            fill=color,
            outline=""
        )

    # Orbit bands
    band_styles = [
        (70, "#3b82f6"),
        (98, "#65a30d"),
        (130, "#d7b377"),
    ]
    for radius, color in band_styles:
        hero_canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            outline=color,
            width=2,
            dash=(10, 8)
        )

    # Animated orbiting sparks
    for index, radius in enumerate((48, 84, 118), start=1):
        angle = hero_rotation_angle * (0.7 + index * 0.15)
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius
        size = 5 + index
        hero_canvas.create_oval(
            x - size,
            y - size,
            x + size,
            y + size,
            fill="#e0e7ff" if index == 1 else "#a7f3d0",
            outline=""
        )

    atoms = [
        (-1.6, -0.4, -0.15, "C"),
        (-0.85, 0.8, 0.4, "N"),
        (0.45, 0.3, -0.4, "C"),
        (1.7, -0.45, 0.25, "O"),
        (0.1, -1.05, 0.55, "S"),
        (-1.5, 1.1, -0.4, "H"),
        (1.15, 1.25, 0.55, "H"),
    ]
    bonds = [(0, 1), (1, 2), (2, 3), (2, 4), (1, 5), (2, 6)]
    cos_y = math.cos(hero_rotation_angle)
    sin_y = math.sin(hero_rotation_angle)
    cos_x = math.cos(hero_rotation_angle * 0.55)
    sin_x = math.sin(hero_rotation_angle * 0.55)
    projected_atoms = []

    for x, y, z, symbol in atoms:
        rotated_x = (x * cos_y) + (z * sin_y)
        rotated_z = (-x * sin_y) + (z * cos_y)
        rotated_y = (y * cos_x) - (rotated_z * sin_x)
        rotated_z = (y * sin_x) + (rotated_z * cos_x)
        depth_scale = 1 + (rotated_z * 0.08)
        screen_x = center_x + (rotated_x * 53 * depth_scale)
        screen_y = center_y - (rotated_y * 53 * depth_scale)
        projected_atoms.append((screen_x, screen_y, rotated_z, symbol))

    for start, end in bonds:
        x1, y1, z1, _ = projected_atoms[start]
        x2, y2, z2, _ = projected_atoms[end]
        hero_canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill="#a5b4fc" if (z1 + z2) > 0 else "#7c3aed",
            width=4,
            capstyle="round"
        )

    for x, y, z, symbol in sorted(projected_atoms, key=lambda atom: atom[2]):
        color = ATOM_COLORS.get(symbol, "#f8f8ff")
        radius = 11 if symbol != "H" else 7
        radius += max(min(z, 3), -3) * 1.1
        hero_canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill=color,
            outline=BG,
            width=2
        )
        if symbol != "H":
            hero_canvas.create_text(
                x,
                y,
                text=symbol,
                fill="#101214",
                font=("Helvetica", 8, "bold")
            )

    hero_canvas.create_text(
        center_x,
        28,
        text="Drug Molecule Explorer",
        fill="#e2e8f0",
        font=("Helvetica", 12, "bold")
    )
    hero_canvas.create_text(
        center_x,
        height - 22,
        text="Chemistry in motion",
        fill=MUTED,
        font=SMALL_FONT
    )

    hero_rotation_angle += 0.032
    root.after(45, draw_hero_molecule)


welcome_label = tk.Label(
    title_frame,
    text="Welcome to the Drug Molecule Explorer",
    font=TITLE_FONT,
    bg=BG,
    fg=TEXT
)
welcome_label.pack(pady=10)
subtitle_label = tk.Label(
    title_frame,
    text="Search a molecule, inspect drug-likeness, view structures, and compare similar compounds.",
    font=FONT,
    bg=BG,
    fg=MUTED,
    wraplength=760
)
subtitle_label.pack(pady=(0, 8))

hero_canvas = tk.Canvas(
    center_intro,
    width=340,
    height=255,
    bg="#17191b",
    highlightthickness=1,
    highlightbackground=BORDER
)
hero_canvas.grid(row=0, column=0, padx=8, pady=8, sticky="n")
create_feature_card(
    right_intro,
    "PubChem Lookup",
    "Accepts a drug name or CID, then pulls formula, identifiers, and SMILES data for descriptor analysis.",
    0,
    0
)
create_feature_card(
    right_intro,
"Similarity Clues",
"Ranks related molecules with fingerprint similarity to help spot nearby chemical candidates.",
1,
0
)
drug_entry = tk.Entry(
search_frame,
font=FONT,
width=28,
bg=INPUT_BG,
fg=TEXT,
insertbackground=TEXT,
relief="solid",
bd=1,
highlightthickness=1,
highlightbackground=BORDER,
highlightcolor=ACCENT
)
drug_entry.pack(pady=(6, 10), ipady=8)
drug_entry.bind("<Return>", lambda event: search_drug())
search_button = ttk.Button(search_frame, text="Search", command=search_drug, style="Modern.TButton")
search_button.pack(pady=(0, 12))
startup_exit_button = ttk.Button(
search_frame,
text="Exit",
command=root.destroy,
style="Secondary.TButton"
)
startup_exit_button.pack(pady=(0, 12))
result_label = tk.Label(
search_frame,
text="",
font=FONT,
bg=CARD_BG,
fg=TEXT,
justify="left",
wraplength=360
)
result_label.pack(pady=5)
result_label.config(text="Try a drug name or PubChem CID to begin.")
summary_label = tk.Label(
summary_frame,
text="",
font=FONT,
bg=CARD_BG,
fg=TEXT,
justify="left",
wraplength=1100
)
summary_label.pack(fill="x", pady=6)
image_label = tk.Label(structure_frame, bg=CARD_BG)
image_label.pack(pady=10)
view_3d_canvas = tk.Canvas(
view_3d_frame,
width=360,
height=280,
bg="#1e1e1e",
cursor="fleur",
highlightthickness=1,
highlightbackground=BORDER
)
view_3d_canvas.pack(pady=10)
view_3d_canvas.bind("<ButtonPress-1>", start_3d_drag)
view_3d_canvas.bind("<B1-Motion>", drag_3d_molecule)
view_3d_canvas.bind("<ButtonRelease-1>", stop_3d_drag)
view_3d_canvas.bind("<Enter>", enable_3d_zoom)
view_3d_canvas.bind("<Leave>", disable_3d_zoom)
view_3d_canvas.create_text(
180,
140,
text="Search for a drug to see its 3D structure",
fill=MUTED,
font=FONT
)
zoom_control_frame = tk.Frame(view_3d_frame, bg=CARD_BG)
zoom_control_frame.pack(pady=(0, 8))
zoom_in_button = ttk.Button(
zoom_control_frame,
text="+",
command=lambda: update_3d_zoom(1.18),
style="Secondary.TButton"
)
zoom_in_button.pack(side="left", padx=4)
zoom_out_button = ttk.Button(
zoom_control_frame,
text="-",
command=lambda: update_3d_zoom(1 / 1.18),
style="Secondary.TButton"
)
zoom_out_button.pack(side="left", padx=4)
zoom_reset_button = ttk.Button(
zoom_control_frame,
text="Reset",
command=reset_3d_zoom,
style="Secondary.TButton"
)
zoom_reset_button.pack(side="left", padx=4)
property_table = ttk.Treeview(
descriptor_frame,
columns=("Property", "Value"),
show="headings",
height=9
)
property_table.heading("Property", text="Property")
property_table.heading("Value", text="Value")
property_table.column("Property", width=200)
property_table.column("Value", width=150)
property_table.pack(pady=10)
log_text = tk.Text(
log_frame,
height=6,
width=44,
font=("Menlo", 11),
bg="#1e1e1e",
fg="#9cdcfe",
insertbackground=TEXT,
relief="flat",
bd=0,
padx=12,
pady=10
)
log_text.pack(side="left", pady=10, fill="both", expand=True)
log_scrollbar = ttk.Scrollbar(log_frame, command=log_text.yview)
log_scrollbar.pack(side="right", fill="y", pady=10)
log_text.config(yscrollcommand=log_scrollbar.set)
info_type = ttk.Combobox(
control_frame,
values=["Show All", "General Information", "Molecular Properties", "Molecule Summary", "2D Structure", "3D Structure", "Log Window"],
font=FONT,
state="readonly",
width=28
)
info_type.set("Show All")
info_type.pack(pady=(4, 8), ipady=4)
apply_button = ttk.Button(control_frame, text="Apply", command=apply_option, style="Modern.TButton")
apply_button.pack(pady=3)
save_sdf_button = ttk.Button(control_frame, text="Save SDF", command=save_sdf, style="Secondary.TButton")
save_sdf_button.pack(pady=3)
save_pdb_button = ttk.Button(control_frame, text="Save PDB", command=save_pdb, style="Secondary.TButton")
save_pdb_button.pack(pady=3)
home_button = ttk.Button(control_frame, text="Back to Start", command=return_to_front_page, style="Secondary.TButton")
home_button.pack(pady=3)
exit_button = ttk.Button(control_frame, text="Exit", command=root.destroy, style="Secondary.TButton")
exit_button.pack(pady=3)

similar_tab.grid_columnconfigure(0, weight=1)
similar_title = tk.Label(
similar_tab,
text="Similar Molecules",
font=TITLE_FONT,
bg=BG,
fg=TEXT
)
similar_title.grid(row=0, column=0, pady=(28, 8), padx=24, sticky="w")
similar_status = tk.Label(
similar_tab,
text="Search for a drug in the Explorer tab to load similar molecules.",
font=FONT,
bg=BG,
fg=MUTED,
justify="left"
)
similar_status.grid(row=1, column=0, pady=(0, 16), padx=24, sticky="w")
similar_table_frame = tk.LabelFrame(
similar_tab,
text="Similarity Results",
font=PANEL_FONT,
bg=CARD_BG,
fg=PANEL_TITLE,
bd=1,
relief="solid",
padx=18,
pady=16,
highlightbackground=BORDER
)
similar_table_frame.grid(row=2, column=0, padx=24, pady=10, sticky="nsew")
similar_tab.grid_rowconfigure(2, weight=1)
similar_table = ttk.Treeview(
similar_table_frame,
columns=("Name", "CID", "Formula", "MW", "Similarity"),
show="headings",
height=14
)
similar_table.heading("Name", text="Name")
similar_table.heading("CID", text="CID")
similar_table.heading("Formula", text="Formula")
similar_table.heading("MW", text="MW")
similar_table.heading("Similarity", text="Similarity")
similar_table.column("Name", width=420)
similar_table.column("CID", width=110)
similar_table.column("Formula", width=180)
similar_table.column("MW", width=100)
similar_table.column("Similarity", width=120)
similar_table.pack(side="left", fill="both", expand=True)
similar_scrollbar = ttk.Scrollbar(similar_table_frame, command=similar_table.yview)
similar_scrollbar.pack(side="right", fill="y")
similar_table.config(yscrollcommand=similar_scrollbar.set)
similar_table.bind("<Double-1>", open_similar_molecule)

comparison_tab.grid_columnconfigure(0, weight=1)
comparison_tab.grid_rowconfigure(0, weight=1)
comparison_canvas = tk.Canvas(comparison_tab, bg=BG, highlightthickness=0)
comparison_page_scrollbar = ttk.Scrollbar(comparison_tab, orient="vertical", command=comparison_canvas.yview)
comparison_content = tk.Frame(comparison_canvas, bg=BG)
comparison_content.bind(
"<Configure>",
lambda e: comparison_canvas.configure(scrollregion=comparison_canvas.bbox("all"))
)
comparison_canvas_window = comparison_canvas.create_window((0, 0), window=comparison_content, anchor="n", width=1280)
comparison_canvas.configure(yscrollcommand=comparison_page_scrollbar.set)
comparison_canvas.bind(
"<Configure>",
lambda e: comparison_canvas.itemconfigure(comparison_canvas_window, width=e.width)
)
comparison_canvas.grid(row=0, column=0, sticky="nsew")
comparison_page_scrollbar.grid(row=0, column=1, sticky="ns")
comparison_content.grid_columnconfigure(0, weight=1)
comparison_title = tk.Label(
comparison_content,
text="Molecule Comparison",
font=TITLE_FONT,
bg=BG,
fg=TEXT
)
comparison_title.grid(row=0, column=0, pady=(28, 8), padx=24, sticky="w")
comparison_input_frame = tk.LabelFrame(
comparison_content,
text="Compare Two Molecules",
font=PANEL_FONT,
bg=CARD_BG,
fg=PANEL_TITLE,
bd=1,
relief="solid",
padx=18,
pady=14,
highlightbackground=BORDER
)
comparison_input_frame.grid(row=1, column=0, padx=24, pady=(4, 12), sticky="ew")
comparison_input_frame.grid_columnconfigure(0, weight=1)
comparison_input_frame.grid_columnconfigure(1, weight=1)
comparison_a_entry = tk.Entry(
comparison_input_frame,
font=FONT,
bg=INPUT_BG,
fg=TEXT,
insertbackground=TEXT,
relief="solid",
bd=1,
highlightthickness=1,
highlightbackground=BORDER,
highlightcolor=ACCENT
)
comparison_a_entry.grid(row=0, column=0, padx=(0, 8), pady=6, sticky="ew", ipady=7)
comparison_b_entry = tk.Entry(
comparison_input_frame,
font=FONT,
bg=INPUT_BG,
fg=TEXT,
insertbackground=TEXT,
relief="solid",
bd=1,
highlightthickness=1,
highlightbackground=BORDER,
highlightcolor=ACCENT
)
comparison_b_entry.grid(row=0, column=1, padx=(8, 0), pady=6, sticky="ew", ipady=7)
comparison_button = ttk.Button(
comparison_input_frame,
text="Compare",
command=compare_molecules,
style="Modern.TButton"
)
comparison_button.grid(row=0, column=2, padx=(14, 0), pady=6)
comparison_a_entry.bind("<Return>", lambda event: compare_molecules())
comparison_b_entry.bind("<Return>", lambda event: compare_molecules())

comparison_view_frame = tk.Frame(comparison_content, bg=BG)
comparison_view_frame.grid(row=2, column=0, padx=24, pady=4, sticky="ew")
comparison_view_frame.grid_columnconfigure(0, weight=1, uniform="compare")
comparison_view_frame.grid_columnconfigure(1, weight=1, uniform="compare")

comparison_a_frame = tk.LabelFrame(
comparison_view_frame,
text="Molecule A",
font=PANEL_FONT,
bg=CARD_BG,
fg=PANEL_TITLE,
bd=1,
relief="solid",
padx=18,
pady=14,
highlightbackground=BORDER
)
comparison_a_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
comparison_b_frame = tk.LabelFrame(
comparison_view_frame,
text="Molecule B",
font=PANEL_FONT,
bg=CARD_BG,
fg=PANEL_TITLE,
bd=1,
relief="solid",
padx=18,
pady=14,
highlightbackground=BORDER
)
comparison_b_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

comparison_name_a = tk.Label(comparison_a_frame, text="First molecule", font=PANEL_FONT, bg=CARD_BG, fg=TEXT)
comparison_name_a.pack(pady=(0, 8))
comparison_image_a = tk.Label(comparison_a_frame, bg=CARD_BG)
comparison_image_a.pack(pady=(0, 10))
comparison_3d_a_canvas = tk.Canvas(
comparison_a_frame,
width=320,
height=220,
bg="#1e1e1e",
highlightthickness=1,
highlightbackground=BORDER
)
comparison_3d_a_canvas.pack(pady=6)
comparison_3d_a_canvas.create_text(160, 110, text="3D model A", fill=MUTED, font=FONT)

comparison_name_b = tk.Label(comparison_b_frame, text="Second molecule", font=PANEL_FONT, bg=CARD_BG, fg=TEXT)
comparison_name_b.pack(pady=(0, 8))
comparison_image_b = tk.Label(comparison_b_frame, bg=CARD_BG)
comparison_image_b.pack(pady=(0, 10))
comparison_3d_b_canvas = tk.Canvas(
comparison_b_frame,
width=320,
height=220,
bg="#1e1e1e",
highlightthickness=1,
highlightbackground=BORDER
)
comparison_3d_b_canvas.pack(pady=6)
comparison_3d_b_canvas.create_text(160, 110, text="3D model B", fill=MUTED, font=FONT)

comparison_results_frame = tk.LabelFrame(
comparison_content,
text="Similarities and Differences",
font=PANEL_FONT,
bg=CARD_BG,
fg=PANEL_TITLE,
bd=1,
relief="solid",
padx=18,
pady=14,
highlightbackground=BORDER
)
comparison_results_frame.grid(row=3, column=0, padx=24, pady=(12, 24), sticky="nsew")
comparison_content.grid_rowconfigure(3, weight=1)
comparison_summary = tk.Label(
comparison_results_frame,
text="Enter two molecule names or CIDs to compare structure and descriptors.",
font=FONT,
bg=CARD_BG,
fg=TEXT,
justify="left",
wraplength=1120
)
comparison_summary.pack(fill="x", pady=(0, 12))
comparison_table = ttk.Treeview(
comparison_results_frame,
columns=("Property", "Molecule A", "Molecule B", "Difference"),
show="headings",
height=10
)
comparison_table.heading("Property", text="Property")
comparison_table.heading("Molecule A", text="Molecule A")
comparison_table.heading("Molecule B", text="Molecule B")
comparison_table.heading("Difference", text="A - B / Note")
comparison_table.column("Property", width=220)
comparison_table.column("Molecule A", width=180)
comparison_table.column("Molecule B", width=180)
comparison_table.column("Difference", width=180)
comparison_table.pack(side="left", fill="both", expand=True)
comparison_scrollbar = ttk.Scrollbar(comparison_results_frame, command=comparison_table.yview)
comparison_scrollbar.pack(side="right", fill="y")
comparison_table.config(yscrollcommand=comparison_scrollbar.set)

draw_hero_molecule()
draw_comparison_models()
root.after(5000, show_main_app)
root.mainloop()